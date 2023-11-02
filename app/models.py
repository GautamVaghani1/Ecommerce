from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
# Create your models here.
STATE_CHOICES= (
    ('Andaman & Nicobar Islands' , 'Andaman & Nicobar Islands' ),
    ('Andhra Pradesh' , 'Andhra pradesh'),
    ('Arunachal Pradesh' , 'Arunachal Pradesh'),
    ('Assam' , 'Assam'),
    ('Bihar' , 'Bihar'),
    ('Chandigath','Chandigath'),
    ('Chatishgath' , 'Chatishgath'),
    ('Dadra & Nagar Haveli' , 'Dadra & Nagar Haveli'),
    ('Daman & Diu' , 'Daman & Diu'),
    ('Delhi' , 'Delhi'),
    ('Goa' ,'Goa'),
    ('Gujarat' , 'Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh' ,'Himachal Pradesh'),
    ('Jammu & Kashmir' , 'Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharastra' , 'Maharastra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland' , 'Nagaland'),
    ('Odisha' , 'Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim' , 'Sikkim'),
    ('Tamil Nadu' , 'Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh' , 'Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
class Customer(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES , max_length=50)

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L' , 'Laptop'),
    ('TW' , 'Top Wear'),
    ('BW' , 'Bottom Wear'),
)

class Product(models.Model):
    title =models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES , max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way' , 'On the way'),
    ('Delivered' , 'Delivered'),
    ('Cancel' , 'Cancel')
)


class OrderPLaced(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50 , choices=STATUS_CHOICES , default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price



