from django.shortcuts import render
import os, io, sys, datetime, json
from pathlib import Path
import os.path
from django.conf import settings
from django.db import models
import pandas
import keras
from keras import backend as KB
from keras.models import model_from_json
from ml_dnnreg.forms import HyperParamForm, SaveModelForm, ModelFileNameForm, ModelPredictForm
from ml_dnnreg.mlalg import dnn_reg
from ml_dnnreg.models import PredictModel, SaveModel, ModelFileName

# Instructions To Self:
'''
This file will hold the following methods: 
    Index - should render the ml_dnnreg html template
    Prediction - should receive an input file in a POST request, create a SaveModelForm
        out of it, open the file referenced by the form request in media/ml_dnnreg/dnn_model, load the file and build the 
        model from the file, read the input file's data into a dataset for testing, execute the model's predict function on the 
        dataset, receive the results into the normal variables like predict_actual and train_history, load those variables
        into a PredictModel, and then return all of the results.

    TrainModel - should receive in a POST request a training data input file and a form of HyperParam configuration values. Create a neural network model and train it on the 
       input data by running the input form through the dnn_reg function defined in the 
       mlalg analysis file. Create a prediction table from the received predict_actual array using PredictModel. Save the new model and its results using SaveModel, then save a model weight file, training history file, prediction model file, and regression result file to the media/ml_dnnreg/dnn_model folder out of the other corresponding models. Clear the Keras session so that calling this function repeatedly won't fail. Render the trainmodel html template with associated data from the finished model results.
    RepositoryReview - should render the repositoryReview html template that lists all saved model files. If receiving a POST method, it should retrieve the name of the model file from the form's modelFile property, read the identified file and load it into a model variable, read the data from each of the other corresponding files (model weight, training history, etc) into variables, and send that data back to the UI

'''

def index(request):
    return render(request, 'ml_dnnreg/home.html')

