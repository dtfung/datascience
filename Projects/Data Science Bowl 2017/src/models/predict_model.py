"""
@author: donald fung
"""
<<<<<<< HEAD

import os
import sys

=======
import os
import sys

# SETTINGS
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea
RANDOM_STATE = 7

""" Set batch size.  The lower it is, the noisier the training 
signal is going to be.  The higher it is, the longer it will take 
to compute the gradient for each step."""
BATCH_SIZE = 256

<<<<<<< HEAD
""" Change current directory to parent directory by setting
CHANGE_DIR to True.  You will only need to do this if you are having 
issues importing modules.  All source files for this project are stored 
under 'src'.
"""
CHANGE_DIR = True

""" Prepare the images offline by setting PREPARE_OFFLINE to True.  This is 
recommended so as to reduce the processing time during the training process.
=======
""" Set to True to change current directory to access image data.  
You more than likely won't need to do this, but if your compiler 
throws a FileNotFoundError, you can modify the set_sys_path() 
function to access the desired folder """
CHANGE_DIR = True

""" Set to True to prepare the images offline.  This is recommended
so as to reduce the processing time during the training process.
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea
WARNING:  If set to False, the training process will take a while
"""
PREPARE_OFFLINE = True

<<<<<<< HEAD
=======
# FILES
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea
STAGE1_INPUTS = 'data/raw/image_data/stage1'
STAGE1_LABELS = 'data/raw/stage1_labels.csv'

def set_sys_path():
<<<<<<< HEAD
    '''Change system path to parent folder'''
    for i in range(0, 2):
        os.chdir('..')
    src = os.getcwd()
    sys.path.append(src)

def preprocess_data():
    
    # list of folders in directory
    patients = os.listdir(STAGE1_INPUTS)
=======
    '''Sets current working directory to 2 parent folders above src/preprocess.'''
    for i in range(0, 2):
        os.chdir('..')
    print(os.getcwd())

def preprocess_data():
    '''Takes input'''

    # list of folders in directory
    patients = os.listdir('D:\\donal\\Documents\\Python Scripts\\datascience\\Projects\\Data Science Bowl 2017\\data\\model')
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea
    patients.sort

    # preprocess each image
    for patient in patients:
        # TODO: prepare data here
<<<<<<< HEAD
        pass
=======
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea

def predict_cancer():
    
    # Split data into train and test sets
    train, test = preprocess_data()

if __name__ == "__main__":
<<<<<<< HEAD

    # Change sys.path if needed
    if CHANGE_DIR is True:
        set_sys_path()

=======
>>>>>>> 14d36684a6960cf14c61ec8d799cec8012c857ea
    predict_cancer()
