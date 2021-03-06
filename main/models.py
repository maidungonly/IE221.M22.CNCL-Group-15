from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class KcookPost(models.Model):
    """thiết lập model KcookPost gồm các thuộc tính như bên dưới"""
    title_post = models.TextField()
    image = models.ImageField(upload_to="kcookpost_imgs/")
    nguyenlieu = models.TextField()
    introduction = models.CharField(max_length=350, null=True)
    cachlam = models.TextField()
    # slug =models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.title_post


class Categrory(models.Model):
    """thiết lập model Category loại sản phẩm"""
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    """thiết lập model Product (các sản phẩm)"""
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product_imgs/")
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, blank=True)
    product_des = models.TextField()
    cat_name = models.ForeignKey(Categrory, on_delete=models.CASCADE)


class Customer(models.Model):
    """thiết lập model Customer (khách hàng)"""	
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):

	"""Thiết lập thông tin order"""
	customer = models.ForeignKey(
    Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

    # @property
    # def shipping(self):
    # 	shipping = False
    # 	orderitems = self.orderitem_set.all()
    # 	for i in orderitems:
    # 		if i.product.digital == False:
    # 			shipping = True
    # 	return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):

    """thiết lập model những sản phẩm được order"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    """thiết lập model địa chỉ giao hàng"""
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
