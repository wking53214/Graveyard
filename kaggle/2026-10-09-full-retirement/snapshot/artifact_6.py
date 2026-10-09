import lightgbm as lgb

# 1. Re-initialize the model with the best parameters identified
model = lgb.LGBMClassifier(
   n_estimators=1500,
   learning_rate=0.03,
   num_leaves=63,
   feature_fraction=0.8,
   bagging_fraction=0.8,
   bagging_freq=5,
   objective='binary'
)

# 2. Retrain the model using your constructed 'features' matrix and 'target' labels
model.fit(features[features.columns], target)

# 3. Now you can safely run predictions
test_preds = model.predict_proba(test_features[features.columns])[:, 1]

import joblib

# Save the model
joblib.dump(model, 'lgbm_model_v1.pkl')

# Reload the model in a new session
model = joblib.load('lgbm_model_v1.pkl')