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

def createEnviroment():
    from azureml.core import Environment
    env = Environment.from_conda_specification(name='training_environment',  file_path='./conda.yml')

def createComputeTarget():
    from azureml.core import Workspace
    from azureml.core.compute import ComputeTarget, AmlCompute

    # Load the workspace from the saved config file
    ws = Workspace.from_config()

    # Specify a name for the compute (unique within the workspace)
    compute_name = 'aml-cluster'

    # Define compute configuration
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2',
                                                           min_nodes=0, max_nodes=4,
                                                           vm_priority='dedicated')

    # Create the compute
    aml_cluster = ComputeTarget.create(ws, compute_name, compute_config)
    aml_cluster.wait_for_completion(show_output=True)

def attachComputeTarget():
    from azureml.core import Workspace
    from azureml.core.compute import ComputeTarget, DatabricksCompute

    # Load the workspace from the saved config file
    ws = Workspace.from_config()

    # Specify a name for the compute (unique within the workspace)
    compute_name = 'db_cluster'

    # Define configuration for existing Azure Databricks cluster
    db_workspace_name = 'db_workspace'
    db_resource_group = 'db_resource_group'
    db_access_token = '1234-abc-5678-defg-90...'
    db_config = DatabricksCompute.attach_configuration(resource_group=db_resource_group,
                                                       workspace_name=db_workspace_name,
                                                       access_token=db_access_token)

    # Create the compute
    databricks_compute = ComputeTarget.attach(ws, compute_name, db_config)
    databricks_compute.wait_for_completion(True)

def checkComputeTarget():
    from azureml.core.compute import ComputeTarget, AmlCompute
    from azureml.core.compute_target import ComputeTargetException

    compute_name = "aml-cluster"

    # Check if the compute target exists
    try:
        aml_cluster = ComputeTarget(workspace=ws, name=compute_name)
        print('Found existing cluster.')
    except ComputeTargetException:
        # If not, create it
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2',
                                                               max_nodes=4)
        aml_cluster = ComputeTarget.create(ws, compute_name, compute_config)

    aml_cluster.wait_for_completion(show_output=True)

def SelectComputeTarget():
    from azureml.core import Environment, ScriptRunConfig

    compute_name = 'aml-cluster'

    training_env = Environment.get(workspace=ws, name='training_environment')

    script_config = ScriptRunConfig(source_directory='my_dir',
                                    script='script.py',
                                    environment=training_env,
                                    compute_target=compute_name)

def deployModel():
    from azureml.core import Model

    classification_model = Model.register(workspace=ws,
                                          model_name='amlstudio-predict-auto-price',
                                          description='A classification model')

def samplig():
    from azureml.train.hyperdrive import GridParameterSampling, choice

    param_space = {
        '--batch_size': choice(16, 32, 64),
        '--learning_rate': choice(0.01, 0.1, 1.0)   # grid sampling
        #'--learning_rate': normal(10, 3)   # random
        #'--learning_rate': uniform(0.05, 0.1)  # Bayesian

    }

    param_sampling = GridParameterSampling(param_space)

def early_termination():
    from azureml.train.hyperdrive import BanditPolicy

    # bandit policy
    early_termination_policy = BanditPolicy(slack_amount=0.2,
                                            evaluation_interval=1,
                                            delay_evaluation=5)

    # median stopping policy
    early_termination_policy = MedianStoppingPolicy(evaluation_interval=1,
                                                    delay_evaluation=5)

    # Truncation selection policy

    early_termination_policy = TruncationSelectionPolicy(truncation_percentage=10,
                                                         evaluation_interval=1,
                                                         delay_evaluation=5)

def differential_privacy():
    '''
    Agregar ruido a los datos para incluir aleatoridad al analisis, no determinista

    A lower epsilon reduces the impact of an individual's data on aggregated results, increasing privacy and reducing accuracy
    '''

def feature_importance():
    '''
    Model explainers use statistical techniques to calculate feature importance.
     This enables you to quantify the relative influence each feature in the training dataset has on label prediction.
    Explainers work by evaluating a test data set of feature cases and the labels the model predicts for them.
    MimicExplainer - An explainer that creates a global surrogate model that approximates your trained model and can be used to generate explanations. This explainable model must have the same kind of architecture as your trained model (for example, linear or tree-based).
    TabularExplainer - An explainer that acts as a wrapper around various SHAP explainer algorithms, automatically choosing the one that is most appropriate for your model ar74   chitecture.
    PFIExplainer - a Permutation Feature Importance explainer that analyzes feature importance by shuffling feature values and measuring the impact on prediction performance.
    '''
    # MimicExplainer
    from interpret.ext.blackbox import MimicExplainer
    from interpret.ext.glassbox import DecisionTreeExplainableModel

    mim_explainer = MimicExplainer(model=loan_model,
                                   initialization_examples=X_test,
                                   explainable_model=DecisionTreeExplainableModel,
                                   features=['loan_amount', 'income', 'age', 'marital_status'],
                                   classes=['reject', 'approve'])

    # TabularExplainer
    from interpret.ext.blackbox import TabularExplainer

    tab_explainer = TabularExplainer(model=loan_model,
                                     initialization_examples=X_test,
                                     features=['loan_amount', 'income', 'age', 'marital_status'],
                                     classes=['reject', 'approve'])

    # PFIExplainer
    from interpret.ext.blackbox import PFIExplainer

    pfi_explainer = PFIExplainer(model=loan_model,
                                 features=['loan_amount', 'income', 'age', 'marital_status'],
                                 classes=['reject', 'approve'])

    #Explaining global feature importance

    # MimicExplainer
    global_mim_explanation = mim_explainer.explain_global(X_train)
    global_mim_feature_importance = global_mim_explanation.get_feature_importance_dict()

    # TabularExplainer
    global_tab_explanation = tab_explainer.explain_global(X_train)
    global_tab_feature_importance = global_tab_explanation.get_feature_importance_dict()

    # PFIExplainer
    global_pfi_explanation = pfi_explainer.explain_global(X_train, y_train)
    global_pfi_feature_importance = global_pfi_explanation.get_feature_importance_dict()

    # Explaining local feature importance

    # MimicExplainer
    local_mim_explanation = mim_explainer.explain_local(X_test[0:5])
    local_mim_features = local_mim_explanation.get_ranked_local_names()
    local_mim_importance = local_mim_explanation.get_ranked_local_values()

    # TabularExplainer
    local_tab_explanation = tab_explainer.explain_local(X_test[0:5])
    local_tab_features = local_tab_explanation.get_ranked_local_names()
    local_tab_importance = local_tab_explanation.get_ranked_local_values()

def createExplainer():
    # Import Azure ML run library
    from azureml.core.run import Run
    from azureml.contrib.interpret.explanation.explanation_client import ExplanationClient
    from interpret.ext.blackbox import TabularExplainer
    # other imports as required

    # Get the experiment run context
    run = Run.get_context()

    # code to train model goes here

    # Get explanation
    explainer = TabularExplainer(model, X_train, features=features, classes=labels)
    explanation = explainer.explain_global(X_test)

    # Get an Explanation Client and upload the explanation
    explain_client = ExplanationClient.from_run(run)
    explain_client.upload_model_explanation(explanation, comment='Tabular Explanation')

    # Complete the run
    run.complete()

    # viweing the explanation

    from azureml.contrib.interpret.explanation.explanation_client import ExplanationClient

    client = ExplanationClient.from_run_id(workspace=ws,
                                           experiment_name=experiment.experiment_name,
                                           run_id=run.id)
    explanation = client.download_model_explanation()