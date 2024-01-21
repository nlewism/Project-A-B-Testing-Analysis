import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
from matplotlib import colormaps


def load_data():
    
    # Uploading dataset
    client_profiles = pd.read_csv('https://raw.githubusercontent.com/nlewism/A-B-Customer-Analysis/Natalie/data/raw/df_final_demo.csv')
    
    df_web_data_pt1 = pd.read_csv('https://raw.githubusercontent.com/nlewism/A-B-Customer-Analysis/Natalie/data/raw/df_final_web_data_pt_1.csv')
    
    df_web_data_pt2 = pd.read_csv('https://raw.githubusercontent.com/nlewism/A-B-Customer-Analysis/Natalie/data/raw/df_final_web_data_pt_2.csv')
    
    experiment_roster = pd.read_csv('https://raw.githubusercontent.com/nlewism/A-B-Customer-Analysis/Natalie/data/raw/df_final_experiment_clients.csv')
    experiment_roster.dropna(inplace=True)
    
    # Transforms date_time column into datetime format.
    df_web_data_pt1['date_time'] = pd.to_datetime(df_web_data_pt1['date_time'])
    df_web_data_pt2['date_time'] = pd.to_datetime(df_web_data_pt2['date_time'])
    
    # Concatenates the web data from the clients.
    # Since there was too much data, original dataset was divided in two.
    # Now we combinbe them to view the data as a whole.
    web_group = pd.concat([df_web_data_pt1,df_web_data_pt2])
    
    # Replacing process step with numerical values to help us analyze how customers moved from one step to another.
    process_dict = {'start': 0, 'step_1': 1, 'step_2': 2, 'step_3': 3, 'confirm': 4}
    web_group['process_step'] = web_group['process_step'].replace(process_dict)
    
    
    return client_profiles, experiment_roster, web_group

def data_wrangling(web_group,experiment_roster,client_profiles):
    # This function combines and cleans the original dataframes obtained from load_data() function.
    
    # Groups clients and sums how many times each client was at a specific step.
    
    client_process_counts = web_group.groupby('client_id')['process_step'].value_counts().unstack(fill_value=0)
    
    # Renames columns to better visualize the steps the clients took.
    client_process_column_rename = {0: 'start', 1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'confirm'}
    client_process_counts = client_process_counts.rename(columns=client_process_column_rename)
    
    # Merges web data with experiment roster. This eliminates all the clients from the web data that weren't part of the experiment.
    final_rooster_process_counts = pd.merge(client_process_counts, experiment_roster, on='client_id', how='inner')
    
    # Merges the last dataset with client_profiles. By doing this we can see how clients interacted with each step, and the personal information for each client that was part of the experiment.
    final_rooster_process_counts_profile = pd.merge(final_rooster_process_counts, client_profiles, on='client_id', how='inner')
    
    # Extracts the clients that were part of the Control group and Test group to create two new datasets.
    control_profile_df = final_rooster_process_counts_profile[final_rooster_process_counts_profile['Variation'] == 'Control']
    test_profile_df = final_rooster_process_counts_profile[final_rooster_process_counts_profile['Variation'] == 'Test']
    
    # Merges web data with the list of clients that were part of Test or Control group. This way we can group client activity with their respective variation.
    web_group_experiment = pd.merge(web_group, experiment_roster, on='client_id', how='inner')
    
    # Merges web data, variation and client profile to get aggregate data based on client profiles. Note: Clients data will be repeated since web data contains all the information of what a client did when they were interacting with the problem.
    client_profile_experiment = pd.merge(web_group_experiment, client_profiles, on='client_id', how='left')

    return client_process_counts, final_rooster_process_counts_profile, control_profile_df, test_profile_df, web_group_experiment, client_profile_experiment
 
    
    
