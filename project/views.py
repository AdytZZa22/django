from django.shortcuts import render
import os
import pandas as pd


# Create your views here.
def home(request):
    # dfSR = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), delimiter=';')
    # mydict = {
    #     "df": dfSR.to_html()
    # }
    return render(request, 'index.html')
