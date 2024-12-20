from bokeh.layouts import column
from bokeh.models import Tabs, TabPanel, Div
from visualizations import create_sales_trend, create_sales_bar, create_sales_heatmap, create_geographic_visualization, create_sales_pie, create_feedback_distrubution_per_category, create_avg_sentiment_bar


def create_dashboard(sales_df, feedback_df, geo_df):
    # Generate plots
    sales_trend_plot = create_sales_trend(sales_df)
    sales_bar_plot = create_sales_bar(sales_df)
    sales_heatmap_plot = create_sales_heatmap(sales_df)
    geo_plot = create_geographic_visualization(geo_df)
    sales_pie_plot = create_sales_pie(sales_df)
    feedback_distribution_plot = create_feedback_distrubution_per_category(feedback_df)
    avg_sentiment_plot = create_avg_sentiment_bar(feedback_df)

    # Create Tabs
    tab1 = TabPanel(child=sales_trend_plot, title="Sales Trend")
    tab2 = TabPanel(child=sales_bar_plot, title="Sales by Category")
    tab3 = TabPanel(child=sales_heatmap_plot, title="Sales Heatmap")
    tab4 = TabPanel(child=geo_plot, title="Geographic Sales")
    tab5 = TabPanel(child=sales_pie_plot, title="Sales Pie Chart")
    tab6 = TabPanel(child=feedback_distribution_plot, title="Feedback Distribution")
    tab7 = TabPanel(child=avg_sentiment_plot, title="Average Sentiment")

    # Combine tabs into a single layout
    tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7])

    # Add a title
    title = Div(text="<h1>Sales Performance Dashboard</h1>", width=800)

    # Create final layout

    return column(title, tabs)