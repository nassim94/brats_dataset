# Implementation of Reading and displaying Brats Dataset

All BraTS multimodal scans are available as NIfTI files (.nii.gz).
In this dataset we have four modalities include T1, post-contrast T1-weighted (T1Gd), T2, and T2 Fluid Attenuated Inversion Recovery (T2-FLAIR) volumes.
All the imaging datasets have been segmented manually, by one to four raters, following the same annotation protocol, and their annotations were approved
by experienced neuro-radiologists. Annotations comprise the GD-enhancing tumor (ET — label 4), the peritumoral edema (ED — label 2), and the necrotic and
non-enhancing tumor core (NCR/NET — label 1)

# Convert NIFTI files to .jpg
We read brats dataset and save them as .jpg images and masks.
