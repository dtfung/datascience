# -*- coding: utf-8 -*-
import os
import click
import logging

@click.command()
@click.argument('input_filepath', type = click.Path(exists=True))
@click.argument('output_filepath', type = click.Path())
@click.argument('stage_1_image_data', nargs = 1) 
@click.argument('stage_1_labels', nargs = 1) 
@click.argument('data_password', nargs = 1) 
def main(input_filepath, output_filepath, stage_1_image_data, stage_1_labels, data_password):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Reading files from raw data folder')
    logger.info('')
    logger.info('Begin making final data set from raw data')

def read_files(input_filepath, output_filepath):
    """Reads data files and returns a list of Pandas dataframes"""
    pass
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
