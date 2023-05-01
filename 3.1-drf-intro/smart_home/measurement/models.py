from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.pk}'

class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.temperature} ({self.created_at})'
        