[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.204-blue.svg)](https://doi.org/10.25663/brainlife.app.204)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.205-blue.svg)](https://doi.org/10.25663/brainlife.app.205)

# TractSeg training and test
The Apps [TractSeg training](https://doi.org/10.25663/brainlife.app.204) and [TractSeg test](https://doi.org/10.25663/brainlife.app.205) are derived from the original App [TractSeg](https://doi.org/10.25663/brainlife.app.186), with the difference that you can perform your own training on your own data. TractSeg is a tool for fast and accurate white matter bundle segmentation from Diffusion MRI, developed by (Wasserthal et al., 2018), under Apache-2.0 License. Please refer to this App https://doi.org/10.25663/brainlife.app.186 and this repository https://github.com/MIC-DKFZ/TractSeg for a comprehensive documentation of the method.

### TractSeg training App
The App for training TractSeg on your own data is https://doi.org/10.25663/brainlife.app.204.

Inputs: \
CSD peaks and ground truth segmentation bundle masks that you want to use to train the network, of multiple subjects. CSD peaks can be obtained from dwi data using this App: https://doi.org/10.25663/brainlife.app.172.

Outputs: \
Pretrained weights computed by training the network, that you can use as input for the TractSeg test App. 

### TractSeg test App
The App for testing TractSeg after your own training is https://doi.org/10.25663/brainlife.app.205.

Inputs: \
CSD Peaks of the (single) subject you want to obtain the bundle segmentation and the pretrained weights computed by training the network with the TractSeg training App.

Outputs: \
Bundle segmentation as list of bundle masks in nifti format.

### Authors
- Pietro Astolfi (pietroastolfi92@gmail.com)
- Giulia Bertò (giulia.berto.4@gmail.com)

### Contributors
- Paolo Avesani (avesani@fbk.eu)
- Soichi Hayashi (hayashis@iu.edu)

### Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations
TractSeg is the code for the following papers. Please cite the papers if you use it. 
* Tract Segmentation:   
[TractSeg - Fast and accurate white matter tract segmentation](https://doi.org/10.1016/j.neuroimage.2018.07.070) ([free arxiv version](https://arxiv.org/abs/1805.07103))
[NeuroImage 2018]
* Tract Orientation Mapping (TOM):   
[Tract orientation mapping for bundle-specific tractography](https://arxiv.org/abs/1806.05580)
[MICCAI 2018]
* Tracking on TOMs:   
[Combined tract segmentation and orientation mapping for bundle-specific tractography](https://arxiv.org/abs/1901.10271)
[submitted to MIA]

We also kindly ask that you cite the following articles when publishing papers and code using this code. 

* Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Running the Apps 

### On Brainlife.io

You can submit the TractSeg training App online at [https://doi.org/10.25663/bl.app.204](https://doi.org/10.25663/bl.app.204) via the "Execute" tab.

You can submit the TractSeg test App online at [https://doi.org/10.25663/bl.app.205](https://doi.org/10.25663/bl.app.205) via the "Execute" tab.

### Dependencies
This Apps only requires [singularity](https://www.sylabs.io/singularity/) to run.
