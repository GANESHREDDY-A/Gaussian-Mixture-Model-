#!/usr/bin/env python
# coding: utf-8

# In[79]:


get_ipython().run_line_magic('reset', '-f')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE
import re  #regular expression
from sklearn.preprocessing import StandardScaler
from pandas.plotting import andrews_curves
from mpl_toolkits.mplot3d import Axes3D


# In[80]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[81]:


pd.options.display.max_rows = 1000
pd.options.display.max_columns = 1000


# In[82]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[84]:


customer = pd.read_csv("C:/Users/annap/anaconda3/libs/Mall_Customers.csv")
customer.shape
customer.head()


# In[85]:


new_columns = {x : re.sub('[^A-Za-z]+','',x) for x in customer.columns.values}
new_columns
customer.rename(columns = new_columns,inplace=True)
customer.rename(columns = {"AnnualIncomek": "AnnualIncome"},inplace=True)


# In[86]:


customer["Gender"].value_counts()
customer["GenderCode"] = customer["Gender"].map({"Female" : 0, "Male" : 1})


# In[87]:


customer.drop(columns=["CustomerID","Gender"], inplace=True)


# In[88]:


customer.head()


# In[89]:


customer.info()


# In[90]:


#Analyse statistical data


# In[91]:


customer.describe()


# Annual income starts from 15K $ to max of 137K \$.
# Spending score starts from 1 to max upto 99
# Mean and Median are almost same for both Annual Income and Spending Score

# In[92]:


values = customer["GenderCode"].value_counts()
ax = sns.countplot(customer["GenderCode"])
for i, p in enumerate(ax.patches):
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2., height + 0.1, values[i],ha="center")


# In[93]:


andrews_curves(customer, "GenderCode")


# In[94]:


fig = plt.figure(figsize=(15,5))
ax=plt.subplot(1,3,1)
sns.boxplot(data=customer, x="GenderCode",y="Age")
ax=plt.subplot(1,3,2)
sns.boxplot(data=customer, x="GenderCode",y="AnnualIncome")
ax=plt.subplot(1,3,3)
sns.boxplot(data=customer, x="GenderCode",y="SpendingScore")


# Based on the box plots, Good Annual income and Spending scores in both Male & Female

# In[95]:


fig = plt.figure(figsize=(15,5))
ax=plt.subplot(1,3,1)
sns.stripplot(data=customer, x="GenderCode",y="Age")
ax=plt.subplot(1,3,2)
sns.stripplot(data=customer, x="GenderCode",y="AnnualIncome")
ax=plt.subplot(1,3,3)
sns.stripplot(data=customer, x="GenderCode",y="SpendingScore")


# In[96]:


fig = plt.figure(figsize=(15,5))
ax=plt.subplot(1,3,1)
sns.swarmplot(data=customer, x="GenderCode",y="Age")
ax=plt.subplot(1,3,2)
sns.swarmplot(data=customer, x="GenderCode",y="AnnualIncome")
ax=plt.subplot(1,3,3)
sns.swarmplot(data=customer, x="GenderCode",y="SpendingScore")


# ## DISTRIBUTION PLOTS

# In[97]:


fig = plt.figure(figsize=(15,5))
ax=plt.subplot(1,3,1)
sns.distplot(customer.Age, rug=True)
ax=plt.subplot(1,3,2)
sns.distplot(customer.AnnualIncome, rug=True)
ax=plt.subplot(1,3,3)
sns.distplot(customer.SpendingScore, rug=True)


# In[98]:


sns.pairplot(customer, vars=["Age","AnnualIncome","SpendingScore"], diag_kind="kde"
             , kind="reg", hue="GenderCode", markers=["o","D"],palette="husl")


# In[99]:


fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection='3d')
ax.scatter3D(customer['Age'], customer['AnnualIncome'], customer['SpendingScore']
             , c=customer['GenderCode'], cmap='RdBu');
ax.set_xlabel('Age')
ax.set_ylabel('AnnualIncome')
ax.set_zlabel('SpendingScore')


# In[100]:


fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection='3d')
ax.plot(customer['Age'], customer['AnnualIncome'], customer['SpendingScore']);
ax.set_xlabel('Age')
ax.set_ylabel('AnnualIncome')
ax.set_zlabel('SpendingScore')


# In[103]:


ss= StandardScaler()
ss.fit(customer)
X = ss.transform(customer)
X.shape


# In[104]:


sse = []
for k in range(1,10):
    km = KMeans(n_clusters = k)
    km.fit(X)
    sse.append(km.inertia_)
plt.plot(range(1,10), sse, marker='*')


# In[105]:


bic = []
aic = []
for i in range(8):
    gm = GaussianMixture(
                     n_components = i+1,
                     n_init = 10,
                     max_iter = 100)
    gm.fit(X)
    bic.append(gm.bic(X))
    aic.append(gm.aic(X))

