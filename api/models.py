from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=80)
    
    def __str__(self):
        return '%s' % (self.name)

class Location(models.Model):
    project = models.ForeignKey(Project,blank=True,null=True)
    name = models.CharField(max_length=80)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        if self.project is None:
            proj = '-'
        else:
            proj = self.project__name 
        return '%s (%s)' % (self.name,proj)


class Delivery(models.Model):
    filename = models.CharField(max_length=100)
    filename_stored = models.CharField(max_length=200,blank=True,null=True)
    contributor = models.CharField(max_length=100,blank=True,null=True)
    delivered = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return '{} ({})'.format(self.filename,self.delivered)

class Series(models.Model):
    location = models.ForeignKey(Location)
    delivery = models.ForeignKey(Delivery)
    
    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return '{}: {}'.format(self.filename,self.location.name)

class History(models.Model):
    """ A realisation of the time series for a location
    (it can be updated with newer insights)
    """
    location = models.ForeignKey(Location)
    version = models.IntegerField(default=1)
    tolerance = models.FloatField(default=0.0001)
    stdv = models.FloatField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Histories"

    def __str__(self):
        return 'History {} v{}'.format(self.location.name,self.version)

class Measurement(models.Model):
    partof = models.ForeignKey(History)
    timestamp = models.DateField()
    value = models.FloatField()
    val_min = models.FloatField()
    val_max = models.FloatField()

    def __str__(self):
        return '{} : {} - {}'.format(self.partof.location.name,self.timestamp,self.value)

    