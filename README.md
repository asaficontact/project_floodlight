
## NOTE
#### Original files for the project exceed GitHub's maximum file size limit. Click on the link below to access complete code and data files for the project

LINK: https://drive.google.com/open?id=17rMuC6UW2KR5iVxQnc_BNP-lqTZmxQCF

## Initial Setup


```python
#Do all necessary Pacakge Imports
from imports import *
```


```python
#Create a dataHandler class for our dataframe 
data = dh()
```


```python
#Get Data for crisis in asia and southern asia
southern_asia_df = data.filter_data(region=['Southern Asia', 'South-Eastern Asia'])
asia_df = data.filter_data(region=['Middle East', 'Southern Asia', 'South-Eastern Asia'])

#Get Data for crisis in asia and southern asia caused by rebel groups
asia_rebel_groups_df = data.filter_data(region=['Middle East', 'Southern Asia', 'South-Eastern Asia'], rebel_groups=True)
southern_asia_rebel_groups_df = data.filter_data(region=['Southern Asia'], rebel_groups=True)
```

## Predictors of Interest

#### 1: Fatalities
#### 2: Event Type
#### 3: Sub Event Type
#### 4: Associate Actor 1 
#### 5: Actor 2 
#### 6: Inter 2
#### 7: Interaction
#### 8: Region
#### 9: Admin 1
#### 10: Admin 2
#### 11: Admin 3
#### 12: Location
#### 13: Associate Actor 2
#### 14: Country

NOTE: To better understand the predictors look at documentation in Understanding_data folder.

## Types of Actors involved in Crisis Dataset

#### 1: State Forces
#### 2: Rebel Groups
#### 3: Political Militias
#### 4: Identity Militias
#### 5: Rioters
#### 6: Protestors
#### 7: Civilian
#### 8: External/Other Forces

## Crisis Data Initial Exploration for Asia

##### Crisis to Fatalities per Country caused by All Actors[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_df, 'country_paired')
```


![png](README_files/main_13_0.png)


##### Number of Crisis caused by all Actors per Country[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_df, type='crisis map')
```


![png](README_files/main_15_0.png)


##### Crisis to Fatalities per Country caused by Rebel Groups[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_rebel_groups_df, 'country_paired')
```


![png](README_files/main_17_0.png)


##### Number of Crisis caused by Rebel Groups per Country[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_rebel_groups_df, type='crisis map')
```


![png](README_files/main_19_0.png)


