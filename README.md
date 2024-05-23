# Visualising Russian losses in the Russo-Ukrainian war

This repository provides a dashboard that can be used to visualise Russian losses in the Russo-Ukrainian war. The data used is gathered by volunteers at [WarSpotting](https://ukr.warspotting.net), who are doing important work in documenting the enormous scale of losses in this war.


## Examples

![A pie chart](/images/pie_chart.png)
*A pie chart displaying the distribution of self-propelled artillery losses.*

![Counts of losses over time](/images/losses_over_time.png)
*A graph displaying the count of tanks lost over time.*

![Satellite image of Berdiansk airport](/images/map.png)
*A satellite image of Berdiansk airport showing damaged and destroyed helicopters as a result of Ukrainian strike using cluster munitions.*


## Usage

###  Acquiring the data

There are two ways to acquire the data files that are used in the dashboard.

1. Run all cells in `get_data.ipynb`, which stores the files in `./data/`
2. Download `losses.csv` and `stats.csv` from this repository and store in `./data/`

### Using the dashboard

After the necessary data files have been acquired, run `dashboard.py`. This will start app and can then be accessed at localhost:8050.

As a first step you can narrow down what data is being displayed. This includes the type of vehicle loss, the model for that type of vehicle, and additionally the status of the loss (abandoned, captured, damaged, or destroyed).

Based on the selection a pie chart is generated that displays the distribution of models lost for the selected type of vehicle (or in the case of all types being selected the distribution of losses across the different types of vehicles). Next to this a graph displays the losses over time since the start of the full scale invasion (February 24, 2022), up until the most recent data point. Here a distinction is made based on the status of the lost vehicle. Finally, a map displays where the vehicles were lost, if the information is available. The marker colour depends on the status of the lost vehicle. Clicking on a marker displays the status and the type of the lost vehicle.


## Requirements

* pandas
* dash
* dash_bootstrap_components
* plotly.express
* folium

## Credits and attributions

* Data is gathered by volunteers at [WarSpotting](https://ukr.warspotting.net) and acquired through their [API](https://ukr.warspotting.net/api/docs/)
* Satellite imagery: &copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')