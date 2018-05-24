from django.conf.urls import url,include
from . import views
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # visualization
    url(r'^value_at_risk/?$',views.value_at_risk, name='chart'),
    url(r'^report2/?$',views.report2, name='report2'),  
    url(r'^summarize/?$',views.visual, name='summarize'), 
    url(r'^chart-click/?$',views.chart_click, name='chart_click'),  
 
    
    url(r'^vote/?$',views.vote, name='vote'),   


    # (?# url(r'^/$', views.q_learning, name='q_learning'),)


    url(r'^$', views.home, name='home'),
    # Genetic
    url(r'^click/(?P<name>.*)/(?P<store_id>.*)/(?P<rule>.*)$', views.click, name='click'),
    # Q Learning
    url(r'^ql/$', views.q_learning, name='q_learning'),
    url(r'^get-feedback-from-user/$', views.get_feedback_from_user, name='get_feedback_from_user'),


    
    # tohroong
    url(r'^update-status/$', views.update_status, name='update_status'),
    url(r'^change-status/$', views.change_status, name='change_status'),
    url(r'^โรงอาหารโต้รุ่ง/$', views.home_tohrung, name='tohrung'),
    url(r'^โรงอาหารโต้รุ่ง/(?P<store_name>.*)?$', views.until_dawn_canteen, name='until_dawn_canteen'),
    url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^check-out/$', views.ud_checkout, name='ud_checkout'),
    url(r'^ud-delivery/?$',views.ud_delivery, name='ud_delivery'),
    url(r'^ud-select-payment/(?P<order_id>\d+)/$', views.ud_payment, name='ud-select-payment'),
    
    # steakholder
    url(r'^steak-holder/?$',views.steakholder, name='steakholder'), 
    url(r'^add_steak_to_cart/$', views.add_steak_to_cart, name='add_steak_to_cart'),
    url(r'^st_remove_from_cart/$', views.st_remove_from_cart, name='st_remove_from_cart'),
    url(r'^menues-check-out/$', views.st_checkout, name='st_checkout'),
    url(r'^st-delivery/?$',views.st_delivery, name='st_delivery'),
    url(r'^st-select-payment/(?P<order_id>\d+)/$', views.st_payment, name='st-select-payment'),
    url(r'^order-success/(?P<order_id>\d+)/?$',views.order_success, name='order_success'),
    url(r'^st-code/$', views.st_use_code, name='st_use_code'),

    # ordinary
    url(r'^value_at_risk2/?$',views.value_at_risk2, name='chart2'),   

    url(r'^chart/?$',views.chart, name='chart'),   
    url(r'^report/?$',views.report, name='report'),   
    url(r'^store/(?P<store_name>.*)/(?P<store_id>\d+)$', views.shop_decision, name='shop'),
    url(r'^store/(?P<store_id>\d+)/(?P<store_name>.*)$', views.shop, name='normal_shop'),     
    url(r'^delivery/?$',views.delivery, name='delivery'),
    url(r'^success/(?P<order_id>\d+)/?$',views.success, name='success'),
    url(r'^addStore/?$', views.addStore, name='add_store'),
    url(r'^(?P<pk>\d+)/addMenu/?$', views.addMenu, name='add_menu'),
    
    url(r'^search/(?P<cate>.*)?$',views.searchBycate, name='search_cate'),
    url(r'^search/?$',views.searchAll, name='search_input'),
    url(r'^about-ginim/?$',views.about_us, name='about_us'),
    url(r'^contact/?$',views.contact, name='contact'),
    url(r'^order/?$',views.order, name='order'),
    url(r'^like/$', views.like_button, name='like_button'),
    url(r'^checkIsSell/$', views.checkIsSell, name='checkIsSell'),
    url(r'^edit-store/$', views.outofstock, name='outofstock'),
    url(r'^inf-complete$', views.fill_in_complete, name='inf-complete'),
    url(r'^inf$', views.fill_in, name='inf'),
    url(r'^inf-edit$', views.fill_in_edit, name='is_inf'),
    url(r'^select-payment/(?P<pk>\d+)/$', views.payment, name='select_payment'),
   
    url(r'^usecoupon/(?P<coupon>\d+)?$',views.use_coupon, name='use_coupon'),
    url(r'^code/$', views.use_code, name='code'),
    url(r'^show-slip-(?P<pk>\d+)/$', views.showSlip, name='show-slip'),
    url(r'^changeDelivery-tr/$', views.changeDelivery_tr, name='changeDeliverytr'),
    url(r'^edit-delivery-tr/(?P<id>\d+)?$', views.edit_delivery_tr, name='edit_deliverytr'),
    url(r'^changeDelivery/$', views.changeDelivery, name='changeDelivery'),
    url(r'^edit-delivery/$', views.edit_delivery, name='edit_delivery'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

