import hashlib
import os
from tqdm import tqdm

def get_file_hash(file_path):
   """Calculate the MD5 hash of a file."""
   hasher = hashlib.md5()
   with open(file_path, 'rb') as f:
       # Read in chunks to prevent memory overflow
       for chunk in iter(lambda: f.read(4096), b""):
           hasher.update(chunk)
   return hasher.hexdigest()

def remove_duplicates(directory):
   seen_hashes = set()
   duplicates = []
   
   # Iterate through files
   for root, _, files in os.walk(directory):
       for file in tqdm(files):
           file_path = os.path.join(root, file)
           
           file_hash = get_file_hash(file_path)
           
           if file_hash in seen_hashes:
               duplicates.append(file_path)
           else:
               seen_hashes.add(file_hash)
   
   # Delete duplicates
   for dup in duplicates:
       os.remove(dup)
       print(f"Removed: {dup}")

# Execute
remove_duplicates('/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/train/train/')

# Clear temporary joblib files that often cause semaphore errors
!rm -rf /tmp/joblib_*