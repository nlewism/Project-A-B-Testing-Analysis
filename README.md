# Vanguard_Customer_Analysis
Project status(Active)

# Project objective
The primary objective of this project is to analyze the outcomes of the A/B test conducted by the Customer Experience (CX) team at Vanguard. The focus is on evaluating the impact of introducing a more intuitive and modern User Interface (UI), along with timely in-context prompts, on the online client experience. The experiment, which ran from 3/15/2017 to 6/20/2017, involved a control group using Vanguard's traditional online process and a test group exposed to the new, enhanced digital interface. Both groups followed an identical process sequence comprising an initial page, three subsequent steps, and a confirmation page to gauge process completion rates. The goal is to discern whether the revamped design contributes to a superior user experience, ultimately leading to higher rates of successful process completion. The findings from this analysis will provide crucial insights for optimizing Vanguard's digital platforms and enhancing overall client satisfaction.

# Methods used
Grouping and Data Analysis:
- groupby(): Aggregates or analyses DataFrame rows according to designated columns.
- nunique(): Returns the number of unique elements along a particular axis, providing counts of distinct values in each column.
- value_counts(): Computes and provides the counts of unique elements in a Series, offering insights into the distribution of values.

Data Cleaning:
- rename(): Renames columns or indices of a DataFrame, enhancing clarity or consistency.
Data Transformation:
- to_datetime(): Allows you to manipulate and analyze dates and times by converting a column or columns in a DataFrame to datetime format.

Data Combination and Manipulation:
- concat(): Concatenates two or more DataFrames along a specified axis, facilitating the combination of datasets with similar structures.
- merge(): Combines two DataFrames into a single DataFrame based on a common column, similar to SQL joins.

Data Sorting and Manipulation:
- sort_values(): Sorts a DataFrame by one or more columns, allowing for better data organization.
Data Combination:
- append(): Appends rows of one DataFrame to another, enabling the vertical combination of two datasets.

Visualization:
- sns.histplot(): Creates a histogram, visualizing the distribution of a single variable by dividing the data into bins and displaying the frequency or density of observations in each bin.
- sns.countplot(): Creates a bar plot representing the counts of unique values in a categorical variable, making it useful for visualizing the distribution of categorical data.
- sns.scatterplot(): Creates a scatter plot, where each point represents an observation with values on both the x and y axes, providing insights into the correlation or pattern between two numerical variables.
- sns.boxplot(): Generates a box plot, providing a visual summary of the distribution of numerical data, including measures of central tendency and the spread of the data.
- sns.barplot(): Generates a bar plot, typically used to depict the average value of a numerical variable for different categories, providing a clear visual representation of the central tendency across different groups.

# Technologies used
- Python
- Pandas
- Seaborn
- Matplotlib.pyplot
- Numpy
- Statsmodels.stats.proportion
- Scipy.stats
- Streamlit

# Project Description: Enhancing User Experience through Digital Experiment Analysis at Vanguard

Context:

As newly onboarded data analyst in the Customer Experience (CX) team at Vanguard, a leading US-based investment management company, our inaugural task involves delving into the outcomes of an ambitious digital experiment undertaken by the team. In response to the dynamic evolution of the digital landscape and the changing expectations of Vanguard's clients, the CX team implemented enhancements in the form of a more intuitive and modern User Interface (UI). Coupled with timely in-context prompts, these changes were anticipated to streamline the online process for clients. The overarching question driving this initiative was whether these design modifications would effectively encourage a higher number of clients to successfully complete the online process.

Experiment Overview:

The experiment, conducted through A/B testing, spanned from 3/15/2017 to 6/20/2017. The participants were divided into two groups:

- Control Group: Engaged with Vanguard's traditional online process.
- Test Group: Experienced the new, upgraded digital interface.

Both groups traversed an identical process sequence, encompassing an initial page, three subsequent steps, and a confirmation page indicating process completion. The primary objective was to assess if the redesigned interface indeed contributed to an improved user experience and higher rates of successful process completion.

Data Tools:

To undertake a comprehensive analysis, three datasets will serve as our guiding compass:

- Client Profiles (df_final_demo): This dataset encapsulates crucial demographic information such as age, gender, and account details of Vanguard's clients.
- Digital Footprints (df_final_web_data): This dataset provides an intricate trace of client interactions online, presented in two parts (pt_1 and pt_2). Merging these two files is recommended for a holistic analysis of digital engagement.
- Experiment Roster (df_final_experiment_clients): This dataset reveals which clients were part of the grand experiment, segregating those exposed to the new digital interface.

Project Goal:

