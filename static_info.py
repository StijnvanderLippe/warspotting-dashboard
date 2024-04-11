import pandas as pd

# Load data
df_losses = pd.read_csv('data/losses.csv')
df_stats = pd.read_csv('data/stats.csv')

# Preparation for data selection
type_list = ['All'] + sorted(df_losses['type'].unique().tolist())
status_list = ['Any'] + sorted(df_losses['status'].unique().tolist())
unit_list = df_losses['unit'].unique().tolist()
model_list = []

for type in type_list:
    # Extract list of models per vehicle type
    model_list.append(['All'] + sorted(df_losses[df_losses['type'] == type]['model'].unique().tolist()))


# For losses over time
date_range = pd.date_range(df_losses['date'].min(), df_losses['date'].max())

def reindex_dates(date_range, pd_series):
    # Makes sure a pd_series covers a full date_range if certain dates are missing in the pd_series
    # If the series has MultiIndex then it assumes the date is the first level
    if isinstance(pd_series.index, pd.MultiIndex):
        pd_series.index = pd_series.index.set_levels(pd.DatetimeIndex(pd_series.index.levels[0]), level=0)
        pd_series_reindex = pd_series.reindex(pd.MultiIndex.from_product([date_range, pd_series.index.levels[1]], names=pd_series.index.names), fill_value=0)
    else:
        pd_series.index = pd.DatetimeIndex(pd_series.index)
        pd_series_reindex = pd_series.reindex(date_range, fill_value=0)
    return pd_series_reindex