##### Crisis to Fatalities per Event Type caused by All Actors[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_df, type='event_paired')
```


![png](README_files/main_21_0.png)


##### Crisis to Fatalities per Country caused by Rebel Groups[2017-2019]


```python
data.crisis_to_fatalities_graph(asia_rebel_groups_df, type='event_paired')
```


![png](README_files/main_23_0.png)


## Random Forest Model for Classifying Rebel Groups in Afghanistan

##### Creating best random forest for Afghanistan by Grid Search


```python
#Get Data for crisis in Afghanistan caused by rebel groups
afg_rebel_groups_df = data.filter_data(country=['Afghanistan'], rebel_groups=True)
#Get Random Forest [the best parameters have been found using grid search]
afg_rebel_groups_rf = data.random_forest(afg_rebel_groups_df, max_depth= 30, min_samples_leaf=1, min_samples_split = 10, n_estimators=500, model_name = 'afghanistan')
```

##### Load best Random Forest model based of grid search for Afghanistan


```python
asia_rebel_groups_rf = data.load_model('Afghanistan')
```

##### Confusion Matrix for Training Data [Normalized]



```python
data.plot_confusion_matrix(afg_rebel_groups_df, afg_rebel_groups_rf, dataset_type = 'train', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fab923ebe48>




![png](README_files/main_30_1.png)


##### Confusion Matrix for Testing Data [Normalized]


```python
data.plot_confusion_matrix(afg_rebel_groups_df, afg_rebel_groups_rf, dataset_type = 'test', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fab444f72b0>




![png](README_files/main_32_1.png)


##### Tests to check accuracy of the model


```python
data.classifier_accuracy(afg_rebel_groups_df, afg_rebel_groups_rf)
```




    {'training_accuracy': 0.8340914013428633,
     'testing_accuracy': 0.8232618583495777,
     'training_F1_weighted': 0.7805860368800424,
     'testing_F1_weighted': 0.7674833570687929,
     'training_precision_weighted': 0.8515754941098571,
     'testing_precision_weighted': 0.8386940263095153,
     'training_recall_weighted': 0.8340914013428633,
     'testing_recall_weighted': 0.8232618583495777}



## Random Forest Model for Classifying Rebel Groups in Southern Asia

##### Load best Random Forest model based of grid search for Southern Asia


```python
southern_asia_rebel_groups_rf = data.load_model('southern_asia')
```

##### Confusion Matrix for Training Data [Normalized]


```python
data.plot_confusion_matrix(southern_asia_rebel_groups_df, southern_asia_rebel_groups_rf, dataset_type = 'train', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc528549f28>




![png](README_files/main_39_1.png)


##### Confusion Matrix for Testing Data [Normalized]


```python
data.plot_confusion_matrix(southern_asia_rebel_groups_df, southern_asia_rebel_groups_rf, dataset_type = 'test', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc528549ac8>




![png](README_files/main_41_1.png)


##### Tests to check accuracy of the model


```python
data.classifier_accuracy(southern_asia_rebel_groups_df, southern_asia_rebel_groups_rf)
```




    {'training_accuracy': 0.8423524022218405,
     'testing_accuracy': 0.8268338773406632,
     'training_F1_weighted': 0.7898185645638188,
     'testing_F1_weighted': 0.7707830293459663,
     'training_precision_weighted': 0.8712670574510711,
     'testing_precision_weighted': 0.8306234964296919,
     'training_recall_weighted': 0.8423524022218405,
     'testing_recall_weighted': 0.8268338773406632}



## Random Forest Model for Classifying Rebel Groups in Asia

##### Load best Random Forest model based of grid search for Asia


```python
asia_rebel_groups_rf = data.load_model('asia')
```

##### Confusion Matrix for Training Data [Normalized]



```python
data.plot_confusion_matrix(asia_rebel_groups_df, asia_rebel_groups_rf, dataset_type = 'train', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc539b6a5c0>




![png](README_files/main_48_1.png)


##### Confusion Matrix for Testing Data [Normalized]


```python
data.plot_confusion_matrix(asia_rebel_groups_df, asia_rebel_groups_rf, dataset_type = 'test', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc549f98b00>




![png](README_files/main_50_1.png)


##### Tests to check accuracy of the model


```python
data.classifier_accuracy(asia_rebel_groups_df, asia_rebel_groups_rf)
```




    {'training_accuracy': 0.853942423468457,
     'testing_accuracy': 0.84090411558669,
     'training_F1_weighted': 0.8372359852046187,
     'testing_F1_weighted': 0.8226387702490333,
     'training_precision_weighted': 0.8441646669875207,
     'testing_precision_weighted': 0.8279729962978163,
     'training_recall_weighted': 0.853942423468457,
     'testing_recall_weighted': 0.84090411558669}



## Random Forest Model for Classifying Islamic State (Type of Rebel Group) in Asia

Create Dataset for Islamic State classification


```python
isis_df = data.filter_data(region = ['Southern Asia', 'Middle East', 'South-Eastern Asia'], rebel_groups= True, actor_name= 'islamic state')
```

##### Load best Random Forest model based of grid search for ISIS activity in Asia


```python
isis_rf = data.load_model('isis')
```

##### Confusion Matrix for Training Data [Normalized]



```python
data.plot_confusion_matrix(isis_df, isis_rf, dataset_type = 'train', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fe8183ffe48>




![png](README_files/main_59_1.png)


##### Confusion Matrix for Testing Data [Normalized]


```python
data.plot_confusion_matrix(isis_df, isis_rf, dataset_type = 'test', normalize = True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fe85d373588>




![png](README_files/main_61_1.png)


##### Tests to check accuracy of the model


```python
data.classifier_accuracy(isis_df, isis_rf)
```




    {'training_accuracy': 0.925958500276882,
     'testing_accuracy': 0.9200664484291787,
     'training_F1_weighted': 0.9238511827444541,
     'testing_F1_weighted': 0.9177113406155695,
     'training_precision_weighted': 0.9330340541392627,
     'testing_precision_weighted': 0.9277676133005858,
     'training_recall_weighted': 0.925958500276882,
     'testing_recall_weighted': 0.9200664484291787}


