import os
import json
import shutil
import argparse

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def organize_dataset(metadata_path, source_dir, output_dir):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    # Create train/test directories for each label
    for split in ['train', 'test']:
        for label in range(10):  # adjust based on total number of classes
            ensure_dir(os.path.join(output_dir, split, str(label)))

    # Move files
    for class_info in metadata:
        label = class_info['label']
        for instance in class_info['instances']:
            video_id = instance['video_id']
            split = instance['split']

            src_path = os.path.join(source_dir, video_id)
            dest_path = os.path.join(output_dir, split, str(label), video_id)

            if os.path.exists(src_path):
                shutil.copy(src_path, dest_path)  # Use shutil.copy() if you prefer
                print(f"Moved {video_id} → {dest_path}")
            else:
                print(f"⚠️ File not found: {src_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Organize dataset based on metadata")
    parser.add_argument('--metadata', type=str, required=True,
                        help='Path to metadata JSON file (metadata_by_label.json or metadata_by_signer.json)')
    parser.add_argument('--source', type=str, required=True,
                        help='Directory containing all video files')
    parser.add_argument('--output', type=str, default='dataset',
                        help='Output directory for organized dataset')

    args = parser.parse_args()

    organize_dataset(args.metadata, args.source, args.output)