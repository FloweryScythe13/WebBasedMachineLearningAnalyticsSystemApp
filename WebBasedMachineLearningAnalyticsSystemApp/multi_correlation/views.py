from django.shortcuts import render
import os, io, sys, datetime, json
import os.path
import pandas as pd
import numpy as np
import statistics
from django.template.loader import get_template
from django.http import HttpResponse
from multi_correlation.forms import HyperParamForm

# define where to access the template file index.html
def index(request):
    template = get_template('index.html')
    html = template.render()
    return HttpResponse(html)

# define multi_correlation behavior
def multi_correlation(request):
    if request.method == 'POST':
        form = HyperParamForm(request.POST, request.FILES)
        if form.is_valid():
            sampleCsvFile = form.cleaned_data['sampleCsvFile'] # this gets the filename?

            # access the new data file in the media folder
            dataframe = pd.read_csv("media/" + str(form.cleaned_data['sampleCsvFile']))
            dataset = dataframe.values
            labels = dataframe.columns.values.tolist()
            data_json = dataframe.to_json()

            dataList = []
            label_num = []
            for i in range(0, dataset.shape[1]):
                if(not isinstance(dataset[0][i], str)):
                    label_num.append(labels[i])
                    sitenum = 0
                    max, min = 0, 0
                    sum = 0
                    datavec = []
                    sitevec = []
                    for j in range(0, dataset.shape[0]):
                        datavec.append(dataset[j][i])
                        if (sitenum == 0):
                            max, mean, min = dataset[j][i], dataset[j][i], dataset[j][i]
                        else:
                            if (dataset[j][i] > max):
                                max = dataset[j][i]
                            if (dataset[j][i] < min):
                                min = dataset[j][i]
                            sum = sum + dataset[j][i]
                            sitenum += 1

                    dataList.append({"parameter": labels[i],
                                    "datavec": datavec,
                                    "median": statistics.median(datavec),
                                    "mean": statistics.mean(datavec),
                                    "stdev": statistics.stdev(datavec),
                                    "max": max,
                                    "min": min,
                                    "points": len(datavec),
                                    "P99": np.percentile(datavec, 99),
                                    "P95": np.percentile(datavec, 95),
                                    "P75": np.percentile(datavec, 75),
                                    "P25": np.percentile(datavec, 25),
                                    "P05": np.percentile(datavec, 5),
                                    "P01": np.percentile(datavec, 1)
                    })

            return render(request, 'multi_correlation/multi_correlation.html', 
                        {'form': form,
                        'dataList': dataList,
                        'data_json': data_json,
                        'dataset': dataset,
                        'labels': labels,
                        'range': range(dataset.shape[1])})


        else:
            print('form is not valid!')
            return render(request, 'multi_correlation/multi_correlation.html', {'form': form,})

    else:
        form = HyperParamForm()
    return render(request, 'multi_correlation/multi_correlation.html', {'form': form})