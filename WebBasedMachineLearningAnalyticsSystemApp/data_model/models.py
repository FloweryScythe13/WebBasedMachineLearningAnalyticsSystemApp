from django.db import models

class FileModel(models.Model):
	sampleCsvFile = models.FileField()

	def __str__(self):
		return self.sampleCsvFile