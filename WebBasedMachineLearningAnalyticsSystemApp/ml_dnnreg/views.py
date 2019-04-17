from django.shortcuts import render
import os, io, sys, datetime, json
import os.path
from django.conf import settings
from django.db import models
import pandas
import keras
from keras import backend as KB
from keras.models import model_from_json
from ml_dnnreg.forms import HyperParamForm, SaveModelForm
from ml_dnnreg.mlalg import dnn_reg

# Create your views here.
