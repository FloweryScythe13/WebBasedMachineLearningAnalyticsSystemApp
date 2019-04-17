from django.forms import ModelForm
from multi_correlation.models import HyperParam

class HyperParamForm(ModelForm):
    """The HTML form for users to load the data file."""
    class Meta:
        model = HyperParam
        fields = '__all__'


