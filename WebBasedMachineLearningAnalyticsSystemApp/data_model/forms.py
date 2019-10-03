from django.forms import ModelForm
from data_model.models import FileModel

class FileForm(ModelForm):
    """The form that will be sent by users with an attached data file for imports"""
    class Meta:
        model = FileModel
        fields = '__all__'