Our mission is to leverage these datasets to unravel insights that shed light on the impact of the UI enhancements on user experience and process completion rates. Through meticulous data analysis, we aim to provide actionable recommendations to optimize Vanguard's digital platforms and elevate overall client satisfaction.

This project marks a pivotal step in understanding the dynamics of user interactions within the financial realm and contributes to Vanguard's commitment to delivering an exceptional digital experience to its clientele.

# Project Setup and Analysis Steps
Follow these steps to set up and conduct the analysis for the Vanguard CX team's digital experiment.

Step 1: Clone the Repository

- Clone the project repository to your local machine.

Step 2: Install Dependencies

- Ensure you have the required Python libraries installed. You can install them using:"pip install -r requirements.txt"

Step 3: Load and Merge Datasets

- Load the three datasets (df_final_demo, df_final_web_data, and df_final_experiment_clients) into your preferred data analysis environment (e.g., Jupyter Notebook, Python script). Merge the df_final_web_data parts (pt_1 and pt_2) for a comprehensive analysis.

Step 4: Explore Data

- Explore the datasets to gain a preliminary understanding. Check for missing values, outliers, and any patterns that may influence the analysis.

Step 5: Preprocess Data

- Preprocess the data as needed. Handle missing values, perform data cleaning, and ensure datasets are in a suitable format for analysis.

Step 6: Conduct A/B Testing Analysis

- Utilize statistical techniques to analyze the A/B test results. Compare the Control and Test groups to uncover insights into user experience and process completion rates.

Step 7: Visualize Results

- Create visualizations (using tools like Seaborn and Matplotlib) to illustrate key findings. Visual representations enhance the understanding of trends and patterns.

Step 8: Generate Insights and Recommendations

- Based on your analysis, generate actionable insights and recommendations for the Vanguard CX team. Consider the implications of the UI changes on user behavior and suggest potential optimizations.

Step 9: Document Your Analysis

- Document your analysis process, findings, and any code-related information. Ensure clarity for team members or collaborators who may review or continue the analysis.

Step 10: Contribute or Share Results

- If applicable, contribute your findings back to the project repository. Share results with relevant stakeholders, and consider how your analysis might inform future iterations of the digital experiment.

# Key Findings

Completion Rate Analysis:

- Hypothesis Testing: Conducted a two-proportion z-test to compare the completion rates of the Test (new design) and Control (old design) groups. The results yielded a Z-statistic of -8.87 and an extremely low p-value (7.02e-19), leading to the rejection of the null hypothesis. There is robust evidence that completion rates are significantly different between the two groups.

- Alternative Hypothesis Testing: Performed a one-sided z-test to assess whether the completion rate for the Test group is greater than the Control group increased by 5%. The analysis returned a Z-statistic of -8.87 and a p-value of 1.00, indicating a failure to reject the null hypothesis. There is no significant evidence that the completion rate for the Test group is greater than the Control group increased by 5%.

Gender Engagement Analysis:

- Hypothesis Testing: Applied a chi-square test to investigate the gender-based differences in client engagement with the new process. With a chi-square statistic of 3.62 and a p-value of 0.31, the analysis failed to reject the null hypothesis. There is no significant difference in the proportion of clients engaging with the new process across different gender categories.

Client Age Analysis:

- Hypothesis Testing: Utilized a t-test to examine the average age difference between clients engaging with the new and old processes. The t-statistic was 2.42, and the p-value was 0.02, leading to the rejection of the null hypothesis. There is a significant difference in the average age between the Control and Test groups.

Client Tenure Analysis:

- Hypothesis Testing: Applied a t-test to assess the average client tenure difference between the Test and Control groups. The t-statistic was 1.87, and the p-value was 0.06, indicating a failure to reject the null hypothesis. There is no significant difference in the average tenure years between the Control and Test groups.

These key findings provide valuable insights into the impact of the new UI on completion rates, gender engagement, client age, and tenure. The results guide actionable recommendations for refining the digital experience and tailoring strategies to specific client segments.

# Conclusion
Summarizing the Vanguard CX Team's Digital Experiment Analysis, we observed a significant impact of the redesigned User Interface (UI) on completion rates, highlighting its influence on user interactions. While the 5% increase hypothesis was inconclusive, our findings suggest a need for nuanced strategies in targeting diverse age groups. Interestingly, gender did not emerge as a significant factor affecting engagement with the new UI. The analysis provides actionable insights, encouraging a focused and iterative approach to further refine the UI for enhanced user experience across different client segments. Explore the repository for a detailed breakdown of our findings and recommendations, shaping the path forward for Vanguard's digital evolution.

# Presentation

# Contact
- Github:
    - 
    - 
    - 
- LinkedIn:
    - 
    - 
    - 