def calculate_completion_rate(data,variation=None):
    # This function calculates the overall completion rate or the completion rate of specifically each group.
    # Completion rate means a client started at 'start' and got up to 'confirm'.
    # Note: The respective steps are 'start','step_1','step_2','step_3','confirm'.
    
    # Parameters
    # data = dataset which must contain a column with the variation of the client: test or control and the process steps( not process count).
    # variation = if you want to get the completion rate of a specific group, just specify by typing 'Test' or 'Control'. Default is None which will give you the overall completion rate of both groups combined.
    
    
    if (variation == 'Test') or (variation == 'Control'):
        # This code is to get the completion rate of the specified group.
        
        # Extracts the clients that are in the specified group.
        variation_df = data[data['Variation']== variation]
        
        # Extracts the unique clients that got to step 4.
        confirm_step_users = variation_df[variation_df['process_step'] == 4]['client_id'].nunique()
        
        # Extracts the unique clients in the whole datset.
        total_users = variation_df['client_id'].nunique()
        
    else:
        
        # This code is to get the overall completion rate.
        
        # Extracts the unique clients that got to step 4.
        confirm_step_users = data[data['process_step'] == 4]['client_id'].nunique()
        
        # Extracts the unique clients in the whole datset.
        total_users = data['client_id'].nunique()
       
    
    # Calculates completion rate percentage.
    completion_rate_percentage = (confirm_step_users / total_users) * 100

    return completion_rate_percentage
   
    
    
def calculate_avg_time_per_step(data,variation=None):
    # This function calculates the average time it took clients to get from one step to another.
    
    # Parameters
    # data = dataset which must contain a column with the variation of the client: test or control and the process steps( not process count).
    # variation = if you want to get the completion rate of a specific group, just specify by typing 'Test' or 'Control'. Default is None which will give you the overall completion rate of both groups combined.
    
    # First it's important to sort values by client_id and date_time. The reason is that clients may log off one day to continue on another day. If we don't sort by date_time, your average will be inflated because of the log offs. In this case we are assuming clients must finish on the same day.
    merged_web_data = data.sort_values(by=['client_id', 'date_time'])
    
    # Groups clients by date_time and calculates the difference in time to go from one step to another.
    merged_web_data['time_diff'] = merged_web_data.groupby('client_id')['date_time'].diff()
    
    # Excludes 'start'(step 0) since we calculate the time it took to go from step 0 to step 1, and so on. 
    merged_web_data = merged_web_data[merged_web_data['process_step'] != 0]
    
    # Extracts the clients that are in the Test Group.
    merged_web_data_test = merged_web_data[merged_web_data['Variation']=='Test']
    
    # Extracts the clients that are in the Control Group.
    merged_web_data_control = merged_web_data[merged_web_data['Variation']=='Control']
    
    # Creating index to rename row index in the future.
    index_rename = {1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'confirm'}
    
    if variation == 'Control':
        
        # Calculates the mean for each step in the control group.
        average_time_per_step_control = merged_web_data_control.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        average_time_per_step_control = average_time_per_step_control.rename(index=index_rename)
        
        return average_time_per_step_control
    
    elif variation == 'Test':
        
        # Calculates the mean for each step in the control group.
        average_time_per_step_test = merged_web_data_test.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        average_time_per_step_test = average_time_per_step_test.rename(index=index_rename)
        
        return average_time_per_step_test
            
    elif variation == 'Overall':
        
        
        # Calculates the mean for each step overall. 
        avg_time_per_step = merged_web_data.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        avg_time_per_step = avg_time_per_step.rename(index=index_rename)
        
        return avg_time_per_step
    
    else:
        
        # This code returns all the previous values if you don't want them individually.
        
        # Calculates the mean for each step in the control group.
        average_time_per_step_control = merged_web_data_control.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        average_time_per_step_control = average_time_per_step_control.rename(index=index_rename)
        
        # Calculates the mean for each step in the test group.
        average_time_per_step_test = merged_web_data_test.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        average_time_per_step_test = average_time_per_step_test.rename(index=index_rename)
        
        # Calculates the mean for each step overall.
        avg_time_per_step = merged_web_data.groupby('process_step')['time_diff'].mean()
        
        # Renames index
        avg_time_per_step = avg_time_per_step.rename(index=index_rename)
        
        
        return average_time_per_step_control, average_time_per_step_test, avg_time_per_step
    

