from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
import os

OPALG_CHOICES = (('SGD', 'SGD'), ('ADAM', 'ADAM'), ('RMSProp', 'RMSProp'), ('Adadelta', 'Adadelta'), ('Adagrad', 'Adagrad'))
HLACTIVATION_CHOICES = (('linear', 'linear'), ('relu', 'relu'), ('selu', 'selu'), ('sigmoid', 'sigmoid'), ('softmax', 'softmax'), ('softplus', 'softplus'), ('softsign', 'softsign'), ('tanh', 'tanh'))
Normalize_Choices = (('YES', 'YES'), ('NO', 'NO'))


class HyperParam(models.Model):
    basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # what is this for?
    datapath = os.path.join(basepath, 'media')
    sampleCsvFile = models.FileField()
    validationSplit = models.FloatField(default=0.2)
    learningRate = models.FloatField(default=0.001)
    momentum = models.FloatField(default=0.9)
    nEpoch = models.IntegerField(default=100)
    batchSize = models.IntegerField(default=20)
    seed = models.IntegerField(default=123)
    opAlg = models.CharField(max_length=30, choices = OPALG_CHOICES, default = OPALG_CHOICES[1])
    hiddenLayerNum = models.IntegerField(default=2)
    h1n1 = models.IntegerField(default=300)
    h1n1Activation = models.CharField(max_length=30, choices = HLACTIVATION_CHOICES, default = HLACTIVATION_CHOICES[1])
    h1n2 = models.IntegerField(default = 30)
    h1n2Activation = models.CharField(max_length=30, choices = HLACTIVATION_CHOICES, default = HLACTIVATION_CHOICES[0])
    normalization = models.CharField(max_length = 3, choices = Normalize_Choices, default = Normalize_Choices[1])

    def __str__(self):
        return self.sampleCsvFile

# Prediction Table Model
class PredictModel(models.Model):
    number = models.IntegerField(default=0)
    prediction = models.FloatField(default=0.0)
    actual = models.FloatField(default = 0.0)
    delta = models.FloatField(default = 0.0)

    def __str__(self):
        return self.number

# Training History Model
class TrainingHistory(models.Model):
    # Number of Epochs
    nepoch = models.IntegerField(default = 0)
    vmse = models.FloatField(default = 0.0)
    # Mean Squared Error
    mse = models.FloatField(default = 0.0)
    vl = models.FloatField(default = 0.0)
    mae = models.FloatField(default = 0.0)
    loss = models.FloatField(default = 0.0)
    vmae = models.FloatField(default = 0.0)

    def __str__(self):
        return self.mse


# SaveModel will store the trained machine learning model
class SaveModel(models.Model):
    modelFile = models.CharField(max_length = 50, default = "Machine Learning Model File")
    model_time = models.DateTimeField(auto_now_add=True)
    train_history = models.CharField(max_length = 50, default = "Training History File")
    predict_model = models.CharField(max_length = 50, default = "Prediction Model File")
    regresultFile = models.CharField(max_length = 50, default = "Regresult File")
    deltaMean = models.FloatField(default = 0.0)
    trainMean = models.FloatField(default = 0.0)
    validationSplit = models.FloatField(default = 0.2)
    learningRate = models.FloatField(default = 0.00001)
    momentum = models.FloatField(default = 0.9)
    nEpoch = models.IntegerField(default = 100)
    batchSize = models.IntegerField(default = 20)
    seed = models.IntegerField(default = 123)
    opAlg = models.CharField(max_length=30, choices = OPALG_CHOICES, default = OPALG_CHOICES[1])
    hiddenLayerNum = models.IntegerField(default = 2)
    h1n1 = models.IntegerField(default = 65)
    h1n2 = models.IntegerField(default = 19)
    h1n1Activation = models.CharField(max_length=30, choices = HLACTIVATION_CHOICES, default = HLACTIVATION_CHOICES[1])
    h1n2Activation = models.CharField(max_length=30, choices = HLACTIVATION_CHOICES, default = HLACTIVATION_CHOICES[0])
    normalization = models.CharField(max_length = 3, choices = Normalize_Choices, default = Normalize_Choices[1])

    def __str__(self):
        return self.modelFile

# ModelFileName stores the names of existing trained models
class ModelFileName(models.Model):
    savedModel = SaveModel.objects.all()
    choiceFile = []
    for obj in savedModel:
        choiceFile.append([obj.modelFile, obj.modelFile])

    basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datapath = os.path.join(basePath, 'media')
    predictCsvFile = models.FileField()
    modelFile = models.CharField(max_length = 50, choices = choiceFile, default = "Machine Learning Model File")

    def __str__(self):
        return self.modelFile