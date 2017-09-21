#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.tree import DecisionTreeClassifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi', 'expenses', 'other']


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
temp_data = {}
for x,y in zip(data_dict.keys(),data_dict.values()):
  if not x=='TOTAL':
    temp_data [x] = y


### Task 3: Create new feature(s)
my_dataset = temp_data 

def messages_ratio(messages_by_poi, messages_by_all):
    """ 
     Computes ratio of messages to/from PoI and rest of them. 
    """
    init = 0.0
    if messages_by_all !='NaN' and messages_by_all!=0.0:
          init = messages_by_poi/(1.0* messages_by_all)
    return init


for x,y in zip(temp_data.keys(), temp_data.values()):
        
        from_poi_ratio = messages_ratio(y["from_poi_to_this_person"], y["to_messages"])
        to_poi_ratio = messages_ratio(y["from_this_person_to_poi"], y["from_messages"])
        
        my_dataset[x]["from_poi_ratio"] = from_poi_ratio # Feature 1 -- Ratio of messages sent from PoI
        my_dataset[x]["to_poi_ratio"] = to_poi_ratio # Feature 2 -- Ratio of messages sent to PoI
        my_dataset[x]["all_poi_ratio"] = (to_poi_ratio*0.5) + (from_poi_ratio*0.5) # Feature 3 -- Ratio of all messages involving PoI

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

#Classifier -- 1
#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()

#Classifier -- 2
#clf = DecisionTreeClassifier()

#Classifier -- 3
#from sklearn.ensemble import RandomForestClassifier
#clf  = RandomForestClassifier()


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

##Tuning with max_depth:
#clf = DecisionTreeClassifier()
#clf =  DecisionTreeClassifier(max_depth=2)
#clf =  DecisionTreeClassifier(max_depth=4)
#clf =  DecisionTreeClassifier(max_depth=8)
#clf =  DecisionTreeClassifier(max_depth=12)
 
##Tuning with max_features:
#clf = DecisionTreeClassifier()
#clf = DecisionTreeClassifier(max_features="sqrt")
#clf = DecisionTreeClassifier(max_features="log2")
#clf = DecisionTreeClassifier(max_features="auto")

 
##Trying differnt values for random_state:
#clf = DecisionTreeClassifier()
#clf = DecisionTreeClassifier(random_state=42)
#clf = DecisionTreeClassifier(random_state=60)
#clf = DecisionTreeClassifier(random_state=39)

#Final fine tuned classifier params for best performance
clf = DecisionTreeClassifier(random_state=42,max_depth=8)

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)


from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
features_train = transformer.fit_transform(features_train).toarray()
features_test = transformer.fit_transform(features_test)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)