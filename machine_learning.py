import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

Linearfile = pd.read_csv('./files/FuelConsumptionCo2.csv')
def SimpleRegression(df):
    from sklearn import linear_model
    from sklearn.metrics import r2_score

    # definiendo el conjunto de entrenamiento y prueba
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    test = df[~msk]

    # Creando modelo predictivo
    regr = linear_model.LinearRegression()
    train_x = np.asanyarray(train[['ENGINESIZE']])
    train_y = np.asanyarray(train[['CO2EMISSIONS']])
    regr.fit(train_x, train_y)
    # The coefficients
    print('Coefficients: ', regr.coef_)
    print('Intercept: ', regr.intercept_)

    # Salidas
    plt.scatter(train.ENGINESIZE, train.CO2EMISSIONS, color='blue')
    plt.plot(train_x, regr.coef_[0][0] * train_x + regr.intercept_[0], '-r')
    plt.xlabel("Engine size")
    plt.ylabel("Emission")
    plt.show()

    # prediccion
    test_x = np.asanyarray(test[['ENGINESIZE']])
    test_y = np.asanyarray(test[['CO2EMISSIONS']])
    test_y_ = regr.predict(test_x)
    #print("Prediccion: ", test_y)
    print("Error medio absoluto: %.2f" % np.mean(np.absolute(test_y_ - test_y)))
    print("Suma residual de los cuadrados (MSE): %.2f" % np.mean((test_y_ - test_y) ** 2))
    print("R2-score: %.2f" % r2_score(test_y_, test_y))

def MultipleRegression(df):
    from sklearn import linear_model

    # definiendo el conjunto de entrenamiento y prueba
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    test = df[~msk]

    # Creando modelo predictivo
    regr = linear_model.LinearRegression()
    x = np.asanyarray(train[['ENGINESIZE', 'CYLINDERS', 'FUELCONSUMPTION_COMB']])
    y = np.asanyarray(train[['CO2EMISSIONS']])
    regr.fit(x, y)
    print('Coefficients: ', regr.coef_)

    # Prediccion
    y_hat = regr.predict(test[['ENGINESIZE', 'CYLINDERS', 'FUELCONSUMPTION_COMB']])
    x = np.asanyarray(test[['ENGINESIZE', 'CYLINDERS', 'FUELCONSUMPTION_COMB']])
    y = np.asanyarray(test[['CO2EMISSIONS']])
    #print(y_hat)
    print("Residual sum of squares: %.2f" % np.mean((y_hat - y) ** 2))
    print('Variance score: %.2f' % regr.score(x, y))

    return 0

NoLinearFile = pd.read_csv('./files/china_gdp.csv')
def NoLinealRegression(df):
    from scipy.optimize import curve_fit

    def sigmoid(x, Beta_1, Beta_2):
        y = 1 / (1 + np.exp(-Beta_1 * (x - Beta_2)))
        return y

    x_data, y_data = (df["Year"].values, df["Value"].values)
    beta_1 = 0.10
    beta_2 = 1990.0

    # función logística
    Y_pred = sigmoid(x_data, beta_1, beta_2)

    # predicción de puntos
    plt.plot(x_data, Y_pred * 15000000000000.)
    plt.plot(x_data, y_data, 'ro')
    #plt.show()

    # Normalizando los datos
    xdata = x_data / max(x_data)
    ydata = y_data / max(y_data)

    popt, pcov = curve_fit(sigmoid, xdata, ydata)
    print(" beta_1 = %f, beta_2 = %f" % (popt[0], popt[1]))

    # Modelo predicho
    x = np.linspace(1960, 2015, 55)
    x = x / max(x)
    plt.figure(figsize=(8, 5))
    y = sigmoid(x, *popt)
    plt.plot(xdata, ydata, 'ro', label='data')
    plt.plot(x, y, linewidth=3.0, label='fit')
    plt.legend(loc='best')
    plt.ylabel('GDP')
    plt.xlabel('Year')
    plt.show()

