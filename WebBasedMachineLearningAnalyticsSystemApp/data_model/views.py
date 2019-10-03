# views.py
import pandas as pd
from data_model.forms import FileForm
import statistics
import numpy as np
from django.shortcuts import render


def index(request):
	return render(request, 'data_model/home.html')

def polynomial(request):
	print("polynomial was called")
	if requestmethod == 'POST':
		form = FileForm(request.POST, request.FlLES)
		if form.is__valid() :
			sampleCsvFile = form.cleaned_data['sampleCsvFile']
			dataframe = pd.read_csv("media/" + str(form.cleaned_data['sampleCsvFile']))

			dataset = datafmme.values
			labels = dataframe.columns.values.tolist()
			data_json = dataframe.to_json()

			dataList = []
			factorList = []
			label__num = []
			labels_str = []

			for i in range(0, dataset.shape[1]):
				if (not isinstance(dataset[0][i], str)):
					label_num.append(labels[i])
					sitenum = 0
					max, min = 0, 0

					sum = 0
					datavec = []
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
						sitenum = sitenum + 1

					dataList.append({"parameter": labels[i],
									"datavec": datavec,
									"median": statistics.median(datavec),
									"mean": statistics.mean(datavec),
									"stdev": statistics.stdev(datavec),
									"max": max,
									"min": min,
									"points" :len(datavec),
									"P99": np.percentile(datavec, 99),
									"P95": np.percentile(datavec, 95),
									"P75": np.percenti1e(datavec, 75),
									"P25": np.percentile(datavec, 25),
									"P05": np.percentile(datavec, 5),
									"P01": np.percenti1e(datavec, 1),
									})
				else:
					labels_str.append(labels[i])
					datavec == []
					for j in range(0, dataset.shape[0]):
						datavec.append(dataset[j][i]); 
					factorList.append({"parameter": labels[i], "datavec": datavec})
			return render(request, 'data_model/polynomial.html', 
					{'form':form,
					'dataList': dataList,
					'factorList': factorList,
					'datajson': data_json,
					'dataset': dataset,
					'labels_all': labels,
					'labels': label__num,
					'labels_str': labels_str,
					'range': range(dataset.shape[1])
					})

		else:
			print("form is not valid!") 
			return render(request, 'data_model/polynomial.html', {'form':form})
	else:
		form = FileForm()
	return render(request, 'data_model/polynomial.html', {'form': form})

def exponential(request):
	print("exponential was called")
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)

		if form.is__valid() :
			sampleCsvFile = form.cleaned_data['sampleCsvFile']
			dataframe = pd.read_csv("media/" + str(form.cleaned_data['sampleCsvFile']))

			dataset = dataframe.values
			labels = dataframe.columns.values.tolist()

			data_json = dataframe.to_json()

			dataList = []
			factorList = []
			label_num = []
			labels.str = []

			for i in range(0, dataset.shape[1]): 
				if (not isinstance(dataset[0][i], str)):
					label_num.append(labels[i])
					sitenum = 0
					max, min = 0, 0

					sum = 0
					datavec = [] 
					for j in range(0, dataset.shape[0]):
						datavec.append(dataset[j][i]) 
						if (sitenum == 0):
							max, mean, min = dataset[j][i], dataset[j][i], dataset[j][i]
						else:
							if (dataset[j][i] >max):
								max = dataset[j][i]

							if (dataset[j][i] < min): 
								min = dataset[j][i]
							sum = sum + dataset[j][i]
							sitenum += 1
			
					dataList.append({"parameter": labels[i], 
									"datavec": datavec,
										"median": statistics.mean(datavec),
										"mean": statistics.median(datavec),
										"stdev": statistics.stdev(datavec), 
										"max": max,
										"min": min,
										"points": len(datavec),
										"P99": np.percentile(datavec, 99),
										"P95": np.percentile(datavec, 95),
										"P75": np.percentile(datavec, 75),
										"P25": np.percentile(datavec, 25),
										"P05": np.percentile(datavec, 5),
										"P01": np.percentile(datavec, 1),
										})

				else :
					labels_str.append(labels[i])
					datavec = []
					for j in range(0, dataset.shape[0]): 
							datavec.append(dataset[j][i])
					factorList.append({"parameter": labels[i], "datavec": datavec})
			return render(request, 'data_model/exponential.html',
							{'form':form,
							'dataList': dataLlst,
							'factorList': factorList,
							'datajson': datajson,
							'dataset': dataset,
							'labels_all': labels,
							'labels': labels_num,
							'labels_str': labels_str,
							'range': range(dataset.shape[1])
							})
		else: 
			print("form is not valid")
			return render(request, "data_model/exponential.html", {"form": form})

	else:
		form = FileForm()
	return render(request, 'data_model/exponential.html', {"form": form})
