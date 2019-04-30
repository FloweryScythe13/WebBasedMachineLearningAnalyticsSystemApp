import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from ml_dnnreg.forms import HyperParamForm

def dnn_reg(form: HyperParamForm):
    sampleCsvFile = form.cleaned_data['sampleCsvFile']
    validationSplit = form.cleaned_data['validationSplit']
    learningRate = form.cleaned_data['learningRate']
    momentum = form.cleaned_data['momentum']
    nEpoch = form.cleaned_data['nEpoch']
    batchSize = form.cleaned_data['batchSize']
    seed = form.cleaned_data['seed']
    opAlg = form.cleaned_data['opAlg']
    hiddenLayerNum = form.cleaned_data['hiddenLayerNum']
    h1n1 = form.cleaned_data['h1n1']
    h1n2 = form.cleaned_data['h1n2']
    h1n1Activation = form.cleaned_data['h1n1Activation']
    h1n2Activation = form.cleaned_data['h1n2Activation']
    normalization = form.cleaned_data['normalization']

    dataframe = pd.read_csv(f"media/ml_dnnreg/{str(form.cleaned_data['sampleCsvFile'])}", header=None)
    dataset = dataframe.values

    Y = dataset[:, 0]
    X = dataset[:, 1:dataset.shape[1]]
    sampleSize = len(X)
    nFeatures = X.shape[1]
    YTest = dataset[:, 0]

    # normalization of input data
    if (normalization == "YES"):
        XTest = keras.utils.normalize(X, 1, 2)
    else:
        XTest = X
    print(XTest)

    # fix the random seed for reproducibility
    np.random.seed(seed)

    # Construct the model
    model = Sequential()
    if(opAlg == "SGD"):
        op_ALG = keras.optimizers.SGD(learningRate, momentum, 0.0, False)
    elif(opAlg == "ADAM"):
        op_ALG = keras.optimizers.Adam(learningRate)
    elif(opAlg == "RMSProp"):
        op_ALG = keras.optimizers.RMSprop(learningRate)
    elif(opAlg == "Adadelta"):
        op_ALG = keras.optimizers.Adadelta(learningRate)
    elif(opAlg == "Adagrad"):
        op_ALG = keras.optimizers.Adagrad(learningRate)
    print(op_ALG)

    for n in range(0, hiddenLayerNum-1):
        if n == 0:
            model.add(Dense(h1n1, input_dim=nFeatures, kernel_initializer='normal', activation=h1n1Activation))
        else:
            model.add(Dense(h1n1, kernel_initializer='normal', activation=h1n1Activation))

    model.add(Dense(h1n2, kernel_initializer='normal', activation=h1n2Activation))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer=op_ALG, metrics = ['mean_squared_error', 'mean_absolute_error'])
    model.summary()

    train_history = model.fit(XTest, Y, batchSize, epochs = nEpoch, verbose = 2, validation_split=validationSplit)
    test_predict = model.predict(X)

    predict_actual = []
    deltaSum = 0
    trainSum = 0
    for n in range(0, len(test_predict)):
        predict_actual.append([float("{0:.3f}".format(test_predict[n][0])), Y[n]])
        deltaSum += Y[n] - test_predict[n][0]
        trainSum += test_predict[n][0]

    deltaMean = deltaSum / len(test_predict)
    trainMean = trainSum / len(test_predict)

    # Polynomial Regression
    def polyfit(x, y, degree):
        results = {}
        coeffs = np.polyfit(x, y, degree)

        # Polynomial Coefficients
        results['polynomial'] = coeffs.tolist()

        # r-squared
        p = np.poly1d(coeffs)

        # fit the values, and find mean
        yhat = p(x)
        ybar = np.sum(y)/len(x)
        ssreg = np.sum((yhat-ybar)**2)
        sstot = np.sum((y-ybar)**2)
        results['R2'] = ssreg / sstot

        return results


    test_predict = test_predict[:,0]
    regresult = polyfit(test_predict, YTest, 1)

    return train_history, predict_actual, regresult, model, deltaMean, trainMean