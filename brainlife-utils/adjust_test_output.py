#!/usr/bin/env python

import nibabel as nib
import glob
import os
import json
from data_utils import split_masks

if __name__ == '__main__':
    pred_file = glob.glob('./test_output/segmentations/*.nii.gz')[0]
    pred = nib.load(pred_file)
    
    # correct predictions size
    corrected_pred = nib.Nifti1Image(pred.get_data()[:-1,:,:-1,:],
                                    affine=pred.affine.copy(),
                                    header=pred.header.copy())

    # read classes
    with open('brainlife-utils/brainlife_config_test.json', 'rb') as f:
        cfg = json.load(f)

    classes = cfg['classes']
    classes = [c.encode('utf-8') for c in classes]

    # create masks dir
    outdir = './output/masks'

    # split masks
    split_masks(corrected_pred, classes, outdir)
    print('Segmented masks created')

