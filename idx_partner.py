# -*- coding: utf-8 -*-
"""Salinan dari Portofolio IDX Partner.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11npbkDZiOe3AlqxFcgTmXpNB3PzVCJHA

## Import Library
"""

! pip install featurewiz

pip install imblearn

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',99)
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
sns.set()

from google.colab import drive
drive.mount('/content/drive')

"""## Import Data"""

df = pd.read_csv('/content/drive/MyDrive/DS/VIX/id x partners VIX/loan_data_2007_2014.csv',index_col=0)

"""# EDA"""

df.shape

df.info()

df.sample()

# drop kolom yang memiliki banyak unique value
cols_to_drop = [
    'id'
    , 'member_id'
    , 'url'
    , 'desc'
    , 'zip_code'
    , 'annual_inc_joint'
    , 'dti_joint'
    , 'verification_status_joint'
    , 'open_acc_6m'
    , 'open_il_6m'
    , 'open_il_12m'
    , 'open_il_24m'
    , 'mths_since_rcnt_il'
    , 'total_bal_il'
    , 'il_util'
    , 'open_rv_12m'
    , 'open_rv_24m'
    , 'max_bal_bc'
    , 'all_util'
    , 'inq_fi'
    , 'total_cu_tl'
    , 'inq_last_12m'
    , 'sub_grade'
]

data = df.drop(cols_to_drop, axis=1)

data.sample(5)

data.loan_status.value_counts(normalize=True)*100

"""Dapat dilihat bahwa variable `loan_status` memiliki beberapa nilai :

`Current` artinya pembayaran lancar, `Charged Off` artinya pembayaran macet sehingga dihapusbukukan, `Late` artinya pembayaran telat dilakukan, `In Grace Period` artinya dalam masa tenggang, `Fully Paid` artinya pembayaran lunas, `Default` artinya pembayaran macet

Dari definisi-definisi tersebut, masing-masing individu dapat ditandai apakah mereka merupakan `bad loan` (peminjam yang buruk) atau `good loan` (peminjam yang baik)

Pada **kasus** ini, keterlambatan pembayaran di atas 30 hari dan yang lebih buruk dari itu sebagai penanda bad loan
"""

bad_loan = ['Charged Off', 'In Grace Period', 'Late (31-120 days)', 'Default', 'Does not meet the credit policy. Status:Charged Off']

def loan(x):
  if x['loan_status'] not in bad_loan:
    status = 0
  else:
    status = 1
  return status

data['bad_loan'] = data.apply(lambda x: loan(x), axis = 1)

data['bad_flag'].value_counts(normalize=True)*100

"""Setelah melakukan pengelompokkan terhadap bad/good loan, dapat dilihat bahwa jumlah user yang ditandai sebagai bad loan jauh lebih sedikit daripada good loan. Hal ini menyebabkan terjadinya **imbalanced dataset**"""

data.drop('loan_status',axis=1,inplace=True)

"""## Cleaning, Preprocessing, Feature Engineering

### emp_length
"""

data['emp_length'].unique()

# modifikasi kolom emp_length agar menjadi numerikal
data['emp_length_int'] = data['emp_length'].str.replace('\+ years', '')
data['emp_length_int'] = data['emp_length_int'].str.replace('< 1 year', str(0))
data['emp_length_int'] = data['emp_length_int'].str.replace(' years', '')
data['emp_length_int'] = data['emp_length_int'].str.replace(' year', '')

data['emp_length_int'] = data['emp_length_int'].astype(float)

data.drop('emp_length',axis=1,inplace=True)

data['term'].unique()

# modifikasi kolom term agar menjadi numerikal
data['term_int'] = data['term'].str.replace(' months','')
data['term_int'] = data['term_int'].astype(float)

data.drop(['term'],axis=1,inplace=True)

