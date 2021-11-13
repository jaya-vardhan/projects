from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
STATE_CHOICES={
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Telangana','Telanagana'),
    ('Karnataka','Karnataka'),
    ('Tamilnadu','Tamilnadu')
}

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.user)

CATEGORY_CHOICES={
    ('M','Mobiles'),
    ('L','laptops'),
    ('TW','TopWear'),
    ('BW','BottomWear')
}

BRAND_CHOICES={
    ('Xiaomi','Xiaomi'),
    ('Samsung','Samsung'),
    ('Realme','Realme'),
    ('Apple','Apple'),
    ('Hp','Hp'),
    ('OnePlus','OnePlus'),
    ('AllenSolly','AllenSolly'),
    ('IndigoNation','IndigoNation'),
    ('DressBerry','DressBerry'),
    ('AmericanTourister','AmericanTourister'),
    ('Zara','Zara'),
    ('Puma','Puma'),
}

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    brand=models.CharField(max_length=50,choices=BRAND_CHOICES)  
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product.id)

    @property
    def cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES={
    ('Accepted','Accepted'),
    ('Shipped','Shipped'),
    ('On The Way','On The way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
}

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=STATUS_CHOICES,max_length=50,default='Pending')

    def __str__(self):
        return str(self.user)

    @property
    def cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)





