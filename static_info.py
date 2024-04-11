import pandas as pd

# Load data
df_losses = pd.read_csv('data/losses.csv')
df_stats = pd.read_csv('data/stats.csv')

# Preparation for data selection
type_list = ['All'] + df_losses['type'].unique().tolist()
status_list = df_losses['status'].unique().tolist()
unit_list = df_losses['unit'].unique().tolist()
model_list = []

for type in type_list:
    # Extract list of models per vehicle type
    model_list.append(['All'] + df_losses[df_losses['type'] == type]['model'].unique().tolist())


# For losses over time
date_range = pd.date_range(df_losses['date'].min(), df_losses['date'].max())

def reindex_dates(date_range, pd_series):
    pd_series.index = pd.DatetimeIndex(pd_series.index)
    pd_series_reindex = pd_series.reindex(date_range, fill_value=0)
    return pd_series_reindex