"""### earliest_cr_line

Memodifikasi `earliest_cr_line` dari format bulan-tahun menjadi perhitungan berapa lama waktu berlalu sejak waktu tersebut. Untuk melakukan hal ini, umumnya digunakan reference date = hari ini. Namun, karena dataset tahun 2007-2014, maka akan lebih relevan jika menggunakan reference date di sekitar tahun 2017. Dalam contoh ini, tanggal 2017-12-01 sebagai reference date.
"""

data['earliest_cr_line'].head(3)

data['earliest_cr_line_date'] = pd.to_datetime(data['earliest_cr_line'], format='%b-%y')
data['earliest_cr_line_date'].head(3)

data['mths_since_earliest_cr_line'] = round(pd.to_numeric((pd.to_datetime('2017-12-01')-data['earliest_cr_line_date'])/np.timedelta64(1,'M')))
data['mths_since_earliest_cr_line'].head(3)

data['mths_since_earliest_cr_line'].describe()

"""Terlihat ada nilai yang aneh, yaitu negatif."""

data[data['mths_since_earliest_cr_line']<0][['earliest_cr_line','earliest_cr_line_date','mths_since_earliest_cr_line']].head(3)

# menghilangkan nilai negatif
data.loc[data['mths_since_earliest_cr_line']<0, 'mths_since_earliest_cr_line'] = data['mths_since_earliest_cr_line'].max()

data.drop(['earliest_cr_line','earliest_cr_line_date'],axis=1, inplace=True)

# mengubah kolom issue_d menjadi numerikal
data['issue_d_date'] = pd.to_datetime(data['issue_d'], format='%b-%y')
data['mths_since_issue_d'] = round(pd.to_numeric((pd.to_datetime('2017-12-01') - data['issue_d_date'])/np.timedelta64(1,'M')))

data['mths_since_issue_d'].describe()

data.drop(['issue_d','issue_d_date'], axis=1, inplace=True)

# mengubah kolom last_pymnt_d menjadi numerikal
data['last_pymnt_d_date'] = pd.to_datetime(data['last_pymnt_d'], format='%b-%y')
data['mths_since_last_pymnt_d'] = round(pd.to_numeric((pd.to_datetime('2017-12-01')-data['last_pymnt_d_date'])/np.timedelta64(1,'M')))

data['mths_since_last_pymnt_d'].describe()

data.drop(['last_pymnt_d','last_pymnt_d_date'],axis=1,inplace=True)

# mengubah kolom next_pymnt_d menjadi numerikal
data['next_pymnt_d_date'] = pd.to_datetime(data['next_pymnt_d'], format='%b-%y')
data['mths_since_next_pymnt_d'] = round(pd.to_numeric((pd.to_datetime('2017-12-01')-data['next_pymnt_d_date'])/np.timedelta64(1,'M')))

data['mths_since_next_pymnt_d'].describe()

data.drop(['next_pymnt_d','next_pymnt_d_date'], axis=1, inplace=True)

"""### Correlation Check"""

plt.figure(figsize=(20,20))
sns.heatmap(data.corr())

"""Di sini, jika ada pasangan fitur-fitur yang memiliki korelasi tinggi maka akan diambil salah satu saja, karena apabila terdapat lebih dari 1 fitur maka akan berpotensi terjadinya redundan. Nilai korelasi yang dijadikan patokan pada dataset ini adalah >0.7"""

# mendrop kolom yang memiliki korelasi > 0.7
corr_matrix = data.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
to_drop_hicorr = [column for column in upper.columns if any(upper[column] > 0.7)]

to_drop_hicorr

data.drop(to_drop_hicorr, axis=1, inplace=True)

"""### Check Categorical Features"""

data.select_dtypes(include='object').nunique()

"""Pada tahap ini dilakukan pembuangan fitur yang memiliki nilai unik sangat tinggi (high cardinality) dan fitur yang hanya memiliki satu nilai unik saja."""

data.drop(['emp_title','title','application_type', 'last_credit_pull_d'],axis=1,inplace=True)

