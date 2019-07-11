#!/usr/bin/env python

from data_utils import create_training_dataset

if __name__ == '__main__':
    # create dataset for training
    print('starting dataset creation')
    create_training_dataset('config.json')
    print('dataset for training created')

