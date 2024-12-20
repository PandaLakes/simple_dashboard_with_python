from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, NumeralTickFormatter, LinearColorMapper, WMTSTileSource
from bokeh.transform import cumsum, factor_cmap, linear_cmap
from bokeh.palettes import Viridis256
import numpy as np


def create_sales_trend(sales_df):
    daily_sales = sales_df.groupby('date')['sales'].sum().reset_index()
    source = ColumnDataSource(daily_sales)

    # Define the figure
    p = figure(
        x_axis_type='datetime',
        height=400, width=800,
        background_fill_color="#ffffff",  # White for a clean look
        tooltips=[
            ("Date", "@date{%F}"),
            ("Sales (€)", "@sales{0,0.00}")
        ],
        toolbar_location="above"
    )

    # Updated line color to a vibrant orange
    p.line('date', 'sales', line_width=3, source=source, color="#FF4500", legend_label="Sales (€)")  # Vibrant Orange

    # Add axis labels
    p.xaxis.axis_label = 'Date'
    p.xaxis.axis_label_text_font_size = "12pt"
    p.xaxis.axis_label_text_color = "#4B0082"  # Indigo for a modern look
    p.yaxis.axis_label = 'Total Sales (€)'
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_color = "#4B0082"

    # Formatters for axis ticks
    p.yaxis.formatter = NumeralTickFormatter(format="0.0a")  # Shortened format like 100k, 200k

    # Hover tool interactivity
    hover = HoverTool(
        tooltips=[
            ("Date", "@date{%F}"),
            ("Sales (€)", "@sales{0,0.00}")
        ],
        formatters={"@date": "datetime"},
        mode="vline"
    )
    p.add_tools(hover)

    # Legend customization
    p.legend.location = "top_left"
    p.legend.label_text_font_size = "10pt"
    p.legend.background_fill_alpha = 0.7
    p.legend.background_fill_color = "#FFFFE0"  # Light Yellow

    # Gridline and axis enhancements
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_dash = [6, 4]  # Dashed gridlines
    p.grid.grid_line_alpha = 0.3  # Lighter gridlines for aesthetics

    return p


def create_sales_bar(sales_df):
    category_sales = sales_df.groupby('category')['sales'].sum().reset_index()
    source = ColumnDataSource(category_sales)

    # Colors matching the uploaded image
    colors = ['#FFA500', '#9370DB', '#87CEEB', '#FF4500', '#32CD32']  # Vibrant orange, purple, blue, red, green
    categories = category_sales['category']

    p = figure(x_range=categories,
               height=400, width=800,
               background_fill_color="#FFFFFF")  # White background

    p.vbar(x='category', top='sales', width=0.8, source=source,
           fill_color=factor_cmap('category', palette=colors, factors=categories))

    # Adding axis labels
    p.xaxis.axis_label = 'Categories'
    p.xaxis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label = 'Ventes (€)'
    p.yaxis.axis_label_text_font_style = "bold"

    # Remove grid lines for a clean look
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # Ajout d'une interactivité au survol
    hover = HoverTool(tooltips=[("Catégorie", "@category"),
                                ("Ventes", "@sales{0,0.00} €")])
    p.add_tools(hover)
    # Format Y-axis labels to display in 'k' notation
    p.yaxis.formatter = NumeralTickFormatter(format="0.0a")  # e.g., 100k, 200k

    return p


def create_sales_heatmap(sales_df):

    heatmap_data = sales_df.groupby(['day_of_week', 'category'])['sales'].sum().unstack(fill_value=0)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = heatmap_data.reindex(days)  # Ensure the order of days of the week

    source = ColumnDataSource(heatmap_data.reset_index().melt(id_vars='day_of_week', var_name='category', value_name='sales'))

    p = figure(
               x_range=list(heatmap_data.columns),
               y_range=list(reversed(days)),
               height=400, width=800,
               toolbar_location=None, tools="",
               background_fill_color="#ffffff")  # White background for a clean look

    # Updated vibrant color palette
    vibrant_palette = ['#fff7bc', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#993404']
    mapper = linear_cmap(field_name='sales', palette=vibrant_palette, low=heatmap_data.values.min(), high=heatmap_data.values.max())

    p.rect(x='category', y='day_of_week', width=1, height=1, source=source,
           line_color=None, fill_color=mapper)

    hover = HoverTool(tooltips=[("Day", "@day_of_week"),
                                ("Category", "@category"),
                                ("Sales", "@sales{0,0.00} €")])
    p.add_tools(hover)

    # Adding a color bar for the vibrant color scheme
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0, 0))
    p.add_layout(color_bar, 'right')

    # Updated axis labels
    p.xaxis.axis_label = 'Category'
    p.xaxis.axis_label_text_color = "#4B0082"  # Indigo
    p.yaxis.axis_label = 'Day of the Week'
    p.yaxis.axis_label_text_color = "#4B0082"

    return p


