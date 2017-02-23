# -*- coding: utf-8 -*-
"""
@author: donald fung
"""

import os
import time
import numpy as np
import pandas as pd
import pydicom as dicom
import scipy.ndimage
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    
def load_scans(path):
    print(path)
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

def count_scans(filepath, num_patients):
    """This function finds out how many unique scans exist for each patient.  I included a variable, num_patients,
    to specify the number of patients that we are interested in"""
    for d in os.listdir(filepath)[:num_patients]:
        print("Patient '{}' has {} scans".format(d, len(os.listdir(filepath + d))))

def run():
    """ Iterate over each image, and then apply a series of steps as outlined below:
    1). Load scans and add calculate slice thickness
    2). Convert pixel values to Hounsefield Units
    3). Resampling
    """
    # list of folders in directory
    patients = os.listdir(STAGE1_INPUTS)
    patients.sort

    # iterate over and preprocess scans for each patient
    for patient in patients:
        # TODO: load scans
    
if __name__=="__main__":
    run()   