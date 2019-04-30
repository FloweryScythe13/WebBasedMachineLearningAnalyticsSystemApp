from django import forms
from django.forms import ModelForm
from ml_dnnreg.models import HyperParam, SaveModel, ModelFileName

class HyperParamForm(ModelForm):
    class Meta:
        model = HyperParam
        fields = '__all__'

class SaveModelForm(ModelForm):
    class Meta:
        model = SaveModel
        fields = ['modelFile']

class ModelFileNameForm(ModelForm):
    class Meta:
        model = ModelFileName
        fields = ['modelFile']

class ModelPredictForm(ModelForm):
    class Meta:
        model = ModelFileName
        fields = '__all__'
