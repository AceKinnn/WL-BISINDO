# WL-BISINDO

> **Authors**: [Grace Oktaviani Kindy](https://github.com/AceKinnn), [Glenn Leonali](https://github.com/lenoel777) & Henry Lucky, BINUS University  
> **Paper**: [DOI:10.1016/j.procs.2025.08.277](https://doi.org/10.1016/j.procs.2025.08.277)

This repository accompanies the paper **[Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods](https://doi.org/10.1016/j.procs.2025.08.277)**. It contains the code to reproduce the baseline results presented in our work, which introduces **WL-BISINDO**—a new video dataset for **Bahasa Isyarat Indonesia (BISINDO)** focused on the **Banten regional variant**. The dataset comprises **1,600 RGB videos** of **32 isolated signs**, each performed by five signers from the Banten region of Indonesia.

Our work aims to support research in **Indonesian Sign Language Recognition (SLR)** and promote inclusive technologies for the Deaf community in Indonesia.

---

## 📥 Download Data

The WL-BISINDO dataset is publicly available on **Kaggle**:

🔗 [Download WL-BISINDO on Kaggle](https://www.kaggle.com/datasets/glennleonali/wl-bisindo)

> **Note**: The dataset is approximately **2.16 GB** and contains 1,600 videos (32 glosses × 10 samples × 5 signers).

| Label | Gloss           | English Translation | Label | Gloss           | English Translation |
|-------|------------------|----------------------|-------|------------------|----------------------|
| 0     | Air             | Water               | 16    | Mengapa         | Why                 |
| 1     | Belajar         | Learn               | 17    | Bagaimana       | How                 |
| 2     | Cari            | Search              | 18    | Merah           | Red                 |
| 3     | Hari            | Day                 | 19    | Kuning          | Yellow              |
| 4     | Ingat           | Remember            | 20    | Hijau           | Green               |
| 5     | Lagi            | Again               | 21    | Hitam           | Black               |
| 6     | Maaf            | Sorry               | 22    | Dengar          | Hear                |
| 7     | Makan           | Eat                 | 23    | Berangkat       | Depart              |
| 8     | Motor           | Motorcycle          | 24    | Datang          | Come                |
| 9     | Saya            | I                   | 25    | Teman           | Friend              |
| 10    | Terima kasih    | Thank you           | 26    | Keluarga        | Family              |
| 11    | Tuli            | Deaf                | 27    | Rumah           | House               |
| 12    | Apa             | What                | 28    | Pagi            | Morning             |
| 13    | Siapa           | Who                 | 29    | Siang           | Noon                |
| 14    | Kapan           | When                | 30    | Sore            | Afternoon           |
| 15    | Di mana         | Where               | 31    | Malam           | Night               |


---

## 🔀 Data Splitting

We provide two evaluation protocols to assess model generalization:

### 1. **Signer-Dependent (SD)**  
- Train and test on data from the **same signers**.  
- Suitable for early-stage research or personalized systems.  
- Split: **70% train / 30% test per gloss**.  
- Metadata: [`data_structuring/SD_split_metadata.json`](data_structuring/SD_split_metadata.json)

### 2. **Signer-Independent (SI)**  
- Train on **4 signers**, test on the **remaining 1 signer** (unseen during training).  
- Evaluates real-world generalization across individuals.  
- Four test configurations (one per signer held out).  
- Metadata:
   - [`data_structuring/SI_1_split_metadata.json`](data_structuring/SI_1_split_metadata.json)
   - [`data_structuring/SI_2_split_metadata.json`](data_structuring/SI_2_split_metadata.json)
   - [`data_structuring/SI_3_split_metadata.json`](data_structuring/SI_3_split_metadata.json)
   - [`data_structuring/SI_4_split_metadata.json`](data_structuring/SI_4_split_metadata.json)

### Organize Your Dataset

Use the provided script to split raw videos into `train/` and `test/` folders:

```bash
python organize_dataset.py \
  --metadata data_structuring/[SD|SI]_split_metadata.json \
  --source all_videos \
  --output dataset_[sd|si]
```

Example:
```bash
python organize_dataset.py --metadata data_structuring/SI_split_metadata.json --source all_videos --output dataset_si
```

---

## ⚙️ Data Preprocessing

Preprocessing differs by model type. Outputs are saved in separate model-specific folders.

### 1. **Pose-Based Models (SPOTER & Siformer)**
- Extract 2D skeletal keypoints using **[Vision API](https://github.com/thanhdolong/sign-language-recognition-trainer)** (alternatives: MediaPipe, OpenPose).
- Output: CSV files containing normalized pose sequences.
- For **Siformer**, sequences are **zero-padded** to a fixed length (max frame count) to enable batch processing. Padding has minimal impact due to attention masking.

### 2. **Visual-Based Model (MViTv2)**
- Use raw RGB video frames directly.
- Frames are sampled uniformly and resized to 224×224 (or 312×312 for larger variants).
- No pose estimation required.

> Preprocessed data for each model should be placed in:
> - `spoter/datasets/`
> - `siformer/datasets/`
> - `mmaction2/data/wl-bisindo/`

---

## 🧠 Model Implementations

### 1. **SPOTER** ([Original Repo](https://github.com/matyasbohacek/spoter/))
- Transformer-based architecture designed for **low-compute** word-level SLR.
- Operates on **pose sequences**.
- Efficient and suitable for edge devices.

**Training example**:
```bash
conda create -n spoter python=3.8
conda activate spoter

python -m train \
  --experiment_name wl_bisindo_spoter_sd \
  --training_set_path spoter/data/train.csv \
  --testing_set_path spoter/data/test.csv \
  --epochs 100 --lr 0.001
```

---

### 2. **Siformer** ([Original Repo](https://github.com/mpuu00001/Siformer/))
- Feature-Isolated Transformer with **input-adaptive inference** (PBEE).
- Supports encoder/decoder attention customization.
- Handles variable-length sequences via padding + attention masking.

**Training example**:
```bash
conda create -n siformer python=3.11
conda activate siformer

python -m train \
  --experiment_name wl_bisindo_siformer_si \
  --training_set_path siformer/datasets/train.csv \
  --testing_set_path siformer/datasets/test.csv \
  --num_classes 32 \
  --epochs 100 --lr 0.0005 \
  --FIM True --PBEE_encoder True
```

---

### 3. **MViTv2** ([MMAction2 Config](https://github.com/open-mmlab/mmaction2/blob/main/configs/recognition/mvit/README.md))
- Multiscale Vision Transformer for **video classification**.
- Uses **raw RGB frames**; no pose required.
- State-of-the-art performance on Kinetics-400.

**Inference example**:
```bash
python tools/test.py \
  configs/recognition/mvit/mvit-small-p244_16x4x1_kinetics400-rgb.py \
  checkpoints/mvit_small_k400.pth \
  --eval top1
```

> You’ll need to adapt the config file for WL-BISINDO (32 classes, custom data path).

---

## 📊 Results Summary

### Signer-Dependent (SD) Setting
| Model     | Modality | Top-1 Accuracy |
|-----------|----------|----------------|
| SPOTER    | Pose     | 93.75%         |
| Siformer  | Pose     | 93.54%         |
| MViTv2    | Visual   | **97.08%**     |

### Signer-Independent (SI) Setting
| Model     | Signer 1 | Signer 2 | Signer 3 | Signer 4 |
|-----------|----------|----------|----------|----------|
| SPOTER    | 84.76%   | 84.28%   | 48.13%   | 75.56%   |
| Siformer  | **90.95%** | **81.90%** | **49.68%** | **78.43%** |

> Siformer consistently outperforms SPOTER in SI settings, demonstrating stronger generalization across unseen signers.

---

## 🙏 Acknowledgements

We sincerely thank **Henry Lucky** for his invaluable supervision and guidance throughout this research. We also extend our deepest gratitude to our sign language contributors—**Marvel, Tazkia, and Kevita**—whose time, expertise, and collaboration were essential to the creation of the WL-BISINDO dataset. Their commitment to supporting sign language research in Indonesia made this work possible.

---

## 📜 License

- **SPOTER code**: [Apache License 2.0](https://github.com/matyasbohacek/spoter/blob/main/LICENSE)  
- **Siformer code**: [MIT License](https://github.com/mpuu00001/Siformer/blob/main/LICENSE)  
- **MViTv2 (MMAction2)**: [Apache License 2.0](https://github.com/open-mmlab/mmaction2/blob/main/LICENSE)  
- **WL-BISINDO dataset**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)  
  > *Non-commercial use only. Attribution required.*

---

## 📚 Citation

If you use WL-BISINDO or reference our baseline methods in your work, please cite:

```bibtex
@article{KINDY2025249,
  title = {Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods},
  journal = {Procedia Computer Science},
  volume = {269},
  pages = {249--258},
  year = {2025},
  note = {The 10th International Conference on Computer Science and Computational Intelligence 2025},
  issn = {1877-0509},
  doi = {10.1016/j.procs.2025.08.277},
  url = {https://www.sciencedirect.com/science/article/pii/S1877050925026225},
  author = {Grace Oktaviani Kindy and Glenn Leonali and Henry Lucky},
  keywords = {Sign Language Recognition, Indonesian Sign Language, BISINDO dataset, Transformer Models, Human Pose Estimation},
  abstract = {The Deaf community in Indonesia, which constitutes 3-4% of the global deaf population, primarily uses Bahasa Isyarat Indonesia (BISINDO), a sign language distinct from Sistem Isyarat Bahasa Indonesia (SIBI). To address the lack of publicly available datasets for BISINDO recognition, this study introduces the Word-Level BISINDO dataset. This dataset contains 1600 RGB videos of 32 isolated signs performed by 5 signers from Banten. Transformer-based models—SPOTER, Siformer, and MViTv2—were implemented and compared using this dataset. Experimental results show that MViTv2 excelled in the signer-dependent (SD) setting with a top-1 accuracy of 97.08%, while Siformer performed best in the signer-independent (SI) setting in 3 out of 4 experiments. This highlights both the robustness of the WL-BISINDO and the strong generalization capability of pose-based models. The WL-BISINDO dataset serves as a foundational resource for research on BISINDO recognition and has the potential to support the development of inclusive sign language technologies in Indonesia.}
}