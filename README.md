<div align="center">
<h1>
<b>
Banten BISINDO Video Dataset (BBVD): An Indonesian Sign Language Dataset and Baseline Methods
</b>
</h1>
</div>

> by **[Grace Oktaviani Kindy](https://github.com/AceKinnn)** and **[Glenn Leonali](https://github.com/lenoel777)**, BINUS University<br>

We introduce a video dataset BBVD for Indonesian Sign Language task. BBVD dataset size is about 2.16 GB, and it contains 1600 RGB videos for 32 sign language gestures from 5 singers, with each class containing 10 samples.

## Download Data
BBVD can be downloaded from [Kaggle](https://www.kaggle.com/datasets/glennleonali/bbvd-all-videos).

<div style="display: flex; gap: 20px;">
  <div style="flex: 1;">
    <table>
      <tr><th>Label</th><th>Gloss</th><th>English Translation</th></tr>
      <tr><td>0</td><td>Air</td><td>Water</td></tr>
      <tr><td>1</td><td>Belajar</td><td>Learn</td></tr>
      <tr><td>2</td><td>Cari</td><td>Search</td></tr>
      <tr><td>3</td><td>Hari</td><td>Day</td></tr>
      <tr><td>4</td><td>Ingat</td><td>Remember</td></tr>
      <tr><td>5</td><td>Lagi</td><td>Again</td></tr>
      <tr><td>6</td><td>Maaf</td><td>Sorry</td></tr>
      <tr><td>7</td><td>Makan</td><td>Eat</td></tr>
    </table>
  </div>
  <div style="flex: 1;">
    <table>
      <tr><th>Label</th><th>Gloss</th><th>English Translation</th></tr>
      <tr><td>8</td><td>Motor</td><td>Motorcycle</td></tr>
      <tr><td>9</td><td>Saya</td><td>I</td></tr>
      <tr><td>10</td><td>Terima kasih</td><td>Thank you</td></tr>
      <tr><td>11</td><td>Tuli</td><td>Deaf</td></tr>
      <tr><td>12</td><td>Apa</td><td>What</td></tr>
      <tr><td>13</td><td>Siapa</td><td>Who</td></tr>
      <tr><td>14</td><td>Kapan</td><td>When</td></tr>
      <tr><td>15</td><td>Di mana</td><td>Where</td></tr>
    </table>
  </div>
  <div style="flex: 1;">
    <table>
      <tr><th>Label</th><th>Gloss</th><th>English Translation</th></tr>
      <tr><td>16</td><td>Mengapa</td><td>Why</td></tr>
      <tr><td>17</td><td>Bagaimana</td><td>How</td></tr>
      <tr><td>18</td><td>Merah</td><td>Red</td></tr>
      <tr><td>19</td><td>Kuning</td><td>Yellow</td></tr>
      <tr><td>20</td><td>Hijau</td><td>Green</td></tr>
      <tr><td>21</td><td>Hitam</td><td>Black</td></tr>
      <tr><td>22</td><td>Dengar</td><td>Hear</td></tr>
      <tr><td>23</td><td>Berangkat</td><td>Depart</td></tr>
    </table>
  </div>
  <div style="flex: 1;">
    <table>
      <tr><th>Label</th><th>Gloss</th><th>English Translation</th></tr>
      <tr><td>24</td><td>Datang</td><td>Come</td></tr>
      <tr><td>25</td><td>Teman</td><td>Friend</td></tr>
      <tr><td>26</td><td>Keluarga</td><td>Family</td></tr>
      <tr><td>27</td><td>Rumah</td><td>House</td></tr>
      <tr><td>28</td><td>Pagi</td><td>Morning</td></tr>
      <tr><td>29</td><td>Siang</td><td>Noon</td></tr>
      <tr><td>30</td><td>Sore</td><td>Afternoon</td></tr>
      <tr><td>31</td><td>Malam</td><td>Night</td></tr>
    </table>
  </div>
</div>


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

