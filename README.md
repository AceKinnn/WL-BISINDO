# Banten BISINDO Video Dataset (BBVD): An Indonesian Sign Language Dataset and Baseline Methods

We introduce a video dataset BBVD for Indonesian Sign Language task. BBVD dataset size is about 2.16 GB, and it contains 1600 RGB videos for 32 sign language gestures from 5 singers, with each class containing 10 samples.

## Data Spliting
Download the data first from google drive.
In this repository, there are 2 types of data splitting:
1. Split by number of samples
   <p>The number of samples for each glosses are split to 70% train data and 30% test data, provided in the script using the metadata</p>
2. Split by number of signers
   The number of samples are split based on signers (4 signers for train data and 1 signer for test data), provided in the script using the metadata

## Data Processing
1. Pose-based data
   We use Vision API to preprocess the data, and output csv file for both train and test. Other alternatives can also use MediaPipe or OpenPose.
   This data can be used directly for SPOTER.
   However for Siformer, we did an additional step which is to standardise the frame numbers for each sample by padding additional zeros at the end of the corresponding skeletal data based on the maximum number of frames. The padded zeros have minimal to no impact on computational efficiency, because of the nature of the attention mechanism Siformer adopted.
   
2. Image-based data
