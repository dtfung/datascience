# -*- coding: utf-8 -*-
"""
@author: donald fung

Credit to Guido Zuidhof for providing a tutorial on how to preprocess the data for this challenge.
Link to tutorial below:
https://www.kaggle.com/gzuidhof/data-science-bowl-2017/full-preprocessing-tutorial
"""
import os
import time
import numpy as np
import pandas as pd
import pydicom as dicom
import scipy.ndimage
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

STAGE1_INPUTS = 'data/raw/image_data/stage1/'
STAGE1_LABELS = 'data/raw/stage1_labels.csv'
STAGE1_INPUTS_PROCESSED = 'data/processed/'
    
def load_scans(path):
    """Reads data files and returns a list of Pandas dataframes"""
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)   
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices

def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope
        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)
        image[slice_number] += np.int16(intercept)
    return np.array(image, dtype=np.int16)

def resample(image, scan, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    spacing = np.array([scan[0].SliceThickness] + scan[0].PixelSpacing, dtype=np.float32)
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    return image, new_spacing

def largest_label_volume(im, bg=-1):
    vals, counts = np.unique(im, return_counts=True)

    counts = counts[vals != bg]
    vals = vals[vals != bg]

    if len(counts) > 0:
        return vals[np.argmax(counts)]
    else:
        return None

def segment_lung_mask(image, fill_lung_structures=True):
    # not actually binary, but 1 and 2. 
    # 0 is treated as background, which we do not want
    binary_image = np.array(image > -320, dtype=np.int8)+1
    labels = measure.label(binary_image)
    
    # Pick the pixel in the very corner to determine which label is air.
    # Improvement: Pick multiple background labels from around the patient
    # More resistant to "trays" on which the patient lays cutting the air 
    # around the person in half
    background_label = labels[0,0,0]
    
    #Fill the air around the person
    binary_image[background_label == labels] = 2
    
    # Method of filling the lung structures (that is superior to something like 
    # morphological closing)
    if fill_lung_structures:
        # For every slice we determine the largest solid structure
        for i, axial_slice in enumerate(binary_image):
            axial_slice = axial_slice - 1
            labeling = measure.label(axial_slice)
            l_max = largest_label_volume(labeling, bg=0)

            #This slice contains some lung
            if l_max is not None: 
                binary_image[i][labeling != l_max] = 1

    #Make the image actual binary
    binary_image -= 1 

    # Invert it, lungs are now 1
    binary_image = 1-binary_image 

    # Remove other air pockets insided body
    labels = measure.label(binary_image, background=0)
    l_max = largest_label_volume(labels, bg=0)

    if l_max is not None: # There are air pockets
        binary_image[labels != l_max] = 0
    return binary_image

def count_scans(filepath, num_patients):
    """This function finds out how many unique scans exist for each patient.  
    I included a variable, num_patients, to specify the number of patients 
    that we are interested in"""
    for d in os.listdir(filepath)[:num_patients]:
        print("Patient '{}' has {} scans".format(d, len(os.listdir(filepath + d))))

def process_scans():
    """Checks for a folder of processed scans.  If it doesn't
    exist, process the patient scans"""

    processed_folder = os.listdir(STAGE1_INPUTS_PROCESSED)
    
    # check if processed images doesn't exist
    if len(processed_folder) < 1:
        """Prepare images online.  This WILL take a long time.  
        If you decide to leave this process running, go 
        do other things with your life and check back in a 
        a few hours."""
        run()
    else:
        print('{} processed images found!'.format(len(processed_folder)))

def load_labels():
    """Create a pandas dataframe from the labels provided"""
    labels = pd.read_csv(STAGE1_LABELS)
    return labels

def run():
    """Iterate over each image, and then apply a series of steps as outlined below:
    1). Load scans and add calculate slice thickness
    2). Convert pixel values to Hounsefield Units(HU)
    3). Resampling
    4). Lung Segmentation

    Returns 
    -------
    ndarray
        The scan 
    """
    print('Begin preprocessing...')
    
    # list of folders in directory
    patients = os.listdir(STAGE1_INPUTS)
    patients.sort
    print('Retrieved list of image folders')
    print('--------------------------------\n')

    total_time = 0.0
    # iterate over and preprocess scans for each patient
    for i, patient in enumerate(patients[:2]):
        start = time.time()
        print('{}. Patient {}'.format(i, patient))
        # get folder path
        path = STAGE1_INPUTS + patient

        # load scan & calculate thickness
        scan = load_scans(path)
        print('    Loaded scan and saved slice thickness')

        # convert pixel values to Hounsefield Units(HU)
        hu_slices = get_pixels_hu(scan)
        print('    Converted pixel values to HU')

        # resampling
        pix_resampled, spacing = resample(hu_slices, scan, [1,1,1])
        print('    Resampling complete')

        # lung segmentation
        segmented_lungs_fill = segment_lung_mask(pix_resampled, True)
        print('    Segmented lungs complete')

        # save image to file
        np.save(file = STAGE1_INPUTS_PROCESSED + patient, 
                arr = segmented_lungs_fill,
                allow_pickle = False)
        print('    Image saved')
        end = time.time()
        print('    Finished processing.')  
        print('    Time elapsed on patient: {} seconds'.format(round(end-start, 2)))
        total_time += end-start
        print('    Total time elapsed: {} \n'.format(round(total_time, 2)))

if __name__=="__main__":
    run()   