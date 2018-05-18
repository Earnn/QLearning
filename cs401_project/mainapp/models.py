 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea,TextInput,FileInput,ChoiceField,Select
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

# Create your models here.
	
class WebsiteVote(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	
	complacence = models.EmailField(max_length=10,blank=True,null=True,default="None")
	comment = models.CharField(max_length=5000,blank=True,null=True,default="None")

	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	


class QTableGlobal(models.Model):


	name = models.CharField(max_length=10,null=True, blank=True)
	# user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	Q_array = ArrayField(ArrayField(models.FloatField()
		),default=[
		[0., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.],
        
        [0., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.],

        [0., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.],
	],blank=True,null=True)
	R_array = ArrayField(ArrayField(models.FloatField()
		),default=
	[
		[0., 0, 100.],
        [100., 0., 0.],
        [0.,100., 0.],
        
        [0., 0, 100.],
        [100., 0., 0.],
        [0.,100., 0.],

        [0., 0, 100.],
        [100., 0., 0.],
        [0.,100., 0.],
	]
	,blank=True,null=True)

class QTableLocal(models.Model):


	name = models.CharField(max_length=10,null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	Q_array = ArrayField(ArrayField(models.FloatField()),blank=True,null=True)
	R_array = ArrayField(ArrayField(models.FloatField()),blank=True,null=True)


class Store(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	price = models.CharField(max_length=50,blank=True,null=True)
	name = models.CharField(max_length=300)
	place = models.CharField(max_length=200)
	image=models.ImageField(upload_to='stores/')
	day_open = models.CharField(max_length=200,null=True, blank=True)
	time_open = models.TimeField(null=True, blank=True)
	time_close = models.TimeField(null=True, blank=True)
	phone = models.CharField(max_length=500,blank=True,null=True)
	tags = models.CharField(max_length=500,blank=True,null=True)
	qrcode = models.ImageField(upload_to='qrcodes/',blank=True,null=True)
	category = models.CharField(max_length=100,blank=True,null=True)
	quote = models.CharField(max_length=1000,blank=True,null=True)
	latitude=models.FloatField(default=14.073565,null=True, blank=True)
	longtitude=models.FloatField(default=100.607963,null=True, blank=True)
	social = models.CharField(max_length=100,blank=True,null=True)
	likes = models.ManyToManyField(User, related_name="likes",blank=True,null=True)
	delivery_boundary = models.CharField(max_length=1000,blank=True,null=True)
	delivery_payment = models.FloatField(null=True, blank=True, default=None)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

	# created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)


	def __str__(self):
		return "%s"%(self.name)

	@property
	def total_likes(self):
		return self.likes.count()

class Populations(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	store1_obj = models.ForeignKey(Store,related_name='store1_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store2_obj = models.ForeignKey(Store,related_name='store2_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store3_obj = models.ForeignKey(Store,related_name='store3_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store4_obj = models.ForeignKey(Store,related_name='store4_obj',on_delete=models.SET_NULL,blank=True,null=True)
	chromosome1 = models.CharField(max_length=10,null=True, blank=True )
	chromosome2 = models.CharField(max_length=10,null=True, blank=True )
	chromosome3 = models.CharField(max_length=10,null=True, blank=True )
	chromosome4 = models.CharField(max_length=10,null=True, blank=True )

class Anonymous_Populations(models.Model):
	name = models.CharField(max_length=100,blank=True,null=True)
	store1_obj = models.ForeignKey(Store,related_name='Astore1_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store2_obj = models.ForeignKey(Store,related_name='Astore2_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store3_obj = models.ForeignKey(Store,related_name='Astore3_obj',on_delete=models.SET_NULL,blank=True,null=True)
	store4_obj = models.ForeignKey(Store,related_name='Astore4_obj',on_delete=models.SET_NULL,blank=True,null=True)
	chromosome1 = models.CharField(max_length=10,null=True, blank=True )
	chromosome2 = models.CharField(max_length=10,null=True, blank=True )
	chromosome3 = models.CharField(max_length=10,null=True, blank=True )
	chromosome4 = models.CharField(max_length=10,null=True, blank=True )

class Menu(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	name = models.CharField(max_length=100)
	price = models.FloatField(null=True, blank=True, default=None)
	image=models.ImageField(upload_to='menu/',blank=True,null=True)
	isSell = models.BooleanField(default=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	def __str__(self):
		return "%s"%(self.name)

# class Tohrung(models.Model):
# 	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)

class Tohrung2(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)

class Order(models.Model):
	store = models.ForeignKey(Store,on_delete=models.SET_NULL,blank=True,null=True)
	menu = ArrayField(models.CharField(max_length=500), blank=True,null=True)
	amount = ArrayField(models.CharField(max_length=500), blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	date = models.DateTimeField(default=datetime.now, blank=True)
	address = models.CharField(max_length=500,blank=True,null=True)
	total = models.FloatField(null=True, blank=True)
	phone_number = models.CharField(max_length=20,null=True, blank=True)
	slip_payment =models.ImageField(upload_to='slip_payment/%Y/%m/%d',blank=True,null=True)
	delivery_charge = models.CharField(max_length=20,blank=True,null=True)
	payment_method = models.CharField(max_length=200,blank=True,null=True)
	coupon= models.CharField(max_length=200,blank=True,null=True)
	morethings = models.CharField(max_length=500,blank=True,null=True)
	status = models.CharField(max_length=20,null=True, blank=True)
	isSuccess = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


	
class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	name = models.CharField(max_length=100,editable=True )
	age = models.CharField(max_length=10,blank=True,null=True,default="None")
	sex = models.CharField(max_length=10,blank=True,null=True,default="None")
	birthdate = models.DateField(blank=True,null=True)
	email = models.EmailField(max_length=100,blank=True,null=True,default="None")
	phone_number = models.CharField(max_length=20,default="None")
	address = models.CharField(max_length=3000,blank=True,null=True,default="None")
	picture=models.ImageField(upload_to="profilePicture/",default="/default.jpg")
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	# status = models.CharField(max_length=10,blank=True,null=True,default="user")

class StoreByUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	store = models.ForeignKey(Store,on_delete=models.SET_NULL,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	comment = models.CharField(max_length=5000)
	rating = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class User_session(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	action = models.CharField(max_length=50,blank=True,null=True)
	value = models.CharField(max_length=100,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class Anonymous_session(models.Model):
	name = models.CharField(max_length=100,blank=True,null=True)
	action = models.CharField(max_length=50,blank=True,null=True)
	value = models.CharField(max_length=100,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class UserValueStore(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class UserValueDelivery(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	cumulative_purchase = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class UserValueStoreAndDelivery(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)
	cumulative_purchase = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


class QMatrix(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)
	amount = ArrayField(models.IntegerField(default=0), blank=True,null=True)
	reward = ArrayField(models.IntegerField(default=0), blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	
class Informations(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	age = models.IntegerField(default=0,blank=True,null=True)
	birthdate = models.DateField(blank=True,null=True)
	sex = models.CharField(max_length=10,blank=True,null=True)
	salary = models.CharField(max_length=50,blank=True,null=True)
	size = models.CharField(max_length=10,blank=True,null=True)
	breakfast = models.BooleanField(default=False)
	lunch = models.BooleanField(default=False)
	dinner = models.BooleanField(default=False)
	late = models.BooleanField(default=False)
	taste = models.BooleanField(default=False)
	price = models.BooleanField(default=False)
	service = models.BooleanField(default=False)
	clean = models.BooleanField(default=False)
	at = models.BooleanField(default=False)
	location = models.BooleanField(default=False)
	facebook = models.BooleanField(default=False)
	twitter = models.BooleanField(default=False)
	instagram = models.BooleanField(default=False)
	line = models.BooleanField(default=False)
	japanese = models.BooleanField(default=False)
	thai = models.BooleanField(default=False)
	diet = models.BooleanField(default=False)
	shabu = models.BooleanField(default=False)
	grill = models.BooleanField(default=False)
	steak = models.BooleanField(default=False)
	fastfood = models.BooleanField(default=False)
	cake = models.BooleanField(default=False)
	dessert = models.BooleanField(default=False)
	coffee = models.BooleanField(default=False)
	juice = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


class Payment(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	pay = models.CharField(max_length=200,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class Coupon(models.Model):
	store = models.ForeignKey(Store, on_delete=models.CASCADE,blank=True,null=True)
	msg = models.CharField(max_length=100,blank=True,null=True)
	amount = models.IntegerField(default=1, blank=True,null=True)
	date_expire = models.DateField(blank=True,null=True)
	code = models.CharField(max_length=10,blank=True,null=True)
	image=models.ImageField(upload_to='images',blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	def __str__(self):
		return "%s"%(self.msg)

class GetCoupon(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
	coupon =  models.ForeignKey(Coupon, on_delete=models.CASCADE,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	amount = models.IntegerField(default=1, blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class CodeType (models.Model):
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE,blank=True,null=True)
	code_type = models.CharField(max_length=10,blank=True,null=True)
	value =  models.CharField(max_length=50,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


class DeliveryTime (models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	monday_open = models.TimeField(null=True, blank=True)
	monday_close = models.TimeField(null=True, blank=True)
	monday = models.BooleanField(default=False)
	tuesday_open = models.TimeField(null=True, blank=True)
	tuesday_close = models.TimeField(null=True, blank=True)
	tuesday = models.BooleanField(default=False)
	wednesday_open = models.TimeField(null=True, blank=True)
	wednesday_close = models.TimeField(null=True, blank=True)
	wednesday = models.BooleanField(default=False)
	thursday_open = models.TimeField(null=True, blank=True)
	thursday_close = models.TimeField(null=True, blank=True)
	thursday = models.BooleanField(default=False)
	friday_open = models.TimeField(null=True, blank=True)
	friday_close = models.TimeField(null=True, blank=True)
	friday = models.BooleanField(default=False)
	saturday_open = models.TimeField(null=True, blank=True)
	saturday_close = models.TimeField(null=True, blank=True)
	saturday = models.BooleanField(default=False)
	sunday_open = models.TimeField(null=True, blank=True)
	sunday_close = models.TimeField(null=True, blank=True)
	sunday = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


class StoreContact(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	contact_type =  models.CharField(max_length=100,blank=True,null=True)
	contact =  models.CharField(max_length=100,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)
	

class DisplayHome(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	coupon =  models.ForeignKey(Coupon, on_delete=models.SET_NULL,blank=True,null=True)
	review = models.ForeignKey(Review, on_delete=models.SET_NULL,blank=True,null=True)
	information = models.ForeignKey(Informations, on_delete=models.SET_NULL,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)


class Statistic(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	month = models.CharField(max_length=20,blank=True,null=True)
	love = models.IntegerField(blank=True,null=True)
	view = models.IntegerField(blank=True,null=True)
	order = models.IntegerField(blank=True,null=True)
	review = models.IntegerField(blank=True,null=True)

	
