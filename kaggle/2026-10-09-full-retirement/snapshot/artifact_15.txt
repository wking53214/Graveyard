def get_file_hash(file_path):
   hasher = hashlib.md5()
   with open(file_path, 'rb') as f:
       for chunk in iter(lambda: f.read(4096), b""):
           hasher.update(chunk)
   return hasher.hexdigest()

def remove_duplicates(directory):
   seen_hashes = set()
   duplicates = []
   for root, , files in os.walk(directory):
       for file in tqdm(files):
           file_path = os.path.join(root, file)
           file_hash = get_file_hash(file_path)
           if file_hash in seen_hashes:
               duplicates.append(file_path)
           else:
               seen_hashes.add(file_hash)
   for dup in duplicates:
       os.remove(dup)
       print(f"Removed: {dup}")

!rm -rf /tmp/joblib*
files.download('submission_final.csv')