data.select_dtypes(exclude='object').nunique()

"""Ternyata, pada tipe data selain `object` juga terdapat fitur yang hanya memiliki satu nilai unik saja, maka akan ikut dibuang juga."""

data.drop(['policy_code'],axis=1,inplace=True)

for col in data.select_dtypes(include='object').columns.tolist():
    print(data[col].value_counts(normalize=True)*100)
    print('\n')

"""Fitur yang sangat didominasi oleh salah satu nilai saja akan dibuang pada tahap ini."""

data.drop('pymnt_plan',axis=1,inplace=True)

"""## Missing Values

### Missing Value Checking
"""

check_missing = data.isnull().sum()*100/data.shape[0]
check_missing[check_missing>0].sort_values(ascending=False)

"""Di sini, kolom-kolom dengan missing values di atas 75% dibuang"""

data.drop('mths_since_last_record',axis=1,inplace=True)

"""### Missing Values Filling"""

data['annual_inc'].fillna(data['annual_inc'].mean(), inplace=True)
data['mths_since_earliest_cr_line'].fillna(0, inplace=True)
data['acc_now_delinq'].fillna(0, inplace=True)
data['total_acc'].fillna(0, inplace=True)
data['pub_rec'].fillna(0, inplace=True)
data['open_acc'].fillna(0, inplace=True)
data['inq_last_6mths'].fillna(0, inplace=True)
data['delinq_2yrs'].fillna(0, inplace=True)
data['collections_12_mths_ex_med'].fillna(0, inplace=True)
data['revol_util'].fillna(0, inplace=True)
data['emp_length_int'].fillna(0, inplace=True)
data['tot_cur_bal'].fillna(0, inplace=True)
data['tot_coll_amt'].fillna(0, inplace=True)
data['mths_since_last_delinq'].fillna(-1, inplace=True)

"""## Feature, Scaling and Transformation

### One Hot Encoding

Semua kolom kategorikal dilakukan One Hot Encoding
"""

categorical_cols = [col for col in data.select_dtypes(include='object').columns.to_list()]

onehot = pd.get_dummies(data[categorical_cols], drop_first=True)

onehot.head()

"""### Standardization

Semua kolom numerikal dilakukan proses standarisasi dengan StandardScaler
"""

numerical_cols = [col for col in data.columns.tolist() if col not in categorical_cols + ['bad_flag']]

from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
std = pd.DataFrame(ss.fit_transform(data[numerical_cols]), columns=numerical_cols)

std.head()

"""### Transformed Dataframe

Menggabungkan kembali kolom-kolom hasil transformasi
"""

data_model = pd.concat([onehot, std, data[['bad_flag']]], axis=1)

"""Melakukan seleksi fitur kembali karena setelah dilakukan encoding, fitur sangat banyak dan berpotensi terjadinya overfit ketika dilakukan modeling. Pada seleksi fitur ini, menggunakan featurewiz untuk mengurangi fitur yang digunakan untuk modeling"""

from featurewiz import featurewiz
feats = featurewiz(data_model, 'bad_flag', corr_limit=0.7, verbose=0)
len(feats)

# tersisa 20 fitur dari 90 fitur yang tersedia
feats[0]

"""## Modeling

### Train - Test Split
"""

from sklearn.model_selection import train_test_split

X = data_model[['recoveries',
 'total_rec_late_fee',
 'int_rate',
 'out_prncp',
 'dti',
 'mths_since_issue_d',
 'term_int',
 'annual_inc',
 'initial_list_status_w',
 'addr_state_NY',
 'loan_amnt',
 'addr_state_TX',
 'grade_G',
 'home_ownership_MORTGAGE',
 'addr_state_NH',
 'tot_cur_bal',
 'revol_util',
 'emp_length_int',
 'verification_status_Verified',
 'verification_status_Source Verified']]
y = data_model['bad_flag']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.shape, X_test.shape

