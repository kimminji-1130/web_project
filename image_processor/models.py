from django.db import models

class Detection(models.Model):
    timestamp = models.DateTimeField()  # 탐지된 시간
    object_name = models.CharField(max_length=100)  # 탐지된 객체 이름
    object_count = models.IntegerField()  # 객체 수

    def __str__(self):
        return f"{self.timestamp} - {self.object_name}: {self.object_count}"
