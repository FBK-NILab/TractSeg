import nibabel as nib
import numpy as np
import json
import os
import glob


def create_dataset(config_file):
    with open(config_file, 'rb') as cfg_src:
        cfg = json.load(cfg_src)
        print('reading app config file')

    # dictionary of inputs
    inputs = cfg["_inputs"]

    out_dataset_dir = './dataset'

    sub_list = []
    class_list = []
    for i in inputs:
        sub = i['meta']['subject'].encode('utf-8')
        if sub not in sub_list:
            sub_list.append('sub-' + sub)
        sub_dir = os.path.join(out_dataset_dir, 'sub-' + sub)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        # i is an input data
        i_dir = os.path.join('..', i['task_id'],
                             i['dataset_id']).encode('utf-8')

        i_key = i['keys'][0].encode('utf-8')
        if i_key == 'peaks':
            i_path = os.path.join(i_dir, i_key + '.nii.gz')
            i_path = os.path.abspath(i_path)
            os.system(
                'ln -s %s %s/%s' % (i_path, sub_dir, os.path.basename(i_path)))
        elif i['keys'][0] == 'masks':
            i_path = os.path.join(i_dir, i_key)
            # merge tractmasks
            to_be_merged = glob.glob(i_path + '/*.nii.gz')
            to_be_merged.sort()

            if len(class_list) == 0:
                class_list = [os.path.basename(c) for c in to_be_merged]
                class_list = [c.split('.nii.gz')[0] for c in class_list]

            nii_merged_mask = merge_masks(to_be_merged)
            nib.save(nii_merged_mask, os.path.join(sub_dir, 'masks.nii.gz'))
    print('dataset folders created')

    #TODO: CROSSVALIDATION

    perc_val = eval(cfg['perc_val'])
    sub_train, sub_val = split_subjects(sub_list, perc_val, seed=10)
    print('using %d subjects for training and %d subjects for validation' 
                                        % (len(sub_train), len(sub_val)))

    with open('config_training_template.json', 'rb') as f:
        ts_config = json.load(f)
        print('reading config_training_template.json')

    ts_config['train_subjects'] = sub_train
    ts_config['validation_subjects'] = sub_val
    
    ts_config['tractseg_data_dir'] = out_dataset_dir 
    ts_config['exp_name'] = 'output'
    ts_config['exp_path'] = './'
    
    ts_config['tractseg_dir'] = ''
    ts_config['num_epochs'] = cfg['num_epochs']
    ts_config['classes'] = class_list

    with open('brainlife-utils/brainlife_config_training.json', 'wb') as f:
        json.dump(ts_config)
        print('written brainlife_config_training.json')


def merge_masks(nifti_list):
    """
    Given a list of nifti images having all the same shape this function returns a single nifti file where images are stacked in the last dimension
    (4th dimension)
    """
    for i, nii in enumerate(nifti_list):
        img = nib.load(nii)
        img_data = img.get_data()
        if i == 0:
            aff = img.affine.copy()
            hdr = img.header.copy()
            merged_img = np.expand_dims(img_data, 3)
            continue
        merged_img = np.concatenate((merged_img, np.expand_dims(img_data, 3)),
                                    axis=3)

    nii_merged_img = nib.Nifti1Image(
        merged_img.astype(np.uint8), affine=aff, header=hdr)

    return nii_merged_img


def split_masks(nii_merged_img, class_list, output_dir):
    aff = merged_img.affine.copy()
    hdr = merged_img.header.copy()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(merged_img.shape(3)):
        img = merged_img[:,:,:,i]
        img_name = class_list[i]
        nii_img = nib.Nifti1Image(img, affine=aff, header=hdr)
        nib.save(nii_img, 
                os.path.join(output_dir, img_name + '.nii.gz'))


def split_subjects(sub_list, perc_val, seed=None):
    n_sub = len(sub_list)
    if seed != None:
        np.random.seed(seed)
    n_sub_val = max(np.floor(perc_val * n_sub),1)
    sub_val = np.random.choice(sub_list, n_sub_val, replace=False).tolist()
    sub_train = [s for s in sub_list if s not in sub_val]

    return sub_train, sub_val