PolinomicalFile = pd.read_csv('./files/ChurnData.csv')
def PolinomicalRegression(df):
    from sklearn import preprocessing
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix

    # Eligiendo las columnas
    X = np.asarray(df[['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip']])
    y = np.asarray(df['churn'])

    # Normalizando los datos
    X = preprocessing.StandardScaler().fit(X).transform(X)

    # Diviiendo el conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
    print('Train set:', X_train.shape, y_train.shape)
    print('Test set:', X_test.shape, y_test.shape)

    # Creando el modelo y prediciendo
    LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train, y_train)
    yhat = LR.predict(X_test)
    yhat_prob = LR.predict_proba(X_test)
    return 0

knnFile = pd.read_csv('./files/teleCust1000t.csv')
def Knn(df):
    from sklearn import preprocessing
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn import metrics

    X = df[['region', 'tenure', 'age', 'marital', 'address', 'income', 'ed', 'employ', 'retire', 'gender', 'reside']].values
    y = df['custcat'].values

    # normalizando
    X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))

    # Separando conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
    print('Set de Entrenamiento:', X_train.shape, y_train.shape)
    print('Set de Prueba:', X_test.shape, y_test.shape)

    # Entrenamiento con el modelo
    k = 4
    neigh = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)

    # Prediccion
    yhat = neigh.predict(X_test)

    # Evaluacion
    print("Entrenar el set de Certeza: ", metrics.accuracy_score(y_train, neigh.predict(X_train)))
    print("Probar el set de Certeza: ", metrics.accuracy_score(y_test, yhat))

kmeansFile = pd.read_csv('./files/Cust_Segmentation.csv')
def Kmeans(df):
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # eliminando columnas categoricas
    df = df.drop('Address', axis=1)

    # normalizando
    X = df.values[:, 1:]
    X = np.nan_to_num(X)
    Clus_dataSet = StandardScaler().fit_transform(X)

    # Modelando
    clusterNum = 3
    k_means = KMeans(init="k-means++", n_clusters=clusterNum, n_init=12)
    k_means.fit(X)
    labels = k_means.labels_

    # Etiquetas
    df["Clus_km"] = labels

    # Distribucion grafica
    area = np.pi * (X[:, 1]) ** 2
    plt.scatter(X[:, 0], X[:, 3], s=area, c=labels.astype(np.float), alpha=0.5)
    plt.xlabel('Age', fontsize=18)
    plt.ylabel('Income', fontsize=16)
    #plt.show()

treeFile = pd.read_csv('./files/drug200.csv')
def DecisionTree(df):
    from sklearn import preprocessing
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn import metrics
    import matplotlib.pyplot as plt

    # preprocesamiento. Convirtiendo variables categoricas a numericas
    X = df[['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']].values

    le_sex = preprocessing.LabelEncoder()
    le_sex.fit(['F','M'])
    X[:,1] = le_sex.transform(X[:,1])

    le_BP = preprocessing.LabelEncoder()
    le_BP.fit([ 'LOW', 'NORMAL', 'HIGH'])
    X[:,2] = le_BP.transform(X[:,2])

    le_Chol = preprocessing.LabelEncoder()
    le_Chol.fit([ 'NORMAL', 'HIGH'])
    X[:,3] = le_Chol.transform(X[:,3])

    y = df["Drug"]

    # Diviendo el conjunto de entrenamiento y prueba
    X_trainset, X_testset, y_trainset, y_testset = train_test_split(X, y, test_size=0.3, random_state=3)

    # Modelo y ajuste
    drugTree = DecisionTreeClassifier(criterion="entropy", max_depth=4)
    drugTree.fit(X_trainset,y_trainset)

    # prediccion
    predTree = drugTree.predict(X_testset)

    # Evaluacion
    print("Precisión de los Arboles de Decisión: ", metrics.accuracy_score(y_testset, predTree))

    from io import StringIO
    import pydotplus
    import matplotlib.image as mpimg
    from sklearn import tree
    dot_data = StringIO()
    filename = "drugtree.png"
    featureNames = df.columns[0:5]
    targetNames = df["Drug"].unique().tolist()
    out = tree.export_graphviz(drugTree, feature_names=featureNames, out_file=dot_data, class_names=np.unique(y_trainset), filled=True, special_characters=True, rotate=False)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(filename)
    img = mpimg.imread(filename)
    plt.figure(figsize=(100, 200))
    plt.imshow(img, interpolation='nearest')


DecisionTree(treeFile)
