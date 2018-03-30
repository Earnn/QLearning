# -*- coding: utf-8 -*- 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Review



class ReviewForm(forms.Form):
    comment =  forms.CharField(max_length=5000, help_text='',widget=forms.Textarea(attrs={'cols': 5,'rows': 5,'class': 'uk-textarea','placeholder':'เขียนรีวิว', }))
 
class StoreForm(forms.Form):
    # DAY_OPEN_CHOICES = (
    # ("Mon.", 'วันจันทร์'),
    # ("Tue.", 'วันอังคาร'),
    # ("Wed.", 'วันพุธ'),
    # ("Thu.", 'วันพฤหัสบดี'),
    # ("Fri.", 'วันศุกร์'),
    # ("Sat.", 'วันเสาร์'),
    # ("Sun.", 'วันอาทิตย์'),
    # ("Mon - Fri.", 'วันจันทร์ - วันศุกร์'),
    # ("Sat. - Sun.", 'วันเสาร์ - วันอาทิตย์'),
    # ("Everyday", 'ทุกวัน')
    # )
    DAY_OPEN_CHOICES = (
    (1, 'วันจันทร์'),
    (2, 'วันอังคาร'),
    (3, 'วันพุธ'),
    (4, 'วันพฤหัสบดี'),
    (5, 'วันศุกร์'),
    (6, 'วันเสาร์'),
    (7, 'วันอาทิตย์'),
    (8, 'วันจันทร์ - วันศุกร์'),
    (9, 'วันเสาร์ - วันอาทิตย์'),
    (0, 'ทุกวัน')
    )
    # DAY_OPEN_CHOICES = (
    # ("วันจันทร์", 'วันจันทร์'),
    # ("วันอังคาร", 'วันอังคาร'),
    # ("วันพุธ", 'วันพุธ'),
    # ("วันพฤหัสบดี", 'วันพฤหัสบดี'),
    # ("วันศุกร์", 'วันศุกร์'),
    # ("วันเสาร์", 'วันเสาร์'),
    # ("วันอาทิตย์", 'วันอาทิตย์'),
    # ("วันจันทร์ - วันศุกร์", 'วันจันทร์ - วันศุกร์'),
    # ("วันเสาร์ - วันอาทิตย์", 'วันเสาร์ - วันอาทิตย์'),
    # ("ทุกวัน", 'ทุกวัน')
    # )
    # DAY_OPEN_CHOICES = (
    # ("mon", 'วันอาทิตย์'),
    # ("tue", 'ทุกวัน')
    # )
    TRUE_FALSE_CHOICES = (
    (False, 'ไม่มีบริการส่ง'),
    (True, 'มีบริการส่ง')
    )
    CATEGORY_CHOICES = (
    ("สเต็ก","สเต็ก"),
    ("ปิ้งย่าง","ปิ้งย่าง"),
    ("ชาบู","ชาบู"),
    ("อาหารไทย","อาหารไทย"),
    ("อาหารญี่ปุ่น","อาหารญี่ปุ่น"),
    ("อาหารเกาหลี","อาหารเกาหลี"),
    ("ของหวาน","ของหวาน"),
    ("เครื่องดื่ม","เครื่องดื่ม"),
    ("อื่นๆ","อื่นๆ"),
    )

    store_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    place =  forms.CharField(max_length=1000, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    store_image = forms.FileField()
    phone =  forms.CharField(max_length=20,required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    tags =  forms.CharField(max_length=50, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    category = forms.ChoiceField(choices = CATEGORY_CHOICES, label="",initial='', widget=forms.Select(), required=False)
    time_open = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required = False)
    time_close = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required = False)
    day_open = forms.ChoiceField(choices = DAY_OPEN_CHOICES, label="",initial='', widget=forms.Select(), required=False)
    delivery = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="",initial='ไม่มีบริการส่ง', widget=forms.Select(), required=False)


class SlipPaymentForm(forms.Form):
    slip_image = forms.FileField() 

class MenuForm(forms.Form):
    menu_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_price =  forms.FloatField( help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_image = forms.FileField()


class SelectMonthForm(forms.Form):
    choices = [(0, 'แสดงทั้งหมด'), (1, 'มกราคม'),(2, 'กุมภาพันธุ์'), (3, 'มีนาคม'), (4, 'เมษายน'), (5, 'พฤษภาคม'), (6, 'มิถุนายน')]
    action = forms.ChoiceField(choices=choices, 
                           widget=forms.Select(attrs={'onchange': 'form.submit();','name':'monthSelect'}))



class AnythingElseForm(forms.Form):
    comment =  forms.CharField(max_length=5500, help_text='',widget=forms.Textarea(attrs={'cols': 5,'rows': 3,'class': 'uk-textarea','placeholder':'เขียนรีวิว', }))


        
class InformationsForm(forms.Form):
    # age = forms.IntegerField(required=True)
    # gender = (('Male','male'),('Female','female'))
    birthdate = forms.DateField(widget=forms.widgets.SelectDateWidget)
    sex = forms.ChoiceField(choices=(('Male','male'),('Female','female')),required=True, 
        widget=forms.RadioSelect(attrs={'class' : '',}))
    size = forms.ChoiceField(choices = (('thin','ผอม'),('fit','หุ่นดี/ทั่วไป'),('chubby','อวบ'),('fat','อ้วน')), 
        required=True, help_text='',widget=forms.CheckboxSelectMultiple)
    salary = forms.ChoiceField(choices=(('น้อยกว่า 10,000','น้อยกว่า 10,000' ),('10,000-19,000','10,000-19,000')
        ,('20,000-29,999','20,000-29,999'),('30,000-39,000','30,000-39,000'),('40,000-49,000','40,000-49,000')
        ,('50,000 ขึ้นไป','50,000 ขึ้นไป')), required=True)
    meal = forms.ChoiceField(choices=(('มื้อเช้า','มื้อเช้า'),('มื้อเที่ยง','มื้อเที่ยง'),('มื้อเย็น','มื้อเย็น'),('มื้อดึก','มื้อดึก')), required=True)
    reason = forms.ChoiceField(choices=(('รสชาติ','รสชาติ'), ('ราคา','ราคา'),('บริการ','บริการ') ,('ความสะอาด','ความสะอาด'), ('บรรยากาศ','บรรยากาศ'), ('สถานที่ตั้ง','สถานที่ตั้ง')), required=True)
    # favorites = models.CharField(max_length=200,blank=False,null=False)
    social_media = forms.ChoiceField(choices=(('Facebook','facebook'), ('Twitter','twitter'),('Line','line') ,('Instagram','instagram')), required=True)