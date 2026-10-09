import kagglehub
import os
import shutil

# 1. Download to the system-managed path
# This returns the absolute path automatically
path = kagglehub.competition_download('the-freuid-challenge-2026-ijcai-ecai')

# 2. Define the path variables dynamically
# This approach works regardless of whether the files are in 'train/train' or just 'train'
train_dir = os.path.join(path, 'train') 
# Check if a nested directory exists
if os.path.exists(os.path.join(train_dir, 'train')):
   train_dir = os.path.join(train_dir, 'train')

label_path = os.path.join(path, 'train_labels.csv')

print(f"Images will be pulled from: {train_dir}")
print(f"Labels will be pulled from: {label_path}")

# 3. Verification
files = [f for f in os.listdir(train_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Found {len(files)} image files.")