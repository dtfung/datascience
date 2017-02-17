"""
@author: donald fung
"""
import os
import sys

# SETTINGS
RANDOM_STATE = 7

""" Set batch size.  The lower it is, the noisier the training 
signal is going to be.  The higher it is, the longer it will take 
to compute the gradient for each step."""
BATCH_SIZE = 256

""" Set to True to change current directory to access image data.  
You more than likely won't need to do this, but if your compiler 
throws a FileNotFoundError, you can modify the set_sys_path() 
function to access the desired folder """
CHANGE_DIR = True

""" Set to True to prepare the images offline.  This is recommended
so as to reduce the processing time during the training process.
WARNING:  If set to False, the training process will take a while
"""
PREPARE_OFFLINE = True

# FILES
STAGE1_INPUTS = 'data/raw/image_data/stage1'
STAGE1_LABELS = 'data/raw/stage1_labels.csv'

def set_sys_path():
    '''Sets current working directory to 2 parent folders above src/preprocess.'''
    for i in range(0, 2):
        os.chdir('..')
    print(os.getcwd())

def preprocess_data():
    '''Takes input'''

    # list of folders in directory
    patients = os.listdir('D:\\donal\\Documents\\Python Scripts\\datascience\\Projects\\Data Science Bowl 2017\\data\\model')
    patients.sort

    # preprocess each image
    for patient in patients:
        # TODO: prepare data here

def predict_cancer():
    
    # Split data into train and test sets
    train, test = preprocess_data()

if __name__ == "__main__":
    predict_cancer()