def create_geographic_visualization(geo_df):

    # Step 1: Aggregate sales by region
    aggregated_df = geo_df.groupby('region').agg({
        'sales': 'sum',  # Sum of sales
        'latitude': 'mean',  # Average latitude
        'longitude': 'mean'  # Average longitude
    }).reset_index()
    
    # Calculate Mercator coordinates and proportional size
    aggregated_df['x'] = aggregated_df['longitude'] * (20037508.34 / 180)
    aggregated_df['y'] = np.log(np.tan((90 + aggregated_df['latitude']) * np.pi / 360)) * (20037508.34 / np.pi)
    aggregated_df['size'] = aggregated_df['sales'] / aggregated_df['sales'].max() * 50  # Proportional size

    # Data source for Bokeh
    source = ColumnDataSource(aggregated_df)

    # Map tile source
    tile_source = WMTSTileSource(url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{Z}/{X}/{Y}.png")

    # Step 2: Create the figure
    p = figure(
        x_axis_type=None, y_axis_type=None,
        height=400, width=800,
        background_fill_color="#ffffff",  # White for a clean background
        tooltips=[
            ("Region", "@region"),
            ("Total Sales", "@sales{0,0.00} €"),
            ("Latitude", "@latitude"),
            ("Longitude", "@longitude"),    
        ]
    )

    p.add_tile(tile_source)

    # Add scatter points with a vibrant color palette
    vibrant_palette = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#f03b20', '#bd0026']  # Light to dark yellow-orange-red
    color_mapper = LinearColorMapper(palette=vibrant_palette, low=aggregated_df['sales'].min(), high=aggregated_df['sales'].max())
    p.scatter(x='x', y='y', size='size', fill_color={'field': 'sales', 'transform': color_mapper},
              fill_alpha=0.8, line_color=None, source=source)

    # Add a color bar
    color_bar = ColorBar(color_mapper=color_mapper, width=8, location=(0, 0), 
                         title="Sales (€)", title_text_font_size="10pt")
    p.add_layout(color_bar, 'right')

    # Add axis labels
    p.xaxis.axis_label = 'Longitude'
    p.xaxis.axis_label_text_color = "#4B0082"  # Indigo for a vibrant label
    p.yaxis.axis_label = 'Latitude'
    p.yaxis.axis_label_text_color = "#4B0082"

    return p


def create_sales_pie(sales_df):
    # Group data by category and calculate angles and colors
    category_sales = sales_df.groupby('category')['sales'].sum().reset_index()
    category_sales['angle'] = category_sales['sales'] / category_sales['sales'].sum() * 2 * np.pi
    
    # Vibrant color palette for the pie chart
    vibrant_colors = ["#FFA07A", "#20B2AA", "#FFD700", "#FF6347", "#40E0D0", "#9370DB", "#FF4500", "#32CD32"][:len(category_sales)]
    category_sales['color'] = vibrant_colors

    source = ColumnDataSource(category_sales)

    # Create the figure
    p = figure(
        height=400, width=500, toolbar_location=None, tools="hover",
        tooltips="@category: @sales{0,0.00} €",
        x_range=(-0.5, 1.0)
    )

    # Draw the pie chart
    p.wedge(
        x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), 
        end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='category', source=source
    )

    # Remove grid and axis for a clean appearance
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # Customize legend
    p.legend.label_text_font_size = "10pt"
    p.legend.background_fill_alpha = 0.7
    p.legend.background_fill_color = "#f8f8ff"  # Light gray for the legend background
    p.legend.border_line_width = 0

    return p


def create_feedback_distrubution_per_category(feedback_df):
    category_counts = feedback_df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    source = ColumnDataSource(category_counts)

    p = figure(
        title="Feedback Count by Product Category",
        x_range=category_counts['category'],
        height=400, width=800,
        background_fill_color="#ffffff"
    )
    p.vbar(
        x='category', top='count', width=0.8,
        source=source,
        fill_color=factor_cmap('category', palette=["#FFA500", "#20B2AA", "#FFD700", "#FF6347", "#40E0D0", "#9370DB", "#FF4500", "#32CD32"], factors=category_counts['category']),
        line_color="white"
    )

    p.xaxis.axis_label = "Category"
    p.yaxis.axis_label = "Feedback Count"
    p.yaxis.formatter = NumeralTickFormatter(format="0")
    p.xgrid.grid_line_color = None
    p.add_tools(HoverTool(tooltips=[("Category", "@category"), ("Count", "@count")]))

    return p

def create_avg_sentiment_bar(feedback_df):
    avg_sentiment = feedback_df.groupby('category')['sentiment_score'].mean().reset_index()
    avg_sentiment.columns = ['category', 'avg_sentiment']
    source = ColumnDataSource(avg_sentiment)

    p = figure(
        x_range=avg_sentiment['category'],
        height=400, width=800,
        background_fill_color="#ffffff"
    )
    p.vbar(
        x='category', top='avg_sentiment', width=0.8,
        source=source,
        fill_color=factor_cmap('category', palette=["#FFA07A", "#20B2AA", "#FFD700", "#FF6347", "#40E0D0", "#9370DB", "#FF4500", "#32CD32"], factors=avg_sentiment['category']),
        line_color="white"
    )

    p.xaxis.axis_label = "Category"
    p.yaxis.axis_label = "Average Sentiment Score"
    p.yaxis.formatter = NumeralTickFormatter(format="0.0")
    p.xgrid.grid_line_color = None
    p.add_tools(HoverTool(tooltips=[("Category", "@category"), ("Avg Sentiment", "@avg_sentiment{0.00}")]))

    return p