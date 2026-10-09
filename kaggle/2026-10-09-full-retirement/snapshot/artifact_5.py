from google.colab import files

# Triggers the browser's download prompt for the specified file
files.download('submission_final.csv')

import os

if os.path.exists('submission_final.csv'):
   print("File found. Triggering download...")
   files.download('submission_final.csv')
else:
   print("Error: 'submission_final.csv' not found. Ensure the export code was executed.")