import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression

def calcLoss(model, data):
    return np.sum([(model.predict(np.array([entry[0:-1]])) - entry[-1])**2 for entry in data])

def SVM(LabelledData, query):
    LabelledData = np.array(LabelledData)
    y = LabelledData[:,-1]
    X = LabelledData[:,:-1]
    reg = make_pipeline(StandardScaler(), SVR(kernel='linear', max_iter=500))
    reg.fit(X, y)
    return reg.predict(query), calcLoss(reg, LabelledData)

def SGD(LabelledData, query):
    LabelledData = np.array(LabelledData)
    y = LabelledData[:,-1]
    X = LabelledData[:,:-1]
    reg = make_pipeline(StandardScaler(), SGDRegressor(max_iter=1000, tol=1e-3))
    reg.fit(X, y)
    return reg.predict(query), calcLoss(reg, LabelledData)

def DNN_RELU(LabelledData, query):
    LabelledData = np.array(LabelledData)
    y = LabelledData[:,-1]
    X = LabelledData[:,:-1]
    regr = MLPRegressor(hidden_layer_sizes=(514, 256, 128, 64, 32, 16), max_iter=200, tol=1e-3, solver='adam', activation='relu')
    regr.fit(X, y)
    return regr.predict(query), calcLoss(regr, LabelledData)

def DNN_IDN(LabelledData, query):
    LabelledData = np.array(LabelledData)
    y = LabelledData[:,-1]
    X = LabelledData[:,:-1]
    regr = MLPRegressor(hidden_layer_sizes=(514, 256, 128, 64, 32, 16), max_iter=200, tol=1e-3, solver='adam', activation='identity')
    regr.fit(X, y)
    return regr.predict(query), calcLoss(regr, LabelledData)

def SVD(LabelledData, query):
    LabelledData = np.array(LabelledData)
    y = LabelledData[:,-1]
    X = LabelledData[:,:-1]
    regr = PLSRegression(n_components=15)
    regr.fit(X, y)
    return regr.predict(query), calcLoss(regr, LabelledData)