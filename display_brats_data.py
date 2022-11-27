import numpy as np
import nibabel as nib
import matplotlib as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

sample_filename_mask = '/content/BraTS20_Training_001_seg.nii.gz'
sample_mask = nib.load(sample_filename_mask)
sample_mask = np.asanyarray(sample_mask.dataobj)

flair = '/content/BraTS20_Training_001_flair.nii.gz'
flair = nib.load(flair)
flair = np.asanyarray(flair.dataobj)

print(f"img shape -> {flair.shape} and mask shape ->{sample_mask.shape}")

t1 = '/content/BraTS20_Training_001_t1.nii.gz'
t1 = nib.load(t1)
t1 = np.asanyarray(t1.dataobj)


t2 = '/content/BraTS20_Training_001_t2.nii.gz'
t2 = nib.load(t2)
t2 = np.asanyarray(t2.dataobj)


t1ce = '/content/BraTS20_Training_001_t1ce.nii.gz'
t1ce = nib.load(t1ce)
t1ce = np.asanyarray(t1ce.dataobj)


mask_WT = sample_mask.copy()
mask_WT[mask_WT == 1] = 1
mask_WT[mask_WT == 2] = 1
mask_WT[mask_WT == 4] = 1

mask_TC = sample_mask.copy()
mask_TC[mask_TC == 1] = 1
mask_TC[mask_TC == 2] = 0
mask_TC[mask_TC == 4] = 1

mask_ET = sample_mask.copy()
mask_ET[mask_ET == 1] = 0
mask_ET[mask_ET == 2] = 0
mask_ET[mask_ET == 4] = 1

mask = np.stack([mask_WT, mask_TC, mask_ET])
mask = np.moveaxis(mask, (0, 1, 2, 3), (0, 3, 2, 1))

fig = plt.figure(figsize=(20, 10))

gs = gridspec.GridSpec(nrows=2, ncols=4, height_ratios=[1, 1.5])

#  Varying density along a streamline
ax0 = fig.add_subplot(gs[0, 0])
flair = ax0.imshow(flair[:,:,65], cmap='bone')
ax0.set_title("FLAIR", fontsize=18, weight='bold', y=-0.2)
fig.colorbar(flair)

#  Varying density along a streamline
ax1 = fig.add_subplot(gs[0, 1])
t1 = ax1.imshow(t1[:,:,65], cmap='bone')
ax1.set_title("T1", fontsize=18, weight='bold', y=-0.2)
fig.colorbar(t1)

#  Varying density along a streamline
ax2 = fig.add_subplot(gs[0, 2])
t2 = ax2.imshow(t2[:,:,65], cmap='bone')
ax2.set_title("T2", fontsize=18, weight='bold', y=-0.2)
fig.colorbar(t2)

#  Varying density along a streamline
ax3 = fig.add_subplot(gs[0, 3])
t1ce = ax3.imshow(t1ce[:,:,65], cmap='bone')
ax3.set_title("T1 contrast", fontsize=18, weight='bold', y=-0.2)
fig.colorbar(t1ce)

# Varying density along a streamline
ax4 = fig.add_subplot(gs[1, 1:3])

l1 = ax4.imshow(mask_WT[:,:,65], cmap='summer',)
l2 = ax4.imshow(np.ma.masked_where(mask_TC[:,:,65]== False,  mask_TC[:,:,65]), cmap='viridis', alpha=0.6)
l3 = ax4.imshow(np.ma.masked_where(mask_ET[:,:,65] == False, mask_ET[:,:,65]), cmap='seismic', alpha=0.6)

ax4.set_title("", fontsize=20, weight='bold', y=-0.1)

_ = [ax.set_axis_off() for ax in [ax0,ax1,ax2,ax3, ax4]]

colors = [im.cmap(im.norm(1)) for im in [l1,l2,l3]]
labels = ['whole','core','ehnancing']
patches = [ mpatches.Patch(color=colors[i], label=f"{labels[i]}") for i in range(len(labels))]
# put those patched as legend-handles into the legend
plt.legend(handles=patches, bbox_to_anchor=(1.1, 0.65), loc=2, borderaxespad=0.4,fontsize = 'xx-large',
           title='Mask Labels', title_fontsize=18, edgecolor="black",  facecolor='#c5c6c7')