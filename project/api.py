import json

from django.http import HttpResponse, JsonResponse
import pandas as pd
import seaborn as sb
import numpy as np
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64


def index(request):
    if request.method == "GET":
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), skipinitialspace=True)
        rows = records(df);
        null_rows = null_records(df)

        # Variabile numerice
        numCols = df.select_dtypes("number").columns

        # Variabile categoriale - daca exista si care sunt acestea
        catCols = df.select_dtypes("object").columns
        numCols = list(set(numCols))
        catCols = list(set(catCols))

        return JsonResponse({
            "records": rows,
            "null_records": int(null_rows),
            "media": df.mean().to_json(),
            "cvartile": df.quantile(np.arange(0.25, 1, 0.25)).to_json(),
            "deviatia": df.std().to_json(),
            "median": df.median().to_json(),
            "number_cols": json.dumps(numCols),
            "categorials_cols": json.dumps(catCols),
        }, safe=False)
    # endif


def makePredictions(request):
    if request.method == "GET":
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), skipinitialspace=True)
        image = generateCountPlotImage(df, 'n_tokens_title')

        return JsonResponse({
            "image": image
        })


def showPopularity(request):
    if request.method == "GET":
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), skipinitialspace=True)
        share_label = list()
        share_data = df['shares']
        df['shares'].describe()
        for share in share_data:
            if share <= 645:
                share_label.append('Foarte slabe')
            elif 645 < share <= 861:
                share_label.append('Slabe')
            elif 861 < share <= 1400:
                share_label.append('Simplu')
            elif 1400 < share <= 31300:
                share_label.append('Bun')
            elif 31300 < share <= 53700:
                share_label.append('Foarte bun')
            elif 53700 < share <= 77200:
                share_label.append('Excelent')
            else:
                share_label.append('Exceptional')

        # Update this class label into the dataframe
        df = pd.concat([df, pd.DataFrame(share_label, columns=['popularity'])], axis=1)
        image = generateCountPlotImage(df, 'popularity')
        return JsonResponse({
            "image": image
        })


def getNumberOfArticles(request):
    if request.method == "GET":
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), skipinitialspace=True)

        weekday_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0,
                          'Sunday': 0}

        # Parcurgeți fiecare rând din setul de date
        for index, row in df.iterrows():
            if row['weekday_is_monday'] == 1:
                weekday_counts['Monday'] += 1
            if row['weekday_is_tuesday'] == 1:
                weekday_counts['Tuesday'] += 1
            if row['weekday_is_wednesday'] == 1:
                weekday_counts['Wednesday'] += 1
            if row['weekday_is_thursday'] == 1:
                weekday_counts['Thursday'] += 1
            if row['weekday_is_friday'] == 1:
                weekday_counts['Friday'] += 1
            if row['weekday_is_saturday'] == 1:
                weekday_counts['Saturday'] += 1
            if row['weekday_is_sunday'] == 1:
                weekday_counts['Sunday'] += 1

        return JsonResponse(weekday_counts, safe=False)


def getImage(request):
    if request.method == "GET":
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "OnlineNewsPopularity.csv"), skipinitialspace=True)
        param = request.GET.get('corr')

        if param == '1':
            corr = df.corr()
        else:
            df_fara_dependenta = df.drop(['shares'], axis=1)
            corr = df_fara_dependenta.corr()

        image = generateImage(corr)

        return JsonResponse({
            "image": image
        }, safe=False)


def generateScatterPlotImage(df, x):
    temp_data = df[df['shares'] <= 200000]

    sns.set()
    plt.figure(figsize=(15, 5))
    sns.scatterplot(x=x, y='shares', hue='popularity', data=temp_data)

    # Save the plot to a BytesIO object
    with io.BytesIO() as buf:
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Read the file into memory
        image_data = buf.read()

    # Encode the image as a PNG
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    return image_base64


def generateCountPlotImage(df, x):
    # Generate a Seaborn heatmap

    sns.set()

    plt.figure(figsize=(15, 5))
    sns.countplot(x=x, data=df, alpha=0.5)

    # Save the plot to a BytesIO object
    with io.BytesIO() as buf:
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Read the file into memory
        image_data = buf.read()

    # Encode the image as a PNG
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    return image_base64


def generateImage(corr):
    # Generate a Seaborn heatmap
    sns.set()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True)

    # Save the plot to a BytesIO object
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Encode the image as a PNG
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_base64


def records(df):
    return len(df)


# end


def null_records(df):
    return df.isnull().values.sum()
# end
