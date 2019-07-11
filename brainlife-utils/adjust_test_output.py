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
    with open('Hyperparameters.txt', 'rb') as f:
        txt = f.read()
        txt = txt.replace('\'', '"')
        txt = txt.replace('False','false')
        txt = txt.replace('True','true')
        txt = txt.replace('None','""')
        txt = txt.rsplit('}',1)[0] + '}'
        txt = txt.replace('(','[')
        txt = txt.replace(')',']')
        txt = txt.replace('u"','"')
        cfg = json.loads(txt)

    classes = cfg['CLASSES']
    classes = [c.encode('utf-8') for c in classes]
    classes.sort()

    # create masks dir
    outdir = './output/masks'

    # split masks
    split_masks(corrected_pred, classes, outdir)
    print('Segmented masks created')

