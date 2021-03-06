# Generated by Django 2.2 on 2019-04-17 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HyperParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampleCsvFile', models.FileField(upload_to='')),
                ('validationSplit', models.FloatField(default=0.2)),
                ('learningRate', models.FloatField(default=0.001)),
                ('momentum', models.FloatField(default=0.9)),
                ('nEpoch', models.IntegerField(default=100)),
                ('batchSize', models.IntegerField(default=20)),
                ('seed', models.IntegerField(default=123)),
                ('opAlg', models.CharField(choices=[('SGD', 'SGD'), ('ADAM', 'ADAM'), ('RMSProp', 'RMSProp'), ('Adadelta', 'Adadelta'), ('Adagrad', 'Adagrad')], default=('ADAM', 'ADAM'), max_length=30)),
                ('hiddenLayerNum', models.IntegerField(default=2)),
                ('h1n1', models.IntegerField(default=300)),
                ('h1n1Activation', models.CharField(choices=[('linear', 'linear'), ('relu', 'relu'), ('selu', 'selu'), ('sigmoid', 'sigmoid'), ('softmax', 'softmax'), ('softplus', 'softplus'), ('softsign', 'softsign'), ('tanh', 'tanh')], default=('relu', 'relu'), max_length=30)),
                ('h1n2', models.IntegerField(default=30)),
                ('h1n2Activation', models.CharField(choices=[('linear', 'linear'), ('relu', 'relu'), ('selu', 'selu'), ('sigmoid', 'sigmoid'), ('softmax', 'softmax'), ('softplus', 'softplus'), ('softsign', 'softsign'), ('tanh', 'tanh')], default=('linear', 'linear'), max_length=30)),
                ('normalization', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default=('NO', 'NO'), max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='PredictModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('prediction', models.FloatField(default=0.0)),
                ('actual', models.FloatField(default=0.0)),
                ('delta', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SaveModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelFile', models.CharField(default='Machine Learning Model File', max_length=50)),
                ('model_time', models.DateTimeField(auto_now_add=True)),
                ('train_history', models.CharField(default='Training History File', max_length=50)),
                ('predict_model', models.CharField(default='Prediction Model File', max_length=50)),
                ('regresultFile', models.CharField(default='Regresult File', max_length=50)),
                ('deltaMean', models.FloatField(default=0.0)),
                ('trainMean', models.FloatField(default=0.0)),
                ('validationSplit', models.FloatField(default=0.2)),
                ('learningRate', models.FloatField(default=1e-05)),
                ('momentum', models.FloatField(default=0.9)),
                ('nEpoch', models.IntegerField(default=100)),
                ('batchSize', models.IntegerField(default=20)),
                ('seed', models.IntegerField(default=123)),
                ('opAlg', models.CharField(choices=[('SGD', 'SGD'), ('ADAM', 'ADAM'), ('RMSProp', 'RMSProp'), ('Adadelta', 'Adadelta'), ('Adagrad', 'Adagrad')], default=('ADAM', 'ADAM'), max_length=30)),
                ('hiddenLayerNum', models.IntegerField(default=2)),
                ('h1n1', models.IntegerField(default=65)),
                ('h1n2', models.IntegerField(default=19)),
                ('h1n1Activation', models.CharField(choices=[('linear', 'linear'), ('relu', 'relu'), ('selu', 'selu'), ('sigmoid', 'sigmoid'), ('softmax', 'softmax'), ('softplus', 'softplus'), ('softsign', 'softsign'), ('tanh', 'tanh')], default=('relu', 'relu'), max_length=30)),
                ('h1n2Activation', models.CharField(choices=[('linear', 'linear'), ('relu', 'relu'), ('selu', 'selu'), ('sigmoid', 'sigmoid'), ('softmax', 'softmax'), ('softplus', 'softplus'), ('softsign', 'softsign'), ('tanh', 'tanh')], default=('linear', 'linear'), max_length=30)),
                ('normalization', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default=('NO', 'NO'), max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nepoch', models.IntegerField(default=0)),
                ('vmse', models.FloatField(default=0.0)),
                ('mse', models.FloatField(default=0.0)),
                ('vl', models.FloatField(default=0.0)),
                ('mae', models.FloatField(default=0.0)),
                ('loss', models.FloatField(default=0.0)),
                ('vmae', models.FloatField(default=0.0)),
            ],
        ),
    ]
