import pandas as pd

# Load data
df_losses = pd.read_csv('data/losses.csv')
df_stats = pd.read_csv('data/stats.csv')

# Preparation for data selection
type_list = df_losses['type'].unique().tolist()
status_list = df_losses['status'].unique().tolist()
unit_list = df_losses['unit'].unique().tolist()
model_list = []

for type in type_list:
    # Extract list of models per vehicle type
    model_list.append(df_losses[df_losses['type'] == type]['model'].unique().tolist())