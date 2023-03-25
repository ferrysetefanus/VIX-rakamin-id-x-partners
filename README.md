# VIX-rakamin-id-x-partners
In this virtual internship, I am positioned as a Data Scientist Intern who is exposed to problems, case studies, and projects that become the daily routine of ID/X Partners. Data scientists will collaborate with business analysts, data engineers, software engineers, project managers, in the same project to provide the best IT Solution for clients. I was challenged to master and implement various skills and tools commonly used at ID/X Partners, such as Big Data Fundamentals, Statistics & Data Analytics, SQL Querying, R Programming, Python Programming, Machine Learning, etc. At the end, I was given the challenge to complete end-to-end Machine Learning modeling to create data science solutions for clients.

Some of the stages carried out in making machine learning models are:
- Defining the target column (in this dataset, the target column is named loan_status)
- Dividing the target column into 2 values, namely good and bad loans.
- After dividing the value of the target column, there is an imbalance between good and bad values, so oversampling will be carried out on the minor value (bad loan) so that the target value becomes balanced.
- Perform data cleaning and preprocessing
- Perform standardization on columns that have numeric data types so that they have the same value scale.
- Performing split datasets and oversampling of imbalanced target values so that they become balanced.
- Train the model using the XGBoost algorithm with an AUC Score of 92% and KS Score of 61%. Top 5 feature importance obtained from this model are : 
    - recoveries, which is the amount of money or assets successfully collected or obtained by creditors from borrowers who fail to repay loans.
    - total_rec_late_fee, which is the amount of late payment penalties collected or obtained by creditors from borrowers who are late in paying loans.
    - term_int, a high level of term_int can increase credit risk, because borrowers may have difficulty paying interest and principal on time.
    - int_rate, a high int_rate level can increase credit risk, as borrowers may have difficulty paying interest and principal on time.
    - out_prncp, is the remaining principal of the loan that must be paid by the borrower at a certain time. The greater the out_prncp, the higher the credit risk         faced by the creditor, because the borrower still has a large loan amount and has not repaid it in full.


