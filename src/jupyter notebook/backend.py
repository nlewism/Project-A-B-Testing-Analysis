import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency

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
    experiment_roster.dropna(inplace=True)
    
    df_web_data_pt1['date_time'] = pd.to_datetime(df_web_data_pt1['date_time'])
    df_web_data_pt2['date_time'] = pd.to_datetime(df_web_data_pt2['date_time'])
    web_group = pd.concat([df_web_data_pt1,df_web_data_pt2])
    process_dict = {'start': 0, 'step_1': 1, 'step_2': 2, 'step_3': 3, 'confirm': 4}
    web_group['process_step'] = web_group['process_step'].replace(process_dict)

    digital_footprints = pd.merge(df_web_data_pt1,df_web_data_pt2, on='client_id')
    
    client_footprints = pd.merge(client_profiles, digital_footprints, on='client_id', how='inner')
    
    grouped_data = pd.merge(client_footprints, experiment_roster, on='client_id', how='inner')
    
    return client_profiles, experiment_roster, web_group, digital_footprints, client_footprints, grouped_data

def data_wrangling(web_group,experiment_roster,client_profiles):
    
    client_process_counts = web_group.groupby('client_id')['process_step'].value_counts().unstack(fill_value=0)
    client_process_column_rename = {0: 'start', 1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'confirm'}
    client_process_counts = client_process_counts.rename(columns=client_process_column_rename)
    
    final_rooster_process_counts = pd.merge(client_process_counts, experiment_roster, on='client_id', how='inner')
    final_rooster_process_counts_profile = pd.merge(final_rooster_process_counts, client_profiles, on='client_id', how='inner')
    
    control_profile_df = final_rooster_process_counts_profile[final_rooster_process_counts_profile['Variation'] == 'Control']
    test_profile_df = final_rooster_process_counts_profile[final_rooster_process_counts_profile['Variation'] == 'Test']
    
    web_group_experiment = pd.merge(web_group, experiment_roster, on='client_id', how='inner')
    
    client_profile_experiment = pd.merge(web_group_experiment, client_profiles, on='client_id', how='left')

    return client_process_counts, final_rooster_process_counts_profile, control_profile_df, test_profile_df, web_group_experiment, client_profile_experiment
 
    
    
def calculate_completion_rate(data,variation=None):

    if (variation == 'Test') or (variation == 'Control'):
        variation_df = data[data['Variation']== variation]
        confirm_step_users = variation_df[variation_df['process_step'] == 4]['client_id'].nunique()
        total_users = variation_df['client_id'].nunique()
        
    else:
        confirm_step_users = data[data['process_step'] == 4]['client_id'].nunique()
        total_users = data['client_id'].nunique()

    completion_rate_percentage = (confirm_step_users / total_users) * 100

    return completion_rate_percentage
   
    
    
def calculate_avg_time_per_step(data,variation=None):
    
    merged_web_data = data.sort_values(by=['client_id', 'date_time'])

    merged_web_data['time_diff'] = merged_web_data.groupby('client_id')['date_time'].diff()
    
    merged_web_data = merged_web_data[merged_web_data['process_step'] != 0]
    
    merged_web_data_test = merged_web_data[merged_web_data['Variation']=='Test']
    
    merged_web_data_control = merged_web_data[merged_web_data['Variation']=='Control']
    
    index_rename = {1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'confirm'}
    
    if variation == 'Control':
        
        average_time_per_step_control = merged_web_data_control.groupby('process_step')['time_diff'].mean()

        average_time_per_step_control = average_time_per_step_control.rename(index=index_rename)
        
        return average_time_per_step_control
    
    elif variation == 'Test':
        
        average_time_per_step_test = merged_web_data_test.groupby('process_step')['time_diff'].mean()
        
        average_time_per_step_test = average_time_per_step_test.rename(index=index_rename)
        
        return average_time_per_step_test
            
    elif variation == 'Overall':

        avg_time_per_step = merged_web_data.groupby('process_step')['time_diff'].mean()
        
        avg_time_per_step = avg_time_per_step.rename(index=index_rename)
        
        return avg_time_per_step
    
    else:
        
        average_time_per_step_control = merged_web_data_control.groupby('process_step')['time_diff'].mean()
        
        average_time_per_step_control = average_time_per_step_control.rename(index=index_rename)
        
        average_time_per_step_test = merged_web_data_test.groupby('process_step')['time_diff'].mean()
        
        average_time_per_step_test = average_time_per_step_test.rename(index=index_rename)
        
        avg_time_per_step = merged_web_data.groupby('process_step')['time_diff'].mean()
        
        avg_time_per_step = avg_time_per_step.rename(index=index_rename)
        
        
        return average_time_per_step_control, average_time_per_step_test, avg_time_per_step

