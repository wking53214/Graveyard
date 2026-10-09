import pandas as pd
import cv2
import os
import numpy as np
from tqdm import tqdm
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops

# Define the file list
test_dir = '/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/train/train/'
files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Initialize storage for 5 features
sobel_vars, lbp_means, glcm_contrasts, glcm_corrs, glcm_homs, ids = [], [], [], [], [], []

for img_file in tqdm(files):
   img_path = os.path.join(test_dir, img_file)
   img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
   
   if img is not None:
       img = cv2.resize(img, (128, 128))
       
       # 1. Sobel Variance
       sobel = cv2.Sobel(img, cv2.CV_64F, 1, 1, ksize=3)
       var = np.var(sobel)
       
       # 2. LBP Texture
       lbp_map = local_binary_pattern(img, P=8, R=1, method='uniform')
       lbp = lbp_map.mean()
       
       # 3. GLCM Features
       img_8bit = (img / 32).astype(np.uint8)
       glcm = graycomatrix(img_8bit, distances=[1], angles=[0], levels=8, symmetric=True, normed=True)
       contrast = graycoprops(glcm, 'contrast')[0, 0]
       correlation = graycoprops(glcm, 'correlation')[0, 0]
       homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
       
       ids.append(img_file.split('.')[0])
       sobel_vars.append(var)
       lbp_means.append(lbp)
       glcm_contrasts.append(contrast)
       glcm_corrs.append(correlation)
       glcm_homs.append(homogeneity)

# Final construction
features = pd.DataFrame({
   'sobel_var': sobel_vars, 
   'lbp_mean': lbp_means,
   'contrast': glcm_contrasts,
   'correlation': glcm_corrs,
   'homogeneity': glcm_homs
}, index=ids)

print(f"Extraction complete. Columns: {features.columns.tolist()}")