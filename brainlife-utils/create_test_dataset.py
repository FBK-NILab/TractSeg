#!/usr/bin/env python

from data_utils import create_test_dataset

if __name__ == '__main__':
    # create dataset for test
    print('starting dataset creation')
    create_test_dataset('config.json')
    print('dataset for test created')
