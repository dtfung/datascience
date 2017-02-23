"""
@author: donald fung
"""
import os
import sys

RANDOM_STATE = 7

""" Set batch size.  The lower it is, the noisier the training 
signal is going to be.  The higher it is, the longer it will take 
to compute the gradient for each step."""
BATCH_SIZE = 256

""" Change current directory to parent directory by setting
CHANGE_DIR to True.  You will only need to do this if you are having 
issues importing modules.  All source files for this project are stored 
under 'src'.
"""
CHANGE_DIR = True

""" Prepare the images offline by setting PREPARE_OFFLINE to True.  This is 
recommended so as to reduce the processing time during the training process.
"""
PREPARE_OFFLINE = True

""" Set to True to change current directory.  You will only need to set this
to True if you are having trouble accessing modules from other folders"""
CHANGE_DIR = True

STAGE1_INPUTS = 'data/raw/image_data/stage1'
STAGE1_LABELS = 'data/raw/stage1_labels.csv'

def set_sys_path():
    '''Change system path to parent folder'''
    for i in range(0, 2):
        os.chdir('..')
    cwd = os.getcwd()
    sys.path.append(cwd)

def predict_cancer():
    """This function contains several steps.  The first 
    prepares all the images before being fed to a neural
    network."""
    from src.preprocess import prepare_dataset
    prepare_dataset.load_scans()

if __name__ == "__main__":
    # Change sys.path if needed
    if CHANGE_DIR is True:
        set_sys_path()
    predict_cancer()
