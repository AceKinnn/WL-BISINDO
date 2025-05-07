<div align="center">
<h1>
<b>
Banten BISINDO Video Dataset (BBVD): An Indonesian Sign Language Dataset and Baseline Methods
</b>
</h1>
</div>

> by **[Grace Oktaviani Kindy](https://github.com/AceKinnn)** and **[Glenn Leonali](https://github.com/lenoel777)**, BINUS University<br>

We introduce a video dataset BBVD for Indonesian Sign Language task. BBVD dataset size is about 2.16 GB, and it contains 1600 RGB videos for 32 sign language gestures from 5 singers, with each class containing 10 samples.

## Data Spliting
Download the data first from google drive.
In this repository, there are 2 types of data splitting:
1. Split by number of samples
   <p>The number of samples for each glosses are split to 70% train data and 30% test data, provided in the script using the metadata</p>
2. Split by number of signers
   <p>The number of samples are split based on signers (4 signers for train data and 1 signer for test data), provided in the script using the metadata</p>

Then run [organize_dataset.py](https://github.com/AceKinnn/BBVD/blob/main/organize_dataset.py) using the respective metadata to split the video to train and test folder, with the following command:
```shell
python organize_dataset.py
   --metadata [str; the path to the json file]
   --source all_videos [str; the path to the videos folder]
   --output dataset_signer_split [str; the path to the desired output folder]
```

Examples of the usage:
```shell
python organize_dataset.py --metadata train_test_signer_split_metadata.json --source all_videos --output dataset_signer_split
```

## Data Processing 
1. Pose-based data
   <p>We use Vision API to preprocess the data, and output csv file for both train and test. Other alternatives can also use MediaPipe or OpenPose.
   This data can be used directly for SPOTER. However for Siformer, we did an additional step which is to standardise the frame numbers for each sample by padding additional zeros at the end of the corresponding skeletal data based on the maximum number of frames. The padded zeros have minimal to no impact on computational efficiency, because of the nature of the attention mechanism Siformer adopted.</p>   
2. Image-based data