fig = plt.figure()
plt.plot([1,2,3,4,5,6,7,8], aic)
plt.plot([1,2,3,4,5,6,7,8], bic)
plt.show()


# ## Based on Scree plot using Gaussian Mixture Algorithm, we could finalize 2 cluster groups

# In[106]:


kmeans_bad = KMeans(n_clusters=2,
                    n_init =10,
                    max_iter = 800)
kmeans_bad.fit(X)

centroids=kmeans_bad.cluster_centers_

fig = plt.figure()
plt.scatter(X[:, 1], X[:, 2],
            c=kmeans_bad.labels_,
            s=2)
plt.scatter(centroids[:, 1], centroids[:, 2],
            marker='x',
            s=100,               # marker size
            linewidths=150,      # linewidth of marker edges
            color='red'
            )
plt.show()


# In[107]:


gm = GaussianMixture(
                     n_components = 2,
                     n_init = 10,
                     max_iter = 100)
gm.fit(X)
#gm.means_
#gm.converged_
#gm.n_iter_
#gm.predict(X)
#gm.weights_
#np.unique(gm.predict(X), return_counts = True)[1]/len(X)
#gm.sample()
fig = plt.figure()

plt.scatter(X[:, 1], X[:, 2],
            c=gm.predict(X),
            s=5)
plt.scatter(gm.means_[:, 1], gm.means_[:, 2],
            marker='v',
            s=10,               # marker size
            linewidths=5,      # linewidth of marker edges
            color='red'
            )
plt.show()


# In[108]:


gm = GaussianMixture(
                     n_components = 2,
                     n_init = 10,
                     max_iter = 100)
gm.fit(X)

tsne = TSNE(n_components = 2)
tsne_out = tsne.fit_transform(X)
plt.scatter(tsne_out[:, 0], tsne_out[:, 1],
            marker='x',
            s=50,              # marker size
            linewidths=5,      # linewidth of marker edges
            c=gm.predict(X)   # Colour as per gmm
            )


# In[109]:


densities = gm.score_samples(X)
densities

density_threshold = np.percentile(densities,5)
density_threshold

anomalies = X[densities < density_threshold]
anomalies
anomalies.shape



fig = plt.figure()
plt.scatter(X[:, 1], X[:, 2], c = gm.predict(X))
plt.scatter(anomalies[:, 0], anomalies[:, 1],
            marker='x',
            s=50,               # marker size
            linewidths=5,      # linewidth of marker edges
            color='red'
            )


# In[110]:


unanomalies = X[densities >= density_threshold]
unanomalies.shape   

df_anomalies = pd.DataFrame(anomalies[:,[1,2]], columns=['salary','spendingscore'])
df_anomalies['type'] = 'anomalous'   # Create a IIIrd constant column
df_normal = pd.DataFrame(unanomalies[:,[1,2]], columns=['salary','spendingscore'])
df_normal['type'] = 'unanomalous'    # Create a IIIrd constant column


# In[111]:


df_anomalies.head()
df_normal.head()


# In[113]:


sns.distplot(df_anomalies['salary'], color='purple')
sns.distplot(df_normal['salary'], color='cyan')


# In[114]:


sns.distplot(df_anomalies['spendingscore'], color='purple')
sns.distplot(df_normal['spendingscore'], color='cyan')


# In[117]:


df = pd.concat([df_anomalies,df_normal])
df_anomalies.shape
df_normal.shape
df.shape


# In[118]:


sns.boxplot(x = df['type'], y = df['salary'])


# In[119]:


sns.boxplot(x = df['type'], y = df['spendingscore'])


# In[120]:


customer_NoGender = customer.copy() #Deep Copy
customer_NoGender.drop(columns=["GenderCode"], inplace = True)
#customer.head()
customer_NoGender.head()


# In[121]:


ss= StandardScaler()
ss.fit(customer_NoGender)
X = ss.transform(customer_NoGender)


# In[122]:


bic = []
aic = []
for i in range(8):
    gm = GaussianMixture(
                     n_components = i+1,
                     n_init = 10,
                     max_iter = 100)
    gm.fit(X)
    bic.append(gm.bic(X))
    aic.append(gm.aic(X))

fig = plt.figure()
plt.plot([1,2,3,4,5,6,7,8], aic)
plt.plot([1,2,3,4,5,6,7,8], bic)
plt.show()


# ## TSNE Visualization for 5 Clusters (without Gender field)

# In[124]:


tsne = TSNE(n_components = 2)
tsne_out = tsne.fit_transform(X)
plt.scatter(tsne_out[:, 0], tsne_out[:, 1],
            marker='x',
            s=50,              # marker size
            linewidths=5,      # linewidth of marker edges
            c=gm.predict(X)   # Colour as per gmm
            )


# With Gender Column (2 clusters)
# Without Gender Column (5 clusters)

# In[ ]:




