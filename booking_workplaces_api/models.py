from django.db import models


class Workplace(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class BookingWorkplace(models.Model):
    description = models.CharField(max_length=200)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    datetime_from = models.DateField()
    datetime_to = models.DateField()

    def __str__(self):
        return self.description
