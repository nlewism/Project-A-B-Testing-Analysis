import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def load_data():
    # Uploading dataset
    client_profiles_url = "https://drive.google.com/file/d/1othytDxreOzauaFFvDVmt-4FLUU7VlC0/view?usp=drive_link"
    df_web_data_pt1_url = "https://drive.google.com/file/d/1qBcLr5zxWFZVbbM86eI9wpJ2iaaHeLnF/view?usp=drive_link"
    df_web_data_pt2_url = "https://drive.google.com/file/d/1--nFdgEJRICu2fE8gLC1TXHKQag9UKv3/view?usp=drive_link"
    experiment_roster_url = "https://drive.google.com/file/d/1_aWfob1QiKDvZd8hfkbcJ-T69ZTECLqw/view?usp=drive_link"
    
    client_profiles = pd.read_csv('https://drive.google.com/uc?id=' + client_profiles_url.split('/')[-2])
    df_web_data_pt1 = pd.read_csv('https://drive.google.com/uc?id=' + df_web_data_pt1_url.split('/')[-2])
    df_web_data_pt2 = pd.read_csv('https://drive.google.com/uc?id=' + df_web_data_pt2_url.split('/')[-2])
    experiment_roster = pd.read_csv('https://drive.google.com/uc?id=' + experiment_roster_url.split('/')[-2])
    
    df_web_data_pt1['date_time'] = pd.to_datetime(df_web_data_pt1['date_time'])
    df_web_data_pt2['date_time'] = pd.to_datetime(df_web_data_pt2['date_time'])
    digital_footprints = pd.merge(df_web_data_pt1,df_web_data_pt2, on='client_id')
    client_footprints = pd.merge(client_profiles, digital_footprints, on='client_id', how='inner')
    grouped_data = pd.merge(client_footprints, experiment_roster, on='client_id', how='inner')
    return client_profiles, df_web_data_pt1, df_web_data_pt2, experiment_roster, digital_footprints, client_footprints, grouped_data


# def merging_datasets(client_profiles, digital_footprints):
#     client_footprints = pd.merge(client_profiles, digital_footprints, on='client_id', how='inner')
#     grouped_data = pd.merge(client_footprints, experiment_roster, on='client_id', how='inner')
#     
#     return grouped_data

# def get_summary(data):
#     summary = pd.DataFrame({
#         'Total Sales': [data['Total'].sum()],
#         'Average Rating': [data['Rating'].mean()],
#         'Total Transactions': [data['Invoice ID'].nunique()]
#     })
#     return summary
# 
# def plot_sales_over_time(data):
#     data['Date'] = pd.to_datetime(data['Date'])
#     sales_over_time = data.groupby(data['Date'].dt.date)['Total'].sum()
#     plt.figure(figsize=(10, 5))
#     plt.plot(sales_over_time.index, sales_over_time.values)
#     plt.title('Sales Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Total Sales')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     st.pyplot(plt)