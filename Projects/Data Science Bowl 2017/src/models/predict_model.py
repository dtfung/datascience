"""
@author: donald fung
"""
import os
import sys
import numpy as np
import pandas as pd

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

STAGE1_INPUTS = 'data/raw/image_data/stage1/'
STAGE1_LABELS = 'data/raw/stage1_labels.csv'
STAGE1_INPUTS_PROCESSED = 'data/processed/'

def set_sys_path():
    """Change system path to parent folder"""
    for i in range(0, 2):
        os.chdir('..')
    cwd = os.getcwd()
    sys.path.append(cwd)
    
def predict_cancer():
    """This function contains several steps.  The first 
    loads all processed images before being fed to a neural
    network."""
    from src.preprocess import prepare_dataset
    # processed images
    prepare_dataset.process_scans()

    # load image label data into pandas dataframe
    train_labels = prepare_dataset.load_labels()
        
if __name__ == "__main__":
    # Change sys.path if needed
    if CHANGE_DIR is True:
        set_sys_path()
    predict_cancer()
