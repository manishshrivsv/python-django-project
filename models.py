from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    starting_price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='cars/')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def highest_bid(self):
        highest=self.bids.order_by('-amount').first()
        return highest.amount if highest else self.starting_price
        

class Bid(models.Model):
    car=models.ForeignKey(Car,related_name="bids",on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