def error_rate(data,variation=None):
    # This function tells the rate at which a client went from further step into a past step. For example, if a client went from step_2 to step_1, this will count as an error.
    
    # Parameters
    # data = dataset which must contain a column with the variation of the client: test or control and the process steps( not process count).
    # variation = if you want to get the completion rate of a specific group, just specify by typing 'Test' or 'Control'. Default is None which will give you the overall completion rate of both groups combined.
    
    
    if (variation == 'Test') or (variation == 'Control'):
    # This code is to get the completion rate of the specified group.
    
        # Extracts the clients that are in the specified group.
        variation_df = data[data['Variation']== variation]
        
        # Sorts values by client_id and date_time.
        error_df = variation_df.sort_values(by=['client_id', 'date_time'])
        
    else:
        
        # This code is to calculate the overall error rate.
        
        # Sorts values by client_id and date_time.
        error_df = data.sort_values(by=['client_id', 'date_time'])
    
    
    # Shifts the values of each group one step forward in the 'process_step' column, and then compares the shifted values with the original values in the 'process_step' column. It checks if the previous 'process_step' value is greater than the current 'process_step' value for each group, and creates a boolean variable based on the conditions.
    error_mask = error_df.groupby('client_id')['process_step'].shift(1) > error_df['process_step']
    
    # Sums the values that are True in error_mask.
    total_errors = error_mask.sum()
    
    # Takes all the rows in the dataframe.
    total_steps = error_df.shape[0]
    
    # Calculates error_rate.
    error_rate = total_errors / total_steps *100
    
    # Calculates the mean error for each step
    average_error_per_step = error_mask.groupby(data['process_step']).mean()*100
    
    
    return total_errors, total_steps, error_rate, average_error_per_step


def drop_off_rate(data,variation=None):
    # This function calculates the rate at which clients leave a step and don't continue to the next one.
    
    # Parameters
    # data = dataset which must contain a column with the variation of the client: test or control and the process steps( not process count).
    # variation = if you want to get the completion rate of a specific group, just specify by typing 'Test' or 'Control'. Default is None which will give you the overall completion rate of both groups combined.
    
    if (variation == 'Test') or (variation == 'Control'):
        # This code is to get the completion rate of the specified group.
        
        # Extracts the clients that are in the specified group.
        variation_df = data[data['Variation']== variation]
        
        # Sorts values by client_id and date_time.
        drop_off_rate = variation_df.sort_values(by=['client_id', 'date_time'])
        
    else:
        # This code is to calculate the overall error rate.
        
        # Sorts values by client_id and date_time.
        drop_off_rate = data.sort_values(by=['client_id', 'date_time'])
    
    # Initializes empty list to store drop off rate per step.
    dropoff_rates = []
    
    # Initializes a loop using the range of the process steps (0-4).
    for step in range(drop_off_rate['process_step'].max() + 1):
        
        # Calculates how many unique clients are in the loop step.
        total_clients_at_step = drop_off_rate[drop_off_rate['process_step'] == step]['client_id'].nunique()
        
        # Excludes last step (4,'confirmation') since we assume clients click confirm and leave the program.
        if step < drop_off_rate['process_step'].max():
            
            # Calculates how many unique clients moved to the next step.
            next_step_clients = drop_off_rate[drop_off_rate['process_step'] == step + 1]['client_id'].unique()
            
            # Calculates how many clients didn't reach the next step.
            dropped_off_clients = total_clients_at_step - len(next_step_clients)
        else:
            
            # For when the loop gets to 4.
            dropped_off_clients = 0
        
        # Calculates the rate of the clients that dropped each step.
        dropoff_rate = dropped_off_clients / total_clients_at_step *100
        
        # Appends results to empty list.
        dropoff_rates.append({'process_step': step, 'dropoff_rate': dropoff_rate})
    
    # Transform list into dataframe.
    dropoff_df = pd.DataFrame(dropoff_rates)
    
    
    return dropoff_df



