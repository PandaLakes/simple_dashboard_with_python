from bokeh.io import curdoc
from data_processing import load_and_clean_data
from dashboard import create_dashboard

sales_df, feedback_df, geo_df = load_and_clean_data()

dashboard = create_dashboard(sales_df, feedback_df, geo_df)

curdoc().add_root(dashboard)
curdoc().title = "Sales Performance Dashboard"