import os.path
import glob
import nibabel as nib
import numpy as np
import cv2

files = glob.glob("/content/HGG/*/")
modality = 't2' #'t1' #'flair' #'t1ce'
output_path = '/content/core/' #'/content/whole/' #'/content/enhancing/'
output_path_seg = '/content/mask_core/' #'/content/mask_whole/' #'/content/mask_enhancing/'

for ff in files:
    nii_file = glob.glob(ff + '*' + modality + '.nii.gz')
    img = nib.load(str(nii_file[0]))  # img = io.imread(nii_file, plugin='simpleitk')
    img = img.get_fdata()

    # img = (img.get_fdata())[:,:,:,1]
    img = (img / img.max()) * 255
    img = img.astype(np.uint8)
    img_name = (nii_file[0].split('/')[-1]).split('.')[0]

    seg_file = glob.glob(ff + '*seg.nii.gz')
    seg = nib.load(str(seg_file[0]))
    seg = seg.get_fdata()
    print(np.unique(seg))

    mask_WT = seg.copy()
    mask_WT[mask_WT == 1] = 1
    mask_WT[mask_WT == 2] = 0
    mask_WT[mask_WT == 4] = 0

    mask_TC = seg.copy()
    mask_TC[mask_TC == 1] = 1
    mask_TC[mask_TC == 2] = 0
    mask_TC[mask_TC == 4] = 1

    mask_ET = seg.copy()
    mask_ET[mask_ET == 1] = 0
    mask_ET[mask_ET == 2] = 0
    mask_ET[mask_ET == 4] = 1

#### we choose which part of tumor we want (whole,core or enhancing)
    # seg1=mask_WT.copy()
    # seg1=mask_ET.copy()
    seg1 = mask_TC.copy()

    # seg = seg >0
    # seg = (seg/seg.max())*255
    seg_name = (seg_file[0].split('/')[-1]).split('.')[0]

    for slice in range(65, 110):  # choose the slice range other slices have no information
        sg = seg1[:, :, slice]
        a = np.where(sg != 0)
        #         print(a)
        if np.size(a) > 1:
            filename = os.path.join(output_path, img_name + '_' + str(slice) + '.jpg')
            seg_filename = os.path.join(output_path_seg, seg_name + '_' + str(slice) + '.jpg')

            im = img[:, :, slice]
            # print(filename)
            #             t2s = (t2s-(t2s[t2s > 0]).mean()) / (t2s[t2s > 0]).std()
            im = ((im - im.min()) * (1 / (im.max() - im.min()) * 255)).astype('uint8')
            sg = ((sg - sg.min()) * (1 / (sg.max() - sg.min()) * 255)).astype('uint8')

            cv2.imwrite(filename, im)
            cv2.imwrite(seg_filename, sg)