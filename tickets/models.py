from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=100)


class Enterprise(models.Model):
    name = models.CharField(max_length=100)


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100, blank=True, null=True)
    destination = models.ForeignKey(Place, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    observations = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='tickets/images', blank=True, null=True)


class In_Place(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    out_at = models.DateTimeField(null=True, blank=True)


class Logs(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