def trainModel(request):
    print("trainModel was called")
    if request.method == 'POST':
        form = HyperParamForm(request.POST, request.FILES)
        if form.is_valid():
            # Run the input through the deep neural network regression analysis
            train_history, predict_actual, regresult, mlmodel, deltaMean, trainMean = dnn_reg(form)

            PredictModel.objects.all().delete()

            for n in range(0, len(predict_actual)):
                # See here for some explanation of this odd syntax: https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.create
                PredictModel.objects.create(number=n+1, prediction = predict_actual[n][0], actual = predict_actual[n][1], delta = (predict_actual[n][0] - predict_actual[n][1]))

            allObjects = PredictModel.objects.all()

            # Books says redirect model.summary() result as string parameter, but why do we have to do this here?
            origStdOut = sys.stdout
            outputBuff = io.StringIO()
            sys.stdout = outputBuff
            mlmodel.summary()
            sys.stdout = origStdOut
            model_summary = outputBuff.getvalue().splitlines(True)
            outputBuff.close()

            model_json = mlmodel.to_json()

            try:
                # Save the model and its results here

                now = str(datetime.datetime.now().isoformat())
                filename_datetime_portion = f"{now[:13]}H{now[14:16]}M{now[17:19]}"
                model_filename = f"dnnreg_model_{filename_datetime_portion}.json"
                model_weight_filename = f"dnnreg_model_{filename_datetime_portion}.h5"
                th_filename = f"trainhistory_{filename_datetime_portion}.json"
                pm_filename = f"predictmodel_{filename_datetime_portion}.json"
                reg_filename = f"regresult_{filename_datetime_portion}.json"
                print(model_filename)

                saveModel = SaveModel.objects.create(modelFile = model_filename, train_history = th_filename, predict_model = pm_filename,
                              regresultFile = reg_filename,
                              deltaMean = deltaMean,
                              trainMean = trainMean,
                              validationSplit = form.cleaned_data['validationSplit'],
                              learningRate = form.cleaned_data['learningRate'],
                              momentum = form.cleaned_data['momentum'],
                              nEpoch = form.cleaned_data['nEpoch'],
                              batchSize = form.cleaned_data['batchSize'],
                              seed = form.cleaned_data['seed'],
                              opAlg = form.cleaned_data['opAlg'],
                              hiddenLayerNum = form.cleaned_data['hiddenLayerNum'],
                              h1n1 = form.cleaned_data['h1n1'],
                              h1n2 = form.cleaned_data['h1n2'],
                              h1n1Activation = form.cleaned_data['h1n1Activation'],
                              h1n2Activation = form.cleaned_data['h1n2Activation'],
                              )
                saveModel.save()
                saveModel.refresh_from_db()

                # Why are we doing this here?
                saveModelDirectoryStr = f'{settings.MEDIA_ROOT}/ml_dnnreg/dnn_model/'
                saveModelDirectoryPath = Path(saveModelDirectoryStr)
                for the_file in saveModelDirectoryPath.iterdir():
                    #filePath = saveModelDirectoryPath / the_file
                    try:
                        if the_file.is_file():
                            the_file.unlink()
                    except Exception as e:
                        print(e)

                with open(saveModelDirectoryPath / model_filename, "w") as jsonFile:
                    jsonFile.write(model_json)
            
                mlmodel.save_weights(saveModelDirectoryPath / model_weight_filename)

                with open(saveModelDirectoryPath / th_filename, "w" ) as jsonFile:
                    jsonFile.write(json.dumps(train_history.history['mean_squared_error']))

                with open(saveModelDirectoryPath / pm_filename, "w") as jsonFile:
                    jsonFile.write(json.dumps(predict_actual))

                with open(saveModelDirectoryPath / reg_filename, "w") as jsonFile:
                    jsonFile.write(json.dumps(regresult))

                if KB.backend() == "tensorflow":
                    KB.clear_session()
                
            except Exception as e:
                print(e)
            MeanSquaredError = train_history.history['mean_squared_error']
            return render(request, 'ml_dnnreg/trainmodel.html', {
                    'form': form,
                    'predict_actual': predict_actual, 
                    'MSE': MeanSquaredError,
                    'allObjects': allObjects,
                    'regdata': regresult,
                    'model_summary': model_summary
                })

        else:
            print('A file with that name already exists')
            return render(request, 'ml_dnnreg/trainmodel.html', {
                    'form': form,
                    'predict_actual': predict_actual, 
                    'MSE': MeanSquaredError,
                    'allObjects': allObjects,
                    'regdata': regresult,
                    'model_summary': model_summary
                })

    else:
        form = HyperParamForm()

    return render(request, 'ml_dnnreg/trainmodel.html', {'form': form})

def repositoryReview(request):
    saved_models = SaveModel.objects.all()
    print("Total saved model count: " + str(saved_models.count()))

    if request.method == 'POST':
        saved_model_form = ModelFileNameForm(request.POST, request.FILES)
        if saved_model_form.is_valid():
            print("saved_model_form is valid")
            selected_Model = SaveModel.objects.get(modelFile = saved_model_form.cleaned_data['modelFile'])
            print(selected_Model.model_time)
            savedModelDir = Path(f"{settings.MEDIA_ROOT}/ml_dnnreg/dnn_model/")
            with open(savedModelDir / selected_Model.modelFile) as json_file:
                model_json = json_file.read()
                loaded_model = model_from_json(model_json)

            with open(savedModelDir / selected_Model.train_history) as json_file:
                train_history_json = json_file.read()

            with open(savedModelDir / selected_Model.predict_model) as json_file:
                predict_model_json = json_file.read()

            with open(savedModelDir / selected_Model.regresultFile) as json_file:
                regresult_json = json_file.read()

            MSE = json.loads(train_history_json)
            predict_actual = json.loads(predict_model_json)
            print(predict_actual)
            regresult = json.loads(regresult_json)

            PredictModel.objects.all().delete()
            
            for n in range(0, len(predict_actual)):
                PredictModel.objects.create(number = n+1, prediction = predict_actual[n][0], actual = predict_actual[n][1], delta = (predict_actual[n][0] - predict_actual[n][1]))
            allobjects = PredictModel.objects.all()

            # do the same redirecting of model.summary() to string parameter
            origStdOut = sys.stdout
            outputBuff = io.StringIO()
            sys.stdout = outputBuff
            loaded_model.summary()
            sys.stdout = origStdOut
            model_summary = outputBuff.getvalue().splitlines(True)
            outputBuff.close()

            if KB.backend() == "tensorflow":
                    KB.clear_session()

            return render(request, 'ml_dnnreg/repositoryreview.html', 
                          {
                              'saved_model_form': saved_model_form,
                              'saved_models': saved_models,
                              'MSE': MSE,
                              'predict_actual': predict_actual,
                              'allobjects': allobjects,
                              'regdata': regresult,
                              'model_summary': model_summary
                          })
        else:
            print("saved_model_form is not valid")
            return render(request, 'ml_dnnreg/repositoryreview.html',
                          {
                              'saved_model_form': saved_model_form,
                              'saved_models': saved_models,
                              'MSE': MSE,
                              'predict_actual': predict_actual,
                              'allobjects': allobjects,
                              'regdata': regresult,
                              'model_summary': model_summary
                          })

    else:
         saved_model_form = ModelFileNameForm(request.POST, request.FILES)
         print("request was not POST")
         return render(request, 'ml_dnnreg/repositoryreview.html', 
                       {
                           'saved_model_form': saved_model_form,
                           'saved_models': saved_models
                           })


