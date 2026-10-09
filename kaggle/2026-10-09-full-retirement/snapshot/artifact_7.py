# Re-run your full extraction loop here
# Once this cell finishes and prints the column list, 'features' will be defined.

# 1. Load labels
train_labels_df = pd.read_csv('/root/.cache/kagglehub/competitions/the-freuid-challenge-2026-ijcai-ecai/train_labels.csv')
train_labels_df = train_labels_df.set_index('id')

# 2. Sync labels to the features you just extracted
target = train_labels_df.loc[features.index]['label']

# 3. Verify
print(f"Features: {type(features)}, Target: {type(target)}")

model.fit(features[features.columns], target)