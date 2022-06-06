from azureml.core import Workspace
'''
ws = Workspace.get(name='aml-workspace',
                   subscription_id='1234567-abcde-890-fgh...',
                   resource_group='aml-resources')
'''
ws = Workspace.from_config()
def targets():
    '''
    what configuration have the azure ml
    '''
    ws = Workspace.from_config()

    for compute_name in ws.compute_targets:
        compute = ws.compute_targets[compute_name]
        print(compute.name, ":", compute.type)

def experiment():
    '''
    how to run a experiment in azure ml
    '''
    from azureml.core import Run
    import pandas as pd
    import matplotlib.pyplot as plt
    import os

    # Get the experiment run context
    run = Run.get_context()

    # load the diabetes dataset
    data = pd.read_csv('data.csv')

    # Count the rows and log the result
    row_count = (len(data))
    run.log('observations', row_count)

    # Save a sample of the data
    os.makedirs('outputs', exist_ok=True)
    data.sample(100).to_csv("outputs/sample.csv", index=False, header=True)

    # Complete the run
    run.complete()

def trainScript():
    from azureml.core import Run
    import pandas as pd
    import numpy as np
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    import os
    # Get the experiment run context
    run = Run.get_context()

    # Prepare the dataset
    diabetes = pd.read_csv('Diabetes.csv')
    print(diabetes.columns)
    print(diabetes.head())
    X, y = diabetes[['DiabetesPedigreeFunction', 'Glucose', 'BloodPressure', 'SkinThickness']].values, diabetes['Outcome'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    # Train a logistic regression model
    reg = 0.1
    model = LogisticRegression(C=1 / reg, solver="liblinear").fit(X_train, y_train)

    # calculate accuracy
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    run.log('Accuracy', np.float(acc))

    # Save the trained model
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(value=model, filename='outputs/model.pkl')

    run.complete()

def datastore():
    from azureml.core import Workspace, Datastore

    # ---------------------------- Register a new datastore ----------------------------
    blob_ds = Datastore.register_azure_blob_container(workspace=ws,
                                                      datastore_name='dataStore_new',
                                                      container_name='azureml-blobstore-a8ce0b70-0183-490f-a84f-c20fb2e7baad',
                                                      account_name='mlworkspace0981489189',
                                                      account_key='kNerR7KlKax2oa8rHjVDfVK3zqxMSjEpxSNuv0puedlbZVAb/aTDYwCxvO69G/QrHW84t+Tbq9zM+AStT+OBug==')
    # ----------------------------------------------------------------------------------
    # list of datastores avalibles
    for ds_name in ws.datastores:
        print(ds_name)

    # configuration of the datastore selected
    blob_store = Datastore.get(ws, datastore_name='workspaceblobstore')
    print(blob_store)

def createDataset():
    from azureml.core import Dataset
    from azureml.core import Datastore

    blob_ds = Datastore.get(ws, datastore_name='dataStore_new')
    tab_ds = Dataset.Tabular.from_delimited_files(path=(blob_ds,'diabetes.csv'))
    #file_ds = Dataset.File.from_files(path=(blob_ds, 'data/files/images/*.jpg'))
    tab_ds.register(workspace=ws, name='csv_table')

def getDataset():
    import azureml.core
    from azureml.core import Workspace, Dataset

    # Load the workspace from the saved config file
    ws = Workspace.from_config()

    # Get a dataset from the workspace datasets collection
    ds1 = ws.datasets['csv_table']

    # Get a dataset by name from the datasets class
    ds2 = Dataset.get_by_name(ws, 'img_files')
    #img_ds = Dataset.get_by_name(workspace=ws, name='img_files', version=2)


print(createDataset())