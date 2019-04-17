from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.multi_correlation),
    # url('/multi_correlation', views.multi_correlation)
]