def error_rate(data):
    
    error_df = data.sort_values(by=['client_id', 'date_time'])
    
    
    error_mask = error_test_1.groupby('client_id')['process_step'].shift(1) > error_test_1['process_step']
    
    
    total_errors = error_mask.sum()
    
    
    total_steps = error_test_1.shape[0]
    
    
    error_rate = total_errors / total_steps *100
    
    
    average_error_per_step = error_mask.groupby(data['process_step']).mean()*100
    
    
    return total_errors, total_steps, error_rate, average_error_per_step


def drop_off_rate(data):

    drop_off_rate = data.sort_values(by=['client_id', 'date_time'])


    dropoff_rates = []
    
    for step in range(drop_off_test_4['process_step'].max() + 1):
        total_clients_at_step = drop_off_test_4[drop_off_test_4['process_step'] == step]['client_id'].nunique()
        
        if step < drop_off_test_4['process_step'].max():
            next_step_clients = drop_off_test_4[drop_off_test_4['process_step'] == step + 1]['client_id'].unique()
            dropped_off_clients = total_clients_at_step - len(next_step_clients)
        else:
            dropped_off_clients = 0
        
        dropoff_rate = dropped_off_clients / total_clients_at_step *100
        dropoff_rates.append({'process_step': step, 'dropoff_rate': dropoff_rate})
    
    
    dropoff_df = pd.DataFrame(dropoff_rates)
    
    
    return dropoff_df



def statistic_func(data, evaluator, stat_test, alpha):
    
    
    if evaluator == 'age':
        column = 'clnt_age'
        
    elif evaluator == 'tenure years':
        column = 'clnt_tenure_yr'
    
    elif evaluator == 'tenure months':
        column = 'clnt_tenure_mnth'
        
    elif evaluator == 'gender':
        column = 'gendr'
        
    elif evaluator == 'number of accounts':
        column = 'num_accts'
        
    elif evaluator == 'balance':
        column = 'bal'
    
    elif evaluator == 'calls in the last 6 months':
        column = 'calls_6_mnth'
    
    elif evaluator == 'logins in the last 6 months':
        column = 'logons_6_mnth'
    
    
    if stat_test == 't-test':
        
        control_group_data = data[data['Variation'] == 'Control'][column].dropna()

        test_group_data = data[data['Variation'] == 'Test'][column].dropna()

        t_statistic, p_value = ttest_ind(control_group_data, test_group_data, equal_var=False)


        if p_value < alpha:
            hypothesis_string = (f"Reject the null hypothesis: There is a significant difference in the average {evaluator} between the Control and Test groups.")
        else:
            hypothesis_string = (f"Fail to reject the null hypothesis: There is no significant difference in the average {evaluator} between the Control and Test groups.")
        
        
        print(f"T-statistic: {t_statistic:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(hypothesis_string)
        
        return t_statistic, p_value, hypothesis_string

    
    elif stat_test == 'chi-test':

        contingency_table = pd.crosstab(data['Variation'], data[column])
        
        chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        
   
        if p_value < alpha:
            hypothesis_string = (f"Reject the null hypothesis: There is a significant difference in the proportion of clients engaging with the new process across different {evaluator} categories.")
        else:
            hypothesis_string = (f"Fail to reject the null hypothesis: There is no significant difference in the proportion of clients engaging with the new process across different {evaluator} categories.")
        
        print(f"Chi-square statistic: {chi2_stat:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(hypothesis_string)
        
        return chi2_stat, p_value, hypothesis_string
    
    else:
        
        control_group_data = data[data['Variation'] == 'Control']

        test_group_data = data[data['Variation'] == 'Test']
        
        users_at_last_step_control = control_group_data[control_group_data['process_step'] == 4]['client_id'].nunique()
        
        users_at_last_step_test = test_group_data[test_group_data['process_step'] == 4]['client_id'].nunique()
        
        total_users_control = control_group_data['client_id'].nunique()
        
        total_users_test = test_group_data['client_id'].nunique()
        
        count = [users_at_last_step_control, users_at_last_step_test]
        nobs = [total_users_control, total_users_test]
        
        if stat_test == 'two-proportion z-test':
            
            stat, p_value = proportions_ztest(count, nobs)
            
            if p_value < alpha:
                hypothesis_string = ("Reject the null hypothesis: There is evidence that completion rates are different.")
            else:
                hypothesis_string = ("Fail to reject the null hypothesis: There is no significant evidence that completion rates are different.")
                
            print(f"Z-statistic: {stat}")
            print(f"P-value: {p_value}")
            print(hypothesis_string)
            
            return stat, p_value, hypothesis_string
        
        else:
        
            stat, p_value = proportions_ztest(count, nobs, alternative='larger')
            
            
            if p_value < alpha:
                hypothesis_string = ("Reject the null hypothesis: The completion rate for the Test group is greater than the Control group increased by 5%.")
            else:
                hypothesis_string = ("Fail to reject the null hypothesis: There is no significant evidence that the completion rate for the Test group is greater than the Control group increased by 5%.")
                
            print(f"Z-statistic: {stat:.4f}")
            print(f"P-value: {p_value:.4f}")
            print(hypothesis_string)
            
            return stat, p_value, hypothesis_string
    
    

    
    
    
    

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