# India Geographic Data Visualization Dashboard

This is a Dash-based interactive dashboard for visualizing Indian demographic data across states and districts.

## Features
- Choropleth maps of India and states
- District-level analytics
- Multi-panel layout with beautiful charts
- Correlation, ranking, and AI insights

## How to Run

1. Install dependencies:
    ```sh
    pip install dash pandas plotly
    ```

2. Run the app:
    ```sh
    python newlatest.py
    ```
    The dashboard will be available at [http://127.0.0.1:8050](http://127.0.0.1:8050).

## File Structure

```
project661/
├── newlatest.py                # Main application file
├── *.geojson                   # State boundary files
├── india.json                  # National boundary data
├── districtwise_data_percentages.csv   # Demographic data
└── ...                         # Other supporting files
```

## Notes
- All code runs from `newlatest.py`.
- Data files must be present in the same directory.
