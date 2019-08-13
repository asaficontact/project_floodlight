from imports import *
class dh:
    def __init__(self):

        '''
        * NO PARAMETERS REQUIRED FOR INITIALIZATION
        '''

        self.df = self.load_data()




    def load_data(self):

        '''
        * NOT TO BE USED OUTSIDE OF THE CLASS
        * LOADS THE COMPLETE ACLED DATASET FROM THE DATA FOLDER
        * IT IS USED TO GET RIDE OF N/A VALUES AND UNNESSARY COLUMNS
        '''

        df = pd.read_csv('data/complete_dataset.csv')

        df.drop(['data_id', 'event_id_cnty', 'iso', 'event_id_no_cnty',
                'time_precision', 'geo_precision', 'source', 'source_scale',
                'notes', 'iso3'], axis = 1, inplace = True)

        remover_value = len(df) * 0.8

        na_list = df.isna().sum().to_dict()
        for key in na_list:
            if na_list[key] > remover_value:
                df.drop(key, inplace = True, axis = 1)

        df.reset_index(drop=True, inplace=True)
        return df




    def organize_actors(self, df, actor_name = None):

        '''
        * NOT TO BE USED OUTSIDE OF THE CLASS
        * ORGANIZES THE ACTORS OF INTEREST IN THE RIGHT ORDER
        '''

        #Get value count of actors
        filter_value = df.inter1.value_counts().idxmax()
        num_actor1 = df[df['inter1'] == filter_value].actor1.value_counts().to_dict()
        num_actor2 = df[df['inter2'] == filter_value].actor2.value_counts().to_dict()
        total_actors = list(set(list(num_actor1.keys()) + list(num_actor2.keys())))

        if actor_name == None:

            #Find the actors that we want to keep
            keep_class = []
            class_cutter = len(df) * 0.009
            for actor in total_actors:
                if actor in num_actor1 and actor in num_actor2:
                    if num_actor1[actor] + num_actor2[actor] > class_cutter:
                        keep_class.append(actor)

                elif actor in num_actor1:
                    if num_actor1[actor] > class_cutter:
                        keep_class.append(actor)

                else:
                    if num_actor2[actor] > class_cutter:
                        keep_class.append(actor)

            #Get rid of actors we dont want to keep
            df = df[(df.actor1.isin(keep_class)) | (df.actor2.isin(keep_class))]

            #Rearrange columns to switch all actors of interest to actor1 column

            for actor in keep_class:
                actor1 = df[df['actor2'] == actor]['actor1'].copy()
                inter1 = df[df['actor2'] == actor]['inter1'].copy()
                inter2 = df[df['actor2'] == actor]['inter2'].copy()
                actor2 = df[df['actor2'] == actor]['actor2'].copy()

                df.loc[(df['actor2'] == actor), 'actor1'] = actor2.copy()
                df.loc[(df['actor2'] == actor), 'inter1'] = inter2.copy()
                df.loc[(df['actor2'] == actor), 'inter2'] = inter1.copy()
                df.loc[(df['actor2'] == actor), 'actor2'] = actor1.copy()

            return df

        else:
            actor_name = actor_name.title()
            #Rearrange columns to switch actor of interest to actor1 column
            actor1 = df[df['actor2'].str.contains(actor_name)]['actor1'].copy()
            inter1 = df[df['actor2'].str.contains(actor_name)]['inter1'].copy()
            inter2 = df[df['actor2'].str.contains(actor_name)]['inter2'].copy()
            actor2 = df[df['actor2'].str.contains(actor_name)]['actor2'].copy()

            df.loc[(df['actor2'].str.contains(actor_name)), 'actor1'] = actor2.copy()
            df.loc[(df['actor2'].str.contains(actor_name)), 'inter1'] = inter2.copy()
            df.loc[(df['actor2'].str.contains(actor_name)), 'inter2'] = inter1.copy()
            df.loc[(df['actor2'].str.contains(actor_name)), 'actor2'] = actor1.copy()

            df.loc[(df['actor1'].str.contains(actor_name)), 'actor1'] = actor_name
            df.loc[(df['actor1'].str.contains(actor_name)) == False, 'actor1'] = f'Not {actor_name}'
            return df





    def filter_data(self, country = None, year = None, region = None, event_type = None,
                    state_forces = False, rebel_groups = False, political_militias = False,
                    identity_militias = False, rioters = False, protestors = False, civilian = False,
                    other_forces = False, actor_name = None):

        '''
        Parameters:
        * country: the name of country/countries to filter the dataset for [should be passed as list] (Optional)
        * year: the year/years to filter the dataset for [should be passed as list] (Optional)
        * region: the name of region/regions to filter the dataset for [should be passed as list] (Optional)
        * event_type: the name of event_type/event_types to filter the dataset for [should be passed as list] (Optional)
        * state_forces: Set to 'True' to filter for state forces (Optional)
        * rebel_groups: Set to 'True' to filter for rebel groups (Optional)
        * political_militias: Set to 'True' to filter for political militias (Optional)
        * identity_militias: Set to 'True' to filter for identity militias (Optional)
        * rioters: Set to 'True' to filter for rioters (Optional)
        * protestors: Set to 'True' to filter for protestors (Optional)
        * civilian: Set to 'True' to filter for civilian (Optional)
        * other_forces: Set to 'True' to filter for other forces (Optional)
        * actor_name: The name of specific actor you want to filter the data for (Optional)

        Return:
        * filter_df: The dataframe constructed after all filters are applied
        '''

        df = self.df.copy()
        inter_list = list([state_forces, rebel_groups, political_militias, identity_militias, rioters, protestors, civilian, other_forces])
        inter = [i+1 for i in range(0, len(inter_list)) if inter_list[i] == True]
        if sum(inter) == 0:
            inter = list(range(1,9))

        if country == None:
            country = list(df.country.value_counts().to_dict().keys())
        if year == None:
            year = list(df.year.value_counts().to_dict().keys())
        if region == None:
            region = list(df.region.value_counts().to_dict().keys())
        if event_type == None:
            event_type = list(df.event_type.value_counts().to_dict().keys())

        filter_df = df[(df['country'].isin(country)) & (df['year'].isin(year)) &
                            (df['region'].isin(region)) & (df['event_type'].isin(event_type)) &
                            ((df['inter1'].isin(inter)) | (df['inter2'].isin(inter)))]

        remover_value = len(filter_df) * 0.8

        na_list = filter_df.isna().sum().to_dict()
        for key in na_list:
            if na_list[key] > remover_value:
                filter_df.drop(key, inplace = True, axis = 1)

        filter_df.fillna('No actor 2', inplace = True)
        filter_df.reset_index(drop=True, inplace=True)
        if actor_name == None and sum(inter_list) == 0:
            return filter_df
        elif actor_name == None and sum(inter_list) != 0:
            filter_df = self.organize_actors(filter_df.copy())
        else:
            filter_df = self.organize_actors(filter_df.copy(), actor_name = actor_name)
        return filter_df




    def get_train_test(self, df):

        '''
        * NOT TO BE USED OUTSIDE OF THE CLASS
        * GENERATES TRAIN AND TEST DATASETS
        '''

        df = df.copy()
        #Drop unnessary columns
        df.drop(['inter1','country', 'event_date', 'year', 'latitude', 'longitude','timestamp'], inplace = True, axis = 1)

        #Create Training and Testing data
        y = df['actor1']
        x = df.drop(['actor1'], axis = 1)
        x['interaction'] = x.interaction.astype('object')
        x['inter2'] = x.inter2.astype('object')
        x = pd.get_dummies(x)
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.25, random_state = 123)
        return x_train, x_test, y_train, y_test





    def random_forest(self, df, model_name = None, max_depth = None, min_samples_leaf = 1,
                      min_samples_split = 2, n_estimators = 10):

        '''
        Parameters:
        * df: dataframe used for random forest (Required)
        * model_name: name for saving the model [All random forest models are saved in best_randomForest_models folder] (Optional)
        * max_depth: max_depth parameter for random forest (Optional)
        * min_samples_leaf: min_samples_leaf parameter for random forest (Optional)
        * min_samples_split: min_samples_split parameter for random forest (Optional)
        * n_estimators: n_estimators parameter for random forest (Optional)
        * NOTE: if not parameters for random forest are passed a GRID Search is executed to find best parameters

        Return:
        * randomForest_model: the random forest model generated from grid search or the parameters passed
        '''

        x_train, x_test, y_train, y_test = self.get_train_test(df)

        if max_depth == None and min_samples_leaf == 1 and min_samples_split == 2 and n_estimators == 10:

            #Grid Searching
            n_estimators = [100, 300, 500, 800, 1200]
            max_depth = [5, 8, 15, 25, 30]
            min_samples_split = [2, 5, 10, 15, 100]
            min_samples_leaf = [1, 2, 5, 10]

            hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,
                          min_samples_split = min_samples_split,
                         min_samples_leaf = min_samples_leaf)

            forest = RandomForestClassifier()
            gridF = GridSearchCV(forest, hyperF, cv = 3, verbose = 1,
                                  n_jobs = -1)

            bestF = gridF.fit(x_train, y_train)

            if model_name != None:
                model_fileName = f'best_randomForest_models/{model_name}_model.sav'
                pickle.dump(bestF, open(model_fileName, 'wb'))

            return bestF

        else:

            #Random_tree with parameters
            forest = RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth,
                          min_samples_split = min_samples_split,
                         min_samples_leaf = min_samples_leaf)

            customF = forest.fit(x_train, y_train)

            if model_name != None:
                model_fileName = f'best_randomForest_models/{model_name}_model.sav'
                pickle.dump(customF, open(model_fileName, 'wb'))

            return customF




    def xgboost(self, df, max_depth = None, n_estimators = None, model_name = None):

        '''
        Parameters:
        * df: dataframe used for random forest (Required)
        * max_depth: max_depth parameter for XGBoost (Optional)
        * n_estimators: n_estimators parameter for XGBoost (Optional)
        * model_name: name for saving the model [All random forest models are saved in xgBoost_models folder] (Optional)

        Return:
        * xgb_model: the XGBoost model generated
        '''

        if max_depth == None and n_estimators == None:
            clf = xgb.XGBClassifier()
        elif max_depth == None:
            clf = xgb.XGBClassifier(n_estimators = n_estimators)
        elif n_estimators == None:
            clf = xgb.XGBClassifier(max_depth = max_depth)
        else:
            clf = xgb.XGBClassifier(max_depth = max_depth, n_estimators = n_estimators)

        x_train, x_test, y_train, y_test = self.get_train_test(df)

        xgb_model = clf.fit(x_train, y_train)

        if model_name != None:
            model_fileName = f'xgBoost_models/{model_name}_model.sav'
            pickle.dump(xgb_model, open(model_fileName, 'wb'))

        return xgb_model



    def classifier_accuracy(self, df, model):

        '''
        Parameters:
        * df: dataframe used in classification model generation (Required)
        * model: the classification model generated (Required)

        Return:
        * accuracy_result: dictionary of Accuracy Score, F1 Score, Precision, and Recall for both train and test datasets
        '''


        x_train, x_test, y_train, y_test = self.get_train_test(df)
        train_predict = model.predict(x_train)
        test_predict = model.predict(x_test)

        #Accuracy Score
        train_accuracy_score = model.score(x_train, y_train)
        test_accuracy_score = model.score(x_test, y_test)

        #F1 Score
        train_f1_weighted_score = f1_score(y_train, train_predict, average='weighted')
        test_f1_weighted_score = f1_score(y_test, test_predict, average='weighted')

        #Precision_score
        train_precision_weighted_score = precision_score(y_train, train_predict, average = 'weighted')
        test_precision_weighted_score = precision_score(y_test, test_predict, average = 'weighted')

        #Recall Score
        train_recall_weighted_score = recall_score(y_train, train_predict, average = 'weighted')
        test_recall_weighted_score = recall_score(y_test, test_predict, average = 'weighted')


        result = {
        'training_accuracy': train_accuracy_score,
        'testing_accuracy': test_accuracy_score,
        'training_F1_weighted': train_f1_weighted_score,
        'testing_F1_weighted': test_f1_weighted_score,
        'training_precision_weighted': train_precision_weighted_score,
        'testing_precision_weighted': test_precision_weighted_score,
        'training_recall_weighted': train_recall_weighted_score,
        'testing_recall_weighted': test_recall_weighted_score,
        }

        return result





    def plot_confusion_matrix(self, df, model, dataset_type = 'train',
                              normalize = False , title = None,
                              cmap=plt.cm.Blues):

        '''
        Parameters:
        * df: dataframe used in classification model generation (Required)
        * model: the classification model generated (Required)
        * dataset_type: 'train' - confusion matrix for training dataset / 'test' - confusion matrix for testing dataset (Default: 'train')
        * normalize: Set True if confusion matrix needs to be Normalized (Default: False)
        * title: Title for the confusion matrix (Optional)
        '''


        x_train, x_test, y_train, y_test = self.get_train_test(df)

        if dataset_type == 'train':
            y_true = y_train
            y_pred = model.predict(x_train)
        else:
            y_true = y_test
            y_pred = model.predict(x_test)

        classes = list(y_train.value_counts().to_dict().keys())

        if not title:
            if normalize:
                title = 'Normalized confusion matrix'
            else:
                title = 'Confusion matrix, without normalization'

        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        # Only use the labels that appear in the data
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        fig, ax = plt.subplots(figsize = (20,10))
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.figure.colorbar(im, ax=ax)
        # We want to show all ticks...
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               # ... and label them with the respective list entries
               xticklabels=classes, yticklabels=classes,
               title=title,
               ylabel='True label',
               xlabel='Predicted label')

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        fig.tight_layout()
        return ax






    def load_model(self, model_name, model_type = 'rf'):

        '''
        Parameters:
        * model_name: name of model to load (Required)
        * model_type: type of model: 'rf' - Random Forest / 'xgb' - XGBoost (Default: 'rf')

        Return:
        * model: the model that has been loaded
        '''

        if model_type == 'rf':
            model_fileName = f'best_randomForest_models/{model_name}_model.sav'
        else:
            model_fileName = f'xgBoost_models/{model_name}_model.sav'
        model = pickle.load( open( model_fileName, "rb" ) )
        return model





    def crisis_to_fatalities_graph(self, df, type = 'country'):

        '''
        Parameters:
        * df: dataframe used in classification model generation (Required)
        * type:
        'country' - create crisis_to_fatalities_graph per country /
        'event' - create crisis_to_fatalities_graph per event /
        'crisis map' - plot all crisis on a map (Default: 'country')
        '''


        df_graphing = df[df.year > 2016]
        df_graphing.year.value_counts()

        if type == 'country_stacked':
            country_list = list(df_graphing.country.value_counts().to_dict().keys())
            country_list

            crisis = list(df_graphing.country.value_counts().to_dict().values())
            crisis

            fatalities= []
            for country in country_list:
                fatalities.append(df_graphing[df_graphing['country'] == country].fatalities.sum())

            #Create alpha_3 country code for countries that have it so it can fit easily on the x axis
            countries = {}
            for country in pycountry.countries:
                countries[country.name] = country.alpha_3
            codes = [countries.get(country, 'Unknown code') for country in country_list]
            country_list = [country_list[i] if codes[i] == 'Unknown code' else codes[i] for i in range(0,len(country_list))]

            graphing_df = pd.DataFrame({'country': country_list,
                                        'number_of_crisis': crisis,
                                        'fatalities': fatalities})

            plt.figure(figsize = (20,10))
            index = np.arange(len(graphing_df.country))
            p1 = plt.bar(graphing_df.country, graphing_df.fatalities, width = 0.42)
            p2 = plt.bar(graphing_df.country, graphing_df.number_of_crisis, width = 0.42)


            plt.xlabel('Countries', fontsize=10)
            plt.ylabel('Number', fontsize=10)
            plt.xticks(index, graphing_df.country, fontsize=10, rotation=28)
            plt.title('Crisis to Fatalities per Country [2017-2019]')
            plt.legend((p1[0], p2[0]), ('Fatalities', 'Crisis'))

            plt.show()

        elif type == 'country_paired':
            country_list = list(df_graphing.country.value_counts().to_dict().keys())
            country_list

            crisis = list(df_graphing.country.value_counts().to_dict().values())
            crisis

            fatalities= []
            for country in country_list:
                fatalities.append(df_graphing[df_graphing['country'] == country].fatalities.sum())

            #Create alpha_3 country code for countries that have it so it can fit easily on the x axis
            countries = {}
            for country in pycountry.countries:
                countries[country.name] = country.alpha_3
            codes = [countries.get(country, 'Unknown code') for country in country_list]
            country_list = [country_list[i] if codes[i] == 'Unknown code' else codes[i] for i in range(0,len(country_list))]

            graphing_df = pd.DataFrame({'country': country_list,
                                        'number_of_crisis': crisis,
                                        'fatalities': fatalities})

            x = np.arange(len(country_list))
            width = 0.35

            fig, ax = plt.subplots(figsize = (20,10))
            rects1 = ax.bar(x - width/2, graphing_df.fatalities, width, label='Fatalities')
            rects2 = ax.bar(x + width/2, graphing_df.number_of_crisis, width, label='Number of Crisis')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Numbers')
            ax.set_title('Crisis to Fatalities per Country [2017-2019]')
            ax.set_xticks(x)
            ax.set_xticklabels(country_list)
            ax.legend()
            fig.tight_layout()

            plt.show()

        elif type == 'event_stacked':

            event_list = list(df_graphing.event_type.value_counts().to_dict().keys())
            event_list

            crisis = list(df_graphing.event_type.value_counts().to_dict().values())
            crisis

            fatalities= []
            for event in event_list:
                fatalities.append(df_graphing[df_graphing['event_type'] == event].fatalities.sum())

            graphing_df = pd.DataFrame({'event': event_list,
                                        'number_of_crisis': crisis,
                                        'fatalities': fatalities})

            plt.figure(figsize = (20,10))
            index = np.arange(len(graphing_df.event))
            p1 = plt.bar(graphing_df.event, graphing_df.fatalities, width = 0.42)
            p2 = plt.bar(graphing_df.event, graphing_df.number_of_crisis, width = 0.42)


            plt.xlabel('Event Type', fontsize=10)
            plt.ylabel('Number', fontsize=10)
            plt.xticks(index, graphing_df.event, fontsize=10, rotation=28)
            plt.title('Crisis to Fatalities per Event Type [2017-2019]')
            plt.legend((p1[0], p2[0]), ('Fatalities', 'Crisis'))

            plt.show()

        elif type == 'event_paired':

            event_list = list(df_graphing.event_type.value_counts().to_dict().keys())
            event_list

            crisis = list(df_graphing.event_type.value_counts().to_dict().values())
            crisis

            fatalities= []
            for event in event_list:
                fatalities.append(df_graphing[df_graphing['event_type'] == event].fatalities.sum())

            graphing_df = pd.DataFrame({'event': event_list,
                                        'number_of_crisis': crisis,
                                        'fatalities': fatalities})

            x = np.arange(len(event_list))
            width = 0.35

            fig, ax = plt.subplots(figsize = (20,10))
            rects1 = ax.bar(x - width/2, graphing_df.fatalities, width, label='Fatalities')
            rects2 = ax.bar(x + width/2, graphing_df.number_of_crisis, width, label='Number of Crisis')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Numbers')
            ax.set_title('Crisis to Fatalities per Event Type [2017-2019]')
            ax.set_xticks(x)
            ax.set_xticklabels(event_list)
            ax.legend()
            fig.tight_layout()

            plt.show()

        elif type =='crisis map':

            geo_df = df_graphing[['longitude','latitude', 'country']]

            gdf = geopandas.GeoDataFrame(
                geo_df, geometry=geopandas.points_from_xy(geo_df.longitude, geo_df.latitude))

            world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

            if df_graphing.region.str.contains('Africa').sum() > 0 and df_graphing.region.str.contains('Asia').sum() == 0 and df_graphing.region.str.contains('Europe').sum() == 0:

                ax = world[world.continent == 'Africa'].plot(
                    color='white', edgecolor='black', figsize = (20,10))
                gdf.plot(column='country', ax=ax, legend=True, markersize = 5, marker='o')
                plt.show()

            elif df_graphing.region.str.contains('Asia').sum() > 0 and df_graphing.region.str.contains('Africa').sum() == 0 and df_graphing.region.str.contains('Europe').sum() == 0:
                ax = world[world.continent == 'Asia'].plot(
                    color='white', edgecolor='black', figsize = (20,10))
                gdf.plot(column='country', ax=ax, legend=True, markersize = 5, marker='o')
                plt.show()

            elif df_graphing.region.str.contains('Europe').sum() > 0 and df_graphing.region.str.contains('Africa').sum() == 0 and df_graphing.region.str.contains('Asia').sum() == 0:

                ax = world[world.continent == 'Europe'].plot(
                    color='white', edgecolor='black', figsize = (20,10))
                gdf.plot(column='country', ax=ax, legend=True, markersize = 5, marker='o')
                plt.show()

            else:

                ax = world.plot(
                    color='white', edgecolor='black', figsize = (20,10))
                gdf.plot(column='country', ax=ax, legend=True, markersize = 5, marker='o')
                plt.show()