# melakukan oversampling untuk mengatasi class imbalance
from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek
ro = RandomOverSampler()
X_train_ro, y_train_ro = ro.fit_resample(X_train, y_train)
y_train_series = pd.Series(y_train_ro)
#check value counts after oversampling
y_train_series.value_counts()

"""### Training

Pada contoh ini digunakan algoritma XGBoost untuk pemodelan.
"""

from xgboost import XGBClassifier

xg = XGBClassifier()
xg.fit(X_train_ro, y_train_ro)

"""Feature Importance dapat ditampilkan."""

arr_feature_importances = xg.feature_importances_
arr_feature_names = X_train.columns.values

df_feature_importance = pd.DataFrame(index=range(len(arr_feature_importances)), columns=['feature','importance'])
df_feature_importance['feature'] = arr_feature_names
df_feature_importance['importance'] = arr_feature_importances
df_all_features= df_feature_importance.sort_values(by='importance',ascending=False)
df_all_features

"""### Validation

Untuk mengukur performa model, dua metrik yang umum dipakai dalam dunia credit risk adalah AUC dan KS.
"""

y_pred_proba = xg.predict_proba(X_test)[:][:,1]

df_actual_predicted = pd.concat([pd.DataFrame(np.array(y_test),columns=['y_actual']),pd.DataFrame(y_pred_proba, columns=['y_pred_proba'])], axis=1)
df_actual_predicted.index = y_test.index

"""### AUC"""

from sklearn.metrics import roc_curve, roc_auc_score

fpr, tpr, tr = roc_curve(df_actual_predicted['y_actual'], df_actual_predicted['y_pred_proba'])
auc = roc_auc_score(df_actual_predicted['y_actual'], df_actual_predicted['y_pred_proba'])

plt.plot(fpr, tpr, label='AUC = %0.4f' %auc)
plt.plot(fpr, fpr, linestyle = '--', color='k')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()

"""### KS"""

df_actual_predicted = df_actual_predicted.sort_values('y_pred_proba')
df_actual_predicted = df_actual_predicted.reset_index()

df_actual_predicted['Cumulative N Population'] = df_actual_predicted.index + 1
df_actual_predicted['Cumulative N Bad'] = df_actual_predicted['y_actual'].cumsum()
df_actual_predicted['Cumulative N Good'] = df_actual_predicted['Cumulative N Population'] - df_actual_predicted['Cumulative N Bad']
df_actual_predicted['Cumulative Perc Population'] = df_actual_predicted['Cumulative N Population'] / df_actual_predicted.shape[0]
df_actual_predicted['Cumulative Perc Bad'] = df_actual_predicted['Cumulative N Bad'] / df_actual_predicted['y_actual'].sum()
df_actual_predicted['Cumulative Perc Good'] = df_actual_predicted['Cumulative N Good'] / (df_actual_predicted.shape[0] - df_actual_predicted['y_actual'].sum())

df_actual_predicted.head()

KS = max(df_actual_predicted['Cumulative Perc Good'] - df_actual_predicted['Cumulative Perc Bad'])

plt.plot(df_actual_predicted['y_pred_proba'], df_actual_predicted['Cumulative Perc Bad'], color='r')
plt.plot(df_actual_predicted['y_pred_proba'], df_actual_predicted['Cumulative Perc Good'], color='b')
plt.xlabel('Estimated Probability for Being Bad')
plt.ylabel('Cumulative %')
plt.title('Kolmogorov-Smirnov:  %0.4f' %KS)

from sklearn.metrics import classification_report
#predicting
y_preds = xg.predict(X_test)
#classification report
print(classification_report(y_test, y_preds))

"""Model yang dibangun menghasilkan performa `AUC = 0.92` dan `KS = 0.66`. Pada dunia credit risk modeling, umumnya AUC di atas 0.7 dan KS di atas 0.3 sudah termasuk performa yang baik."""