import pandas as pd

def load_and_clean_data():
    sales_df = pd.read_csv('sales_data.csv')
    feedback_df = pd.read_csv('customer_feedback.csv')
    geo_df = pd.read_csv('geographic_data.csv')

    # Clean sales data
    sales_df['date'] = pd.to_datetime(sales_df['date'], format='%Y-%m-%d')
    sales_df['category'] = sales_df['category'].astype(str)
    sales_df['sales'] = sales_df['sales'].astype(float)
    sales_df['units'] = sales_df['units'].astype(int)
    sales_df['day_of_week'] = sales_df['date'].dt.day_name()

    # Clean feedback data
    feedback_df['date'] = pd.to_datetime(feedback_df['date'], format='%Y-%m-%d')
    feedback_df['category'] = feedback_df['category'].astype(str)
    feedback_df['rating'] = feedback_df['rating'].astype(int)
    feedback_df['sentiment_score'] = feedback_df['sentiment_score'].astype(float)
    feedback_df['verified_purchase'] = feedback_df['verified_purchase'].astype(bool)

    # Clean geo data
    geo_df['region'] = geo_df['region'].astype(str)
    geo_df['sales'] = geo_df['sales'].astype(float)
    geo_df['latitude'] = geo_df['latitude'].astype(float)
    geo_df['longitude'] = geo_df['longitude'].astype(float)

    return sales_df, feedback_df, geo_df