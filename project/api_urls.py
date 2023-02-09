from django.urls import path
from . import api
urlpatterns = [
        path('data', api.index, name="data"),
        path('getImage', api.getImage, name="getImage"),
        path('getNumberOfArticles', api.getNumberOfArticles, name="getNumberOfArticles"),
        path('showPopularity', api.showPopularity, name='showPopularity'),
        path('makePredictions', api.makePredictions, name='makePredictions'),
]