# Generated by Django 5.1.4 on 2025-02-14 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDatas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('productDescription', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'product_data',
                'managed': True,
            },
        ),
    ]
