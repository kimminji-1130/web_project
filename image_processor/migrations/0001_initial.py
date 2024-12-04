# Generated by Django 5.1.3 on 2024-12-04 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Detection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("object_name", models.CharField(max_length=100)),
                ("object_count", models.IntegerField()),
            ],
        ),
    ]
