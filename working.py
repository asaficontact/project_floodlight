from imports import *

from dataHandler import dh

df = pd.read_csv('data/complete_dataset.csv')

data = dh(df)

x_train, x_test, y_train, y_test = data.get_train_test(asia_df)

x_train.columns
data.df.region.value_counts()

southern_asia_df = data.filter_data(region=['Southern Asia'], rebel_groups=True)
middle_east_df = data.filter_data(region=['Middle East'], rebel_groups=True)
asia_df = data.filter_data(region=['Middle East', 'Southern Asia'], rebel_groups=True)
europe_df = data.filter_data(region=['Europe'], rebel_groups=True)


asia_rf = data.load_model('asia')
southern_asia_rf = data.load_model('southern_asia')
asia_rf.best_params_

southern_asia_rf.best_params_

asia_xgb = data.xgboost(asia_df, 30, 300)
asia_xgb
asia_xgb_accuracy = data.random_forest_accuracy(asia_df, asia_xgb)

asia_rf_accuracy = data.random_forest_accuracy(asia_df, asia_rf)
asia_rf_accuracy

southern_asia_rf_accuracy = data.random_forest_accuracy(southern_asia_df, southern_asia_rf)
southern_asia_rf_accuracy






asia_rf = data.random_forest(asia_df, 'asia')

europe_rf = data.random_forest(europe_df, 'euorpe')
southern_asia_rf = data.random_forest(southern_asia_df, 'southern_asia')
#Still Need to Run
middle_east_rf = data.random_forest(middle_east_df, 'middle_east'

asia_rf_accuracy = data.plot_confusion_matrix(asia_df, asia_rf)

asia_rf_accuracy = data.plot_confusion_matrix(asia_df, asia_rf, normalize=True)

data.plot_confusion_matrix(asia_df, asia_rf, 'test', normalize=True)

data.plot_confusion_matrix(southern_asia_df, southern_asia_rf, normalize=True)

data.plot_confusion_matrix(southern_asia_df, southern_asia_rf, 'test', normalize=True)

data.df.columns

x_model = pickle.load( open( "best_randomForest_models/asia_model.sav", "rb" ) )
x_model.best_params_

y_model = pickle.load( open( "best_randomForest_models/southern_asia_model.sav", "rb" ) )
y_model.best_params_

z_model = pickle.load( open( "best_randomForest_models/euorpe_model.sav", "rb" ) )
z_model.best_params_




afg_df = data.filter_data(country=['Afghanistan'], rebel_groups=True)

afg_df.inter1.value_counts()
afg_df.year.value_counts()
afg_df.event_type.value_counts()
afg_df.sub_event_type.value_counts()
afg_df.actor1.value_counts()

afg_df.actor2.value_counts()

afg_df.inter1.value_counts()


afg_df.inter2.value_counts()




afg_df.interaction.value_counts()

len(afg_df)
afg_df.fatalities.sum()

actor_interest = 'Taliban'

#####

x = afg_df[afg_df['inter1'] == 2].actor1.value_counts().to_dict()


y = afg_df[afg_df['inter2'] == 2].actor2.value_counts().to_dict()

z = list(set(list(x.keys()) + list(y.keys())))
keep_class = []
class_cutter = len(afg_df) * 0.009
for actor in z:
    if actor in x and actor in y:
        if x[actor] + y[actor] > class_cutter:
            keep_class.append(actor)

    elif actor in x:
        if x[actor] > class_cutter:
            keep_class.append(actor)

    else:
        if y[actor] > class_cutter:
            keep_class.append(actor)


afg_df = afg_df[(afg_df.actor1.isin(keep_class)) | (afg_df.actor2.isin(keep_class))]


for actor in tqdm.tqdm(keep_class):
    actor1 = afg_df[afg_df['actor2'] == actor]['actor1'].copy()
    inter1 = afg_df[afg_df['actor2'] == actor]['inter1'].copy()
    inter2 = afg_df[afg_df['actor2'] == actor]['inter2'].copy()
    actor2 = afg_df[afg_df['actor2'] == actor]['actor2'].copy()


    afg_df.loc[(afg_df['actor2'] == actor), 'actor1'] = actor2.copy()
    afg_df.loc[(afg_df['actor2'] == actor), 'inter1'] = inter2.copy()
    afg_df.loc[(afg_df['actor2'] == actor), 'inter2'] = inter1.copy()
    afg_df.loc[(afg_df['actor2'] == actor), 'actor2'] = actor1.copy()


len(afg_df)


############################ Searching for best parameters #####################

#Set up
afg_df.columns

afg_df.drop(['inter1', 'country', 'event_date', 'year', 'latitude', 'longitude','timestamp', 'interaction'], inplace = True, axis = 1)

y = afg_df['actor1']
x = afg_df.drop(['actor1'], axis = 1)


x['interaction'] = x.interaction.astype('object')
x['inter2'] = x.inter2.astype('object')
x = pd.get_dummies(x)
len(x.columns)
len(x)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state = 123)


from sklearn.model_selection import GridSearchCV
n_estimators = [100, 300, 500, 800, 1200]
max_depth = [5, 8, 15, 25, 30]
min_samples_split = [2, 5, 10, 15, 100]
min_samples_leaf = [1, 2, 5, 10]

hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,
              min_samples_split = min_samples_split,
             min_samples_leaf = min_samples_leaf)

forest = RandomForestClassifier(max_depth = 30, min_samples_split= 10, min_samples_leaf = 1, n_estimators=500)
gridF = GridSearchCV(forest, hyperF, cv = 3, verbose = 1,
                      n_jobs = -1)
