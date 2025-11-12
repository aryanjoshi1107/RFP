from django.db import models
from users.models import Users,Category

# # Create your models here.
# class RFP(models.Model):
#     item_name=models.CharField()
#     description = models.CharField()
#     quantity = models.CharField()
#     minimumPrice = models.IntegerField()
#     maximumPrice = models.IntegerField()
#     lastDate = models.DateField()
#     Vendors = models.ManyToManyField(Vendors)


class RfpList(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    last_date = models.DateField()
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_list = models.ManyToManyField(Users, related_name='rfps_visible')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.item_name} (Qty: {self.quantity})"



class RfpQuote(models.Model):
    rfp = models.ForeignKey(RfpList,on_delete=models.CASCADE, related_name='quotes')
    vendor = models.ForeignKey(Users,on_delete=models.CASCADE, related_name='quotes')
    is_accepted = models.BooleanField(default= False)
    item_description = models.TextField()
    quantity = models.PositiveIntegerField()
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.vendor_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Quote by {self.vendor.company_name} for {self.rfp.item_name}"
