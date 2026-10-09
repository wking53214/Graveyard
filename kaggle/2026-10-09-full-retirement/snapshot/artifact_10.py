import os
# Start searching from the base kagglehub directory
base_dir = '/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/'
for root, dirs, files in os.walk(base_dir):
   if 'train' in dirs or 'train_labels.csv' in files:
       print(f"Found potential match at: {root}")

# Updated Configuration Example
train_dir = '/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/train/' # Adjust based on print output
label_path = '/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/train_labels.csv'