def statistic_func(data, evaluator, stat_test, alpha):
    # This function will calculate different statistical methods for the data.
    
    # Parameters
    # data = dataset which must contain client information and experiment variation. 
    # evaluator = what do you want to compare from both groups. Options are: age, tenure years, tenure months, gender, number of accounts, balance, calls in the last 6 months and logins in the last 6 months. 
    # stat_test = what test you want to perform. Options are: t-test, chi-test, two-proportion z-test and one-sided z-test.
    # alpha = the probability of rejecting the null hypothesis when it is actually true. The most common value is 0.05.
    
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
        column = 'balance_category'
    
    elif evaluator == 'calls in the last 6 months':
        column = 'calls_6_mnth'
    
    elif evaluator == 'logins in the last 6 months':
        column = 'logons_6_mnth'
    
    
    if stat_test == 't-test':
        # This test is used to compare the means of two groups.
        
        # Extracts clients from control group.
        control_group_data = data[data['Variation'] == 'Control'][column].dropna()
        
        # Extracts clients from test group.
        test_group_data = data[data['Variation'] == 'Test'][column].dropna()
        
        # t statistic function
        t_statistic, p_value = ttest_ind(control_group_data, test_group_data, equal_var=False)

        # Compares p_value to alpha to reject or fail to reject the null hypothesis.
        if p_value < alpha:
            hypothesis_string = (f"Reject the null hypothesis: There is a significant difference in the average {evaluator} between the Control and Test groups.")
        else:
            hypothesis_string = (f"Fail to reject the null hypothesis: There is no significant difference in the average {evaluator} between the Control and Test groups.")
        
        
        print(f"T-statistic: {t_statistic:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(hypothesis_string)
        
        return t_statistic, p_value, hypothesis_string

    
    elif stat_test == 'chi-test':
        # This test is used for categorical data to test if there is a significant association between two categorical variables.
        
        # Extracts median account balance from dataset.
        median_balance = data['bal'].median()
        
        # Drops null values if no balance is available.
        data.dropna(subset=['bal'], inplace=True)
        
        # Creates a new column clasiffiyng the clients with low or high balance.
        data['balance_category'] = pd.cut(data['bal'], bins=[float('-inf'), median_balance, float('inf')],
                                labels=['Low Balance', 'High Balance'])
        
        # Extracts the clients that reached the last step.
        data['completed'] = data['confirm'] != 0
        
        if evaluator != 'gender':
            
            # Creates a table that shows the counts of observations for each combination of categories in the 'completed' column and the specified column. Each cell in the table represents the count of occurrences of a specific combination of values.
            contingency_table = pd.crosstab(data['completed'],data[column])
            
        else:
            # Creates a table that shows the counts of observations for each combination of categories in the 'Variation' column and the specified column. Each cell in the table represents the count of occurrences of a specific combination of values.
            contingency_table = pd.crosstab(data['Variation'], data[column])
        
        # chi_test function
        chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        
        # Compares p_value to alpha to reject or fail to reject the null hypothesis.
        if p_value < alpha:
            hypothesis_string = (f"Reject the null hypothesis: There is a significant difference in the proportion of clients engaging with the new process across different {evaluator} categories.")
        else:
            hypothesis_string = (f"Fail to reject the null hypothesis: There is no significant difference in the proportion of clients engaging with the new process across different {evaluator} categories.")
        
        print(f"Chi-square statistic: {chi2_stat:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(hypothesis_string)
        
        return chi2_stat, p_value, hypothesis_string
    
    else:
        
        # Extracts clients from control group.
        control_group_data = data[data['Variation'] == 'Control']
        
        # Extracts clients from test group.
        test_group_data = data[data['Variation'] == 'Test']
        
        # Extracts unique clients from control group that reached the last step (4, confirm).
        users_at_last_step_control = control_group_data[control_group_data['process_step'] == 4]['client_id'].nunique()
        
        # Extracts unique clients from test group that reached the last step (4, confirm).
        users_at_last_step_test = test_group_data[test_group_data['process_step'] == 4]['client_id'].nunique()
        
        # Extracts unique clients from control group.
        total_users_control = control_group_data['client_id'].nunique()
        
        # Extracts unique clients from control group.
        total_users_test = test_group_data['client_id'].nunique()
        
        # Creates a list of clients in last step for control and test group.
        count = [users_at_last_step_control, users_at_last_step_test]
        
        # Creates a list of unique clients for control and test group.
        nobs = [total_users_control, total_users_test]
        
        if stat_test == 'two-proportion z-test':
            # This test is used to compare the proportions of two independent groups.
            
            # two-proportion z-test function
            stat, p_value = proportions_ztest(count, nobs)
            
            # Compares p_value to alpha to reject or fail to reject the null hypothesis.
            if p_value < alpha:
                hypothesis_string = ("Reject the null hypothesis: There is evidence that completion rates are different.")
            else:
                hypothesis_string = ("Fail to reject the null hypothesis: There is no significant evidence that completion rates are different.")
                
            # Creates plot to visualize findings.
            labels = ['Control Group', 'Test Group']
            success_counts = [users_at_last_step_control, users_at_last_step_test]
            failure_counts = [total_users_control - users_at_last_step_control, total_users_test - users_at_last_step_test]
            
            fig, ax = plt.subplots()
            bar_width = 0.35
            
          
            colormap = plt.get_cmap('OrRd')
            bar1 = ax.bar(labels, success_counts, bar_width, label='Success (Last Step)', color=colormap(0.6))  # You can adjust 
            bar2 = ax.bar(labels, failure_counts, bar_width, bottom=success_counts, label='Failure (Not Last Step)', color=colormap(0.4))  
            
            ax.set_ylabel('Counts')
            ax.set_title('Completion Rates for Control and Test Groups')
            ax.legend()
            
            plt.show()
                
            print(f"Z-statistic: {stat}")
            print(f"P-value: {p_value}")
            print(hypothesis_string)
            
            return stat, p_value, hypothesis_string
        
        else:
            # The One-Sided Z-Test is used to test whether the proportion of successes in a sample is significantly greater or less than a known population proportion.
            # This will compare the test group completion rate with the completion rate of the control group increased by 5%.
            
            # One-Sided Z-Test function
            stat, p_value = proportions_ztest(count, nobs, alternative='larger')
            
            # Compares p_value to alpha to reject or fail to reject the null hypothesis.
            if p_value < alpha:
                hypothesis_string = ("Reject the null hypothesis: The completion rate for the Test group is greater than the Control group increased by 5%.")
            else:
                hypothesis_string = ("Fail to reject the null hypothesis: There is no significant evidence that the completion rate for the Test group is greater than the Control group increased by 5%.")
            
            # Control Group threshold increase.
            threshold_increase = 0.05
            
            # Extracts the rate of clients that got up to the last step for the control group.
            completion_rate_control = users_at_last_step_control / total_users_control
            
            # Extracts the rate of clients that got up to the last step for the control group.
            completion_rate_test = users_at_last_step_test / total_users_test
            
            # Control group rate is upped by 5% increase.
            threshold_completion_rate = completion_rate_control + threshold_increase
            
            # Creates plot to visualize findings.
            labels = ['Control Group', 'Test Group']
            completion_rates = [completion_rate_control, completion_rate_test]
            threshold_completion_rates = [threshold_completion_rate, threshold_completion_rate]
            
            fig, ax = plt.subplots()
            
            bar_width = 0.35
            bar_positions = np.arange(len(labels))
            
            
            colormap = plt.get_cmap('OrRd')
            bar1 = ax.bar(bar_positions, completion_rates, bar_width, label='Completion Rate', color=colormap(0.7))  
            bar2 = ax.bar(bar_positions, threshold_completion_rates, bar_width, alpha=0.5, label='Threshold Completion Rate', color=colormap(0.4))  
            
            ax.axhline(y=threshold_completion_rate, color='red', linestyle='--', label='Threshold')
            
            ax.set_ylabel('Completion Rate')
            ax.set_title('Completion Rates for Control and Test Groups')
            ax.set_xticks(bar_positions)
            ax.set_xticklabels(labels)
            ax.legend()
            
            plt.show()
            
            print(f"Z-statistic: {stat:.4f}")
            print(f"P-value: {p_value:.4f}")
            print(hypothesis_string)
            
            return stat, p_value, hypothesis_string