bestF = gridF.fit(x_train, y_train)



y.value_counts()

bestF.score(x_train, y_train)
bestF.score(x_test, y_test)

bestF.best_params_
y_train.value_counts()

x = bestF.best_params_
x


forest.fit(x_train, y_train)

forest.score(x_train, y_train)
forest.score(x_test, y_test)

list(y.value_counts().to_dict().keys())

len(y)

plt.imshow(cnf_matrix,  cmap=plt.cm.Blues) #Create the basic matrix.

#Add title and Axis Labels
plt.title('Confusion Matrix')
plt.ylabel('True label')
plt.xlabel('Predicted label')
y_predict = forest.predict(x_train)
y_predict_test = forest.predict(x_test)

from sklearn.metrics import f1_score

f1_score(y_train, y_predict, average='weighted')
f1_score(y_test, y_predict_test, average='weighted')

f1_score(y_train, y_predict, average=None)
f1_score(y_test, y_predict_test, average=None)



plot_confusion_matrix(y_train,y_predict,list(y.value_counts().to_dict().keys()))

plot_confusion_matrix(y_test,y_predict_test,list(y.value_counts().to_dict().keys()))


afg_df1 = afg_df[afg_df['actor1'] != 'Taliban and/or Islamic State (Afghanistan)']

y1 = afg_df1['actor1']
x1 = afg_df1.drop(['actor1'], axis = 1)


x1['interaction'] = x.interaction.astype('object')
x1['inter2'] = x.inter2.astype('object')
x1 = pd.get_dummies(x1)
len(x1.columns)
len(x1)
x1_train, x1_test, y1_train, y1_test = train_test_split(x1,y1, test_size = 0.3, random_state = 123)
forest.fit(x1_train, y1_train)


forest.score(x1_train, y1_train)
forest.score(x1_test, y1_test)
y1_predict = forest.predict(x1_train)
y1_predict_test = forest.predict(x1_test)

f1_score(y1_train, y1_predict, average='weighted')
f1_score(y1_test, y1_predict_test, average='weighted')

f1_score(y1_train, y1_predict, average=None)
f1_score(y1_test, y1_predict_test, average=None)

plot_confusion_matrix(y1_train,y1_predict,list(y.value_counts().to_dict().keys()))

plot_confusion_matrix(y1_test,y1_predict_test,list(y.value_counts().to_dict().keys()))



from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
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
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots(figsize = (12,8))
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






taliban_list = []
taliban_inter_list = []
non_taliban_list = []
non_taliban_inter_list = []






for i in range(0, len(afg_df)):
    if afg_df.actor2[i] == 'Taliban':
        taliban_list.append(afg_df.actor2[i])
        taliban_inter_list.append(afg_df.inter2[i])

        non_taliban_list.append(afg_df.actor1[i])
        non_taliban_inter_list.append(afg_df.inter1[i])
    elif afg_df.actor1[i] == 'Taliban':
        taliban_list.append(afg_df.actor1[i])
        taliban_inter_list.append(afg_df.inter1[i])

        non_taliban_list.append(afg_df.actor2[i])
        non_taliban_inter_list.append(afg_df.inter2[i])
    else:
        taliban_list.append('Not Taliban')
        taliban_inter_list.append(afg_df.inter1[i])

        non_taliban_list.append(afg_df.actor2[i])
        non_taliban_inter_list.append(afg_df.inter2[i])


afg_df['actor1'] = taliban_list
afg_df['inter1'] = taliban_inter_list

afg_df['actor2'] = non_taliban_list
afg_df['inter2'] = non_taliban_inter_list

len(afg_df)
afg_df.actor1.value_counts()


#Model Setup
afg_df.interaction.value_counts()

afg_df[afg_df.interaction == ]['actor1'].value_counts()



afg_df.columns

afg_df.drop(['inter1', 'country'], inplace = True, axis = 1)

y = afg_df['actor1']
x = afg_df.drop(['actor1'], axis = 1)
x.drop(['event_date', 'year', 'admin1', 'admin2', 'latitude', 'longitude', 'timestamp'], inplace = True, axis = 1)

x['interaction'] = x.interaction.astype('object')
x['inter2'] = x.inter2.astype('object')
x.info()
x = pd.get_dummies(x)
len(x.columns)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.25, random_state = 123)

forest = RandomForestClassifier(n_estimators=100, max_depth=15)
forest.fit(x_train, y_train)


forest.score(x_train, y_train)


forest.score(x_test, y_test)


afg_df.duplicated(keep = 'last').sum()

def plot_feature_importances(model, x_train):
    n_features = x_train.shape[1]
    plt.figure(figsize=(8,8))
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), x_train.columns.values)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")

plot_feature_importances(forest, x_train)

asia_rf.best_params_


asia_xgb = xbg(XGBClassifier)
#XG Boost

clf = xgb.XGBClassifier()
clf.fit(x_train, y_train)

training_preds = clf.predict(x_train)

val_preds = clf.predict(x_test)
training_accuracy = accuracy_score(y_train, training_preds)
val_accuracy = accuracy_score(y_test, val_preds)

print("Training Accuracy: {:.4}%".format(training_accuracy * 100))
print("Validation accuracy: {:.4}%".format(val_accuracy * 100))




#TPOT
y_train
from tpot import TPOTClassifier

pipeline_optimizer = TPOTClassifier(generations=5, population_size=20, cv=5,
                                    random_state=42, verbosity=2)

pipeline_optimizer.fit(x_train, y_train)
