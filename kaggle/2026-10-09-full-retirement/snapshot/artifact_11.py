import os
# Search the root path to find the correct data structure
search_path = '/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/'

found = False
for root, dirs, files in os.walk(search_path):
   # Look for a directory containing images
   if any(f.endswith(('.png', '.jpg', '.jpeg')) for f in files):
       print(f"Data found at: {root}")
       train_dir = root
       found = True
       break

if not found:
   print("No image files found in the path. Check if the download completed.")

# Replace the path with the one discovered by the search above
train_dir = 'PASTE_THE_PATH_HERE/' 
label_path = os.path.join(search_path, 'train_labels.csv')

# Verify the file list
files = [f for f in os.listdir(train_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Successfully loaded {len(files)} files.")

import kagglehub
path = kagglehub.competition_download('the-freuid-challenge-2026-ijcai-ecai')
print(f"Path: {path}")