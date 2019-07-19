import nibabel as nib
import numpy as np
import json
import os
import glob


def create_training_dataset(config_file):
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
        if 'sub-%s' % sub not in sub_list:
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
        elif i_key == 'masks':
            i_path = os.path.join(i_dir, i_key)
            # merge tractmasks
            to_be_merged = glob.glob(i_path + '/*.nii.gz')
            to_be_merged.sort()

            if len(class_list) == 0:
                class_list = [os.path.basename(c) for c in to_be_merged]
                class_list = [c.split('.nii.gz')[0] for c in class_list]

            nii_merged_mask = merge_masks(to_be_merged)
            nib.save(nii_merged_mask, os.path.join(sub_dir, 'masks.nii.gz'))
    print('dataset folders for %d subjects created' % len(sub_list))

    #TODO: CROSSVALIDATION

    perc_val = cfg['perc_val']
    sub_train, sub_val = split_subjects(sub_list, perc_val, seed=10)
    print('using %d subjects for training and %d subjects for validation' 
                                        % (len(sub_train), len(sub_val)))

    with open('config_training_template.json', 'rb') as f:
        ts_config = json.load(f)
        print('reading config_training_template.json')

    ts_config['train_subjects'] = sub_train
    ts_config['validation_subjects'] = sub_val
    ts_config['test_subjects'] = sub_val
    
    ts_config['tractseg_data_dir'] = out_dataset_dir 
    ts_config['exp_name'] = 'output'
    ts_config['exp_path'] = './'
    
    ts_config['tractseg_dir'] = ''
    ts_config['num_epochs'] = cfg['num_epochs']
    ts_config['classes'] = class_list

    with open('brainlife-utils/brainlife_config_training.json', 'wb') as f:
        json.dump(ts_config, f)
        print('written brainlife_config_training.json')
        
        
def create_test_dataset(config_file):
    with open(config_file, 'rb') as cfg_src:
        cfg = json.load(cfg_src)
        print('reading app config file')

    # dictionary of inputs
    #inputs = cfg["_inputs"]
    out_dataset_dir = './dataset'

    sub_list = []
    p_path = cfg["peaks"].encode('utf-8')
    p_path = os.path.abspath(p_path)
    npz_path = cfg["npz"].encode('utf-8')
    npz_path = os.path.abspath(npz_path)
    hyp_path = cfg["hparam"].encode('utf-8')
    hyp_path = os.path.abspath(hyp_path)
    
    # creating peaks directory
    sub = cfg["_inputs"][0]['meta']['subject'].encode('utf-8')
    sub_dir = os.path.join(out_dataset_dir, 'sub-' + sub)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    os.system('ln -s %s %s/%s' % (p_path, sub_dir, os.path.basename(p_path)))    
        
    # creating fake empty masks
    p = nib.load(p_path)
    msk_path = '%s/%s' % (sub_dir, 'masks.nii.gz') 
    classes = read_classes(hyp_path)
    msk = np.expand_dims(np.zeros(p.get_data().shape[:3]),len(classes))
    nib.save(
        nib.Nifti1Image(msk, affine=p.affine, header=p.header.copy()),
        msk_path)    
    
    #for i in inputs:
    #    # i is an input data
    #   i_dir = os.path.join('..', i['task_id'],
    #                         i['dataset_id']).encode('utf-8')

     #   i_key = i['keys'][0].encode('utf-8')

      #  if i_key == 'peaks':
       #     sub = i['meta']['subject'].encode('utf-8')
        ##   sub_dir = os.path.join(out_dataset_dir, 'sub-' + sub)
        #    if not os.path.exists(sub_dir):
        #        os.makedirs(sub_dir)
        #    p_path = os.path.join(i_dir, i_key + '.nii.gz')
        #    p_path = os.path.abspath(p_path)
        #   p = nib.load(p_path)
        #   os.system(
        #       'ln -s %s %s/%s' % (p_path, sub_dir, os.path.basename(p_path)))
        #   # creating fake empty masks
        #    msk_path = '%s/%s' % (sub_dir, 'masks.nii.gz') 
        #    msk = np.expand_dims(np.zeros(p.get_data().shape[:3]),3)
        #    nib.save(
        #        nib.Nifti1Image(msk, affine=p.affine, header=p.header.copy()),
        #        msk_path)
       # elif i_key == 'npz':
       #     npz_path = glob.glob(i_dir + '/*.npz')[0]
       #     npz_path = os.path.abspath(npz_path)
       # elif i_key == 'hparam': 
       #     hyp_path = os.path.join(i_dir, 'Hyperparameters.txt')
       #     hyp_path = os.path.abspath(hyp_path)
       #     os.system('cp %s .' % hyp_path)
    
    
    if not os.path.exists('./test_output'):
        os.makedirs('./test_output')        
    os.system('ln -s %s ./test_output/weights.npz' % npz_path)    

    print('dataset folders created')

    with open('config_test_template.json', 'rb') as f:
        ts_config = json.load(f)
        print('reading config_test_template.json')

    ts_config['test_subjects'] = sub_list
    ts_config['weights_path'] = 'weights.npz'
    ts_config['classes'] = classes
    ts_config['tractseg_data_dir'] = out_dataset_dir 
    ts_config['exp_name'] = 'test_output'
    ts_config['exp_path'] = './'
    
    ts_config['tractseg_dir'] = ''

    with open('brainlife-utils/brainlife_config_test.json', 'wb') as f:
        json.dump(ts_config, f)
        print('written brainlife_config_test.json')        


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
    aff = nii_merged_img.affine.copy()
    hdr = nii_merged_img.header.copy()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(nii_merged_img.shape(3)):
        img = nii_merged_img[:,:,:,i]
        img_name = class_list[i]
        nii_img = nib.Nifti1Image(img, affine=aff, header=hdr)
        nib.save(nii_img, 
                os.path.join(output_dir, img_name + '.nii.gz'))


def split_subjects(sub_list, perc_val, seed=None):
    n_sub = len(sub_list)
    if seed != None:
        np.random.seed(seed)
    n_sub_val = max(int(np.floor(perc_val * n_sub)),1)
    sub_val = np.random.choice(sub_list, n_sub_val, replace=False).tolist()
    sub_train = [s for s in sub_list if s not in sub_val]

    return sub_train, sub_val

def read_classes(txt):
    with open(txt, 'rb') as f:
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

        return classes
    
