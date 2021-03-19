# Generated by Django 2.2.7 on 2020-02-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station_MODEL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataid', models.IntegerField(verbose_name='id')),
                ('name', models.CharField(max_length=1024, verbose_name='name')),
                ('latitude', models.FloatField(verbose_name='latitude')),
                ('longitude', models.FloatField(verbose_name='longitude')),
            ],
        ),
    ]