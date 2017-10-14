#!/usr/bin/python

import pickle
from numpy import *
#sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
import pprint
from sklearn.feature_selection import SelectKBest
import pandas as pd
import numpy as np
import pprint 
import seaborn
import matplotlib.pyplot as plt

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

poi_label = 'poi'
features_list = ['poi',
                 'restricted_stock',
                 'restricted_stock_deferred',
                 'salary',
                 'total_payments',
                 'total_stock_value',
                 'bonus',
                 'deferral_payments',
                 'deferred_income',
                 'director_fees',
                 'exercised_stock_options',
                 'expenses',
                 'loan_advances',
                 'long_term_incentive',
                 'other',
                 'from_messages',
                 'from_poi_to_this_person',
                 'from_this_person_to_poi',
                 'shared_receipt_with_poi',
                 'to_messages'] # You will need to use more features

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )


### Task 2: Remove outliers

data_dict.pop('TOTAL')

data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E' )

### Task 3: Create new feature(s)
# financial_fields = ['salary', 'bonus','deferred_income']
# financial_fields = ['exercised_stock_options', 'total_stock_value','bonus']
# Adds a new aggregate financial feature from the given features
def financial_agg(data_dict, features_list):
    financial_fields = ['salary', 'bonus','deferred_income']
    for record in data_dict:
        person = data_dict[record]
        check_nan = True
        for field in financial_fields:
            if person[field] == 'NaN':
                check_nan = False
        if check_nan:
            person['financial_agg'] = sum([person[field] for field in financial_fields])
        else:
            person['financial_agg'] = 'NaN'
    features_list += ['financial_agg']


def email_feature(data_dict,features_list):
    email_fields = ['to_messages', 'from_messages',
              'from_poi_to_this_person', 'from_this_person_to_poi']
              
    for record in data_dict:
        person = data_dict[record]
        check_nan = True
        for field in email_fields:
            if person[field] == 'NaN':
                check_nan = False
        if check_nan:
            total_messages = person['to_messages'] +\
                             person['from_messages']
            poi_messages = person['from_poi_to_this_person'] +\
                           person['from_this_person_to_poi']
            person['email_poi'] = float(poi_messages) / total_messages
        else:
            person['email_poi'] = 'NaN'
      
    features_list += ['email_poi']

email_feature(data_dict,features_list)
financial_agg(data_dict,features_list)


### Store to my_dataset for easy export below.
my_dataset = data_dict

def get_k_best(data_dict, features_list, k):
    """ runs scikit-learn's SelectKBest feature selection
        returns dict where keys=features, values=scores
    """
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    #print sorted_pairs
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sorted_pairs)
    k_best_features = dict(sorted_pairs[:k])
    return k_best_features
    
    
# SelectKBest Test
    
accuracyk = []
precisionk = []
recallk = []
f1k = []

# Below is the range to test for K value for SelectKBest
# Change these to whatever range of K values you like
selectedk = range(11, 12) 

for i in selectedk:
    
    best_features = get_k_best(my_dataset, features_list, i)
    features_list2 = [poi_label] + best_features.keys()
    
    # Evaluation of the Classifiers
    
    # Pipeline
    from sklearn.pipeline import Pipeline
    from sklearn import preprocessing
    
    ### Logistic Regression
    from sklearn.linear_model import LogisticRegression
    clf_logreg = [
        ('MinMaxScaler', preprocessing.MinMaxScaler()),
        ('LogisticRegression', LogisticRegression(C=10000000))
    ]
    
    ### Gaussian Naive Bayes
    from sklearn.naive_bayes import GaussianNB
    clf_gaussian = [
        ('MinMaxScaler', preprocessing.MinMaxScaler()),
        ('GaussianNB', GaussianNB())
    ]
    
    ### Stochastic Gradient Descent
    from sklearn.linear_model import SGDClassifier
    clf_graddes = [
        ('MinMaxScaler', preprocessing.MinMaxScaler()),
        ('SGDClassifier', SGDClassifier())
    ]
    
    ### Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier
    clf_randfor = [
        ('MinMaxScaler', preprocessing.MinMaxScaler()),
        ('RandomForestClassifier', RandomForestClassifier(max_depth = 15, n_estimators =10, max_features = 'sqrt'))
    ]
    
    ### K-means Clustering
    from sklearn.cluster import KMeans
    clf_kmeans = [
        ('MinMaxScaler', preprocessing.MinMaxScaler()),
        ('KMeans', KMeans(n_clusters=2, tol=0.001))
    ]
    
    clf_pipe = Pipeline(clf_logreg)
    # Chosen Classifier
    chosen_clf = clf_pipe
    # Evaluation of the Chosen Classifier
    accuracy, precision, recall, f1 =  test_classifier(chosen_clf, my_dataset, features_list2, folds = 1000)
    #print accuracy, precision, recall, f1
    accuracyk.append([accuracy])
    precisionk.append([ precision])
    recallk.append([recall])
    f1k.append([f1])
    
plt.plot(selectedk, accuracyk)
plt.plot(selectedk, precisionk)
plt.plot(selectedk, recallk)
plt.plot(selectedk, f1k)
plt.legend(['accuracyk', 'precisionk', 'recallk', 'f1k'], loc='upper left')
plt.show()


'''
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
'''

dump_classifier_and_data(chosen_clf, my_dataset, features_list2)