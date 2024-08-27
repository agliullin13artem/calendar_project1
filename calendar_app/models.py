from django.db import models



class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название события')
    start_at = models.DateTimeField(verbose_name='Начало события')
    period = models.IntegerField(null=True, blank=True, verbose_name='Период')


    def __str__(self) -> str:
        return f'Собитие: {self.name}'