def prediction(request):
    saved_model = SaveModel.objects.all()
    saved_model_form = ModelPredictForm(data = request.POST, files=request.FILES)
    if request.method == "POST":
        if saved_model_form.is_valid():
            selected_Model = SaveModel.objects.get(modelFile=saved_model_form.cleaned_data["modelFile"])
            fileList = selected_Model.modelFile.split(".")
            model_weight_file = fileList[0] + ".h5"

            savedModelDir = Path(f"{settings.MEDIA_ROOT}/ml_dnnreg/dnn_model/")
            with open(savedModelDir / selected_Model.modelFile) as json_file:
                model_json = json_file.read()
                loaded_model = model_from_json(model_json)

            with open(savedModelDir / selected_Model.train_history) as json_file:
                train_history_json = json_file.read()

            with open(savedModelDir / selected_Model.predict_model) as json_file:
                predict_model_json = json_file.read()

            with open(savedModelDir / selected_Model.regresultFile) as json_file:
                regresult_json = json_file.read()

            loaded_model.load_weights(savedModelDir / model_weight_file)


            dataframe = pandas.read_csv("media/ml_dnnreg/" + str(saved_model_form.cleaned_data['predictCsvFile']), header=None)
            dataset = dataframe.values
            X = dataset[:, 0:dataset.shape[1]]
            # Run the loaded model on test data
            test_predictions = loaded_model.predict(X)

            MSE = json.loads(train_history_json)
            predict_actual = json.loads(predict_model_json)
            regresult = json.loads(regresult_json)

            PredictModel.objects.all().delete()
            for n in range(0, len(predict_actual)):
                PredictModel.objects.create(number=n+1, prediction=predict_actual[n][0], actual=predict_actual[n][1], delta=(predict_actual[n][0] - predict_actual[n][1]))

            allobjects = PredictModel.objects.all()
            predictobjects = []
            for n in range(0, len(test_predictions)):
                predictobjects.append({"number": n+1, "prediction": test_predictions[n]})

            # do the same weird thing with redirecting the model.summary() method output from stdout
            origStdOut = sys.stdout
            outputBuff = io.StringIO()
            sys.stdout = outputBuff
            loaded_model.summary()
            sys.stdout = origStdOut
            model_summary = outputBuff.getvalue().splitlines(True)
            outputBuff.close()

            if KB.backend() == "tensorflow":
                KB.clear_session()
        
            return render(request, 'ml_dnnreg/prediction.html', {
                    'saved_model_form': saved_model_form,
                    'saved_model': saved_model,
                    'MSE': MSE,
                    'predict_actual': predict_actual,
                    'allobjects': allobjects,
                    'predictobjects': predictobjects,
                    'regdata': regresult,
                    'model_summary': model_summary,
                })
        else:
            print("saved model form is not valid")
            return render(request, 'ml_dnnreg/prediction.html', {'saved_model_form': saved_model_form})

    else:
        print("request was not POST")
        return render(request, 'ml_dnnreg/prediction.html', {'saved_model_form': saved_model_form, 'saved_model': saved_model})