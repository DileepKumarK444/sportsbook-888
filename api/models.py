from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sport'
    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Started', 'Started'),
        ('Ended', 'Ended'),
        ('Cancelled', 'Cancelled')
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    scheduled_start = models.DateTimeField(blank=True,null=True)
    actual_start = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'event'
    def __str__(self):
        return self.name

class Selection(models.Model):
    OUTCOME_CHOICES = (
        ('Unsettled', 'Unsettled'),
        ('Void', 'Void'),
        ('Lose', 'Lose'),
        ('Win', 'Win'),
    )

    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    outcome = models.CharField(max_length=255, choices=OUTCOME_CHOICES)

    class Meta:
        db_table = 'selection'
    def __str__(self):
        return self.name
