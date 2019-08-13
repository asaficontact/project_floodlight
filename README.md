# Mod_5_Project

* Inorder to run the code on your computer you will need to have the data and best_randomForest_models folders downloaded.

* I was not able to upload them to github because of file size limit.

* Please refer to the following link for complete files of Mod_5_Project: https://drive.google.com/open?id=17rMuC6UW2KR5iVxQnc_BNP-lqTZmxQCF

* You can download the folder from the link above and start using the dataHandler class to handle crisis data and develop your own models.

* You donot need to pass any parameters to initilize the dataHandler class.

* You will need the data folder to run dataHandler class as it imports the complete dataset from it.

* The dataHandler class has the following functions:

* filter_data: This class can be used to filter through the complete dataset based on any variable of interest. It takes in values such as country, region, year etc to filter the complete data set against. It returns a dataFrame after all the filters has been applied. 

* random_forest: It takes in the dataframe you want to create the random forest model for. It also takes in random_forest parameters that you might want to set while creating the model. If no parameters for random forest model are passed, it will automatically do a grid search to find the best set of parameters for the model. It also takes an optional parameter model_name, which you should pass if you want to save your model after being constructed. All random forest models are saved in the best_randomForest_models folder. While saving a model "_model.sav" is automatically added to the end of the saved file name.

* xgboost: It takes in the dataframe you want to create the XGBoost model for.It also takes in XGBoost parameters that you might want to set while creating the model. If no parameters for XGBoost are passed, it will run XGBoost on standard parameters set by sklearn. It also takes an optional parameter model_name, which you should pass if you want to save your model after being constructed. All random forest models are saved in the xgBoost_models folder. While saving a model "_model.sav" is automatically added to the end of the saved file name.

* classifier_accuracy: It takes the dataframe for which a classification model was constructed and the classification model as parameters. It returns the Accuracy Score, F1 Score, Preceision, and Recall for training and testing data in form of a dictionary. Not the dataset is split into 75% training data and 25% testing data.

* plot_confusion_matrix: It takes the dataframe for which a classification model was constructed and the classification model as parameters. It also takes in dataset_type, which if set to 'train' will return confusion matrix for training dataset and if set to 'test' it will return confusion matrix for testing dataset. Normalizate parameter can be set to true if the results of confusion matrix needs to be normalized. It also takes an optional parameter for the title of the confusion matrix. It plots the confusion matrix for the classification model created.

* load_model: It takes the model_name and model_type inorder to load a model already constructed and saved. Model_type should be set to 'rf' if a random forest needs to be loaded and 'xgb' if a XGBoost model needs to be loaded. In model name you donot need to add '_model.sav' as it is automatically added to it by the function.

* crisis_to_fatalities: It takes in the dataframe for which the crisis to fatatilies graph needs to be constructed. It takes in a 'type' parameter that describes the type of graph that needs to be constructed. If type is set to 'country_stacked', it will return stacked crisis to fataility per country bar plot and if type is set to 'country_paired', it will return a paired crisis to fatility per country bar plot. Likewise, if it is set to 'event_stacked', it will return stacked crisis to fataility per event barplot, and if set to 'event_paired', it will return paired crisis to fataility per event barplot. Finally if type is set to 'crisis map' it will plot the number of crisis on a map.
