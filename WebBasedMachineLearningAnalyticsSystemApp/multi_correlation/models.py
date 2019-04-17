from django.db import models
import os

class HyperParam(models.Model):
    basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datapath = os.path.join(basepath, 'media')
    sampleCsvFile = models.FileField()

    def __str__(self):
        return self.sampleCsvFile
