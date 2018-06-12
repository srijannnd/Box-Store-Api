from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Box(models.Model):
    length = models.DecimalField(blank=False, decimal_places=2, max_digits=12)
    width = models.DecimalField(blank=False, decimal_places=2, max_digits=12)
    height = models.DecimalField(blank=False, decimal_places=2, max_digits=12)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    area = models.DecimalField(blank=False, decimal_places=2, max_digits=12)
    volume = models.DecimalField(blank=False, decimal_places=2, max_digits=12)

    def save(self, *args, **kwargs):
        l = self.length
        w = self.width
        h = self.height
        self.area = 2*sum(
            [l*w, w*h, l*h])
        self.volume = l*h*w
        return super(Box, self).save(*args, **kwargs)

    class Meta:
        db_table = 'box'
