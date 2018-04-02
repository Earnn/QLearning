from django.contrib import admin
from .models import *

class StoreAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Store._meta.fields]
admin.site.register(Store, StoreAdmin)

class MenuAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Menu._meta.fields]
admin.site.register(Menu, MenuAdmin)


class ProfileAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Profile._meta.fields]
admin.site.register(Profile, ProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Review._meta.fields]
admin.site.register(Review, ReviewAdmin)

class User_sessionAdmin(admin.ModelAdmin):
	list_display=[f.name for f in User_session._meta.fields]
admin.site.register(User_session, User_sessionAdmin)

class Anonymous_sessionAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Anonymous_session._meta.fields]
admin.site.register(Anonymous_session, Anonymous_sessionAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Order._meta.fields]
admin.site.register(Order, OrderAdmin)

class StoreByUserAdmin(admin.ModelAdmin):
	list_display=[f.name for f in StoreByUser._meta.fields]
admin.site.register(StoreByUser, StoreByUserAdmin)

class UserValueStoreAdmin(admin.ModelAdmin):
	list_display=[f.name for f in UserValueStore._meta.fields]
admin.site.register(UserValueStore, UserValueStoreAdmin)

class UserValueDeliveryAdmin(admin.ModelAdmin):
	list_display=[f.name for f in UserValueDelivery._meta.fields]
admin.site.register(UserValueDelivery, UserValueDeliveryAdmin)

class UserValueStoreAndDeliveryAdmin(admin.ModelAdmin):
	list_display=[f.name for f in UserValueStoreAndDelivery._meta.fields]
admin.site.register(UserValueStoreAndDelivery, UserValueStoreAndDeliveryAdmin)

class QMatrixAdmin(admin.ModelAdmin):
	list_display=[f.name for f in QMatrix._meta.fields]
admin.site.register(QMatrix, QMatrixAdmin)

class InformationsAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Informations._meta.fields]
admin.site.register(Informations, InformationsAdmin)


class GetCouponAdmin(admin.ModelAdmin):
	list_display=[f.name for f in GetCoupon._meta.fields]
admin.site.register(GetCoupon, GetCouponAdmin)

class CouponAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Coupon._meta.fields]
admin.site.register(Coupon, CouponAdmin)

class CodeTypeAdmin(admin.ModelAdmin):
	list_display=[f.name for f in CodeType._meta.fields]
admin.site.register(CodeType, CodeTypeAdmin)

class PaymentAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Payment._meta.fields]
admin.site.register(Payment, PaymentAdmin)

class StoreContactAdmin(admin.ModelAdmin):
	list_display=[f.name for f in StoreContact._meta.fields]
admin.site.register(StoreContact, StoreContactAdmin)


class DeliveryTimeAdmin(admin.ModelAdmin):
	list_display=[f.name for f in DeliveryTime._meta.fields]
admin.site.register(DeliveryTime, DeliveryTimeAdmin)

class DisplayHomeAdmin(admin.ModelAdmin):
	list_display=[f.name for f in DisplayHome._meta.fields]
admin.site.register(DisplayHome, DisplayHomeAdmin)


class StatisticAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Statistic._meta.fields]
admin.site.register(Statistic, StatisticAdmin)

class Tohrung2Admin(admin.ModelAdmin):
	list_display=[f.name for f in Tohrung2._meta.fields]
admin.site.register(Tohrung2, Tohrung2Admin)


class QTableAdmin(admin.ModelAdmin):
	list_display=[f.name for f in QTable._meta.fields]
admin.site.register(QTable, QTableAdmin)

class QTableLocalAdmin(admin.ModelAdmin):
	list_display=[f.name for f in QTableLocal._meta.fields]
admin.site.register(QTableLocal, QTableLocalAdmin)







