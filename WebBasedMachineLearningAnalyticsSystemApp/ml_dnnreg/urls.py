from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trainmodel$', views.trainModel, name='trainModel'),
    url(r'^repositoryreview$', views.repositoryReview),
    url(r'^prediction$', views.prediction)
]