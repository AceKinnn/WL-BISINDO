<div align="center">
<h1>
<b>
Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods
</b>
</h1>
</div>

> by **[Grace Oktaviani Kindy](https://github.com/AceKinnn)** and **[Glenn Leonali](https://github.com/lenoel777)**, BINUS University<br>

We introduce a video dataset WL-BISINDO for Indonesian Sign Language task. WL-BISINDO dataset size is about 2.16 GB, and it contains 1600 RGB videos for 32 sign language gestures from 5 singers, with each class containing 10 samples.

## Download Data
WL-BISINDO can be downloaded from [Kaggle](https://www.kaggle.com/datasets/glennleonali/bbvd-all-videos).


## Data Spliting
Download the data first from google drive.
In this repository, there are 2 types of data splitting:
### 1. Signer Dependent (SD)
Trained and evaluated using data from the same set of signers. This approach is suitable for <b>early-stage research</b> or when the target user is known (e.g., personalized systems). However, it's limited for generalization task to unseen signers.

The number of samples for each gloss is split into 70% training data and 30% test data, as specified in [SD_split_metadata.json](https://github.com/AceKinnn/BBVD/blob/main/data_structuring/SD_split_metadata.json)

### 2. Signer Independent (SI)
Trained on data from some signers and tested on data from completely different signers who were not seen during training to ensure <b>generalization</b> and <b>fairness</b> as it <b>simulates a more realistic scenario</b> where the model must recognize signs regardless of who is signing.

The dataset is split based on signers, with 4 signers used for training data and 1 signer reserved for testing data, as specified in [SI_split_metadata.json](https://github.com/AceKinnn/BBVD/blob/main/data_structuring/SI_split_metadata.json)

Then run [organize_dataset.py](https://github.com/AceKinnn/BBVD/blob/main/organize_dataset.py) using the respective metadata to split the video to train and test folder, with the following command:
```shell
python organize_dataset.py
   --metadata [str; the path to the json file]
   --source all_videos [str; the path to the videos folder]
   --output dataset_signer_split [str; the path to the desired output folder]
```

Examples of the usage:
```shell
python organize_dataset.py --metadata SI_split_metadata.json --source all_videos --output dataset_signer_split
```

## Data Processing 
### 1. Pose-based data
We use Vision API to preprocess the data, and output csv file for both train and test. Other alternatives can also use MediaPipe or OpenPose.

This data can be used directly for SPOTER. However for Siformer, we did an additional step which is to standardise the frame numbers for each sample by padding additional zeros at the end of the corresponding skeletal data based on the maximum number of frames. The padded zeros have minimal to no impact on computational efficiency, because of the nature of the attention mechanism Siformer adopted.

### 2. Image-based data

