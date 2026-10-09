# Verify your new feature matrix dimensions
print(f"Features updated to shape: {features.shape}")
# It should now have 5 columns: sobel_var, lbp_mean, contrast, correlation, homogeneity

model = lgb.LGBMClassifier(
   n_estimators=1500,
   learning_rate=0.03,
   num_leaves=63,
   feature_fraction=0.8,
   bagging_fraction=0.8,
   bagging_freq=5,
   objective='binary'
)

model.fit(
   X_train, y_train,
   eval_set=[(X_val, y_val)],
   eval_metric='binary_logloss',
   callbacks=[lgb.early_stopping(stopping_rounds=100)]
)