from django.db import models
from django.utils.text import slugify

def get_directory_path(instance, filename):
    return f'phones/{instance.pk}_{filename}'

class Phone(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=get_directory_path)
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)
