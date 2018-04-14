# -*- coding: utf-8 -*- 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
# from echobot.models import *
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.postgres.search import SearchVector,TrigramSimilarity,SearchQuery,SearchRank
from django.db.models import Avg
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
import datetime
from datetime import date,timedelta
from django.core import serializers
import sys
from ast import literal_eval


import base64
import hashlib
import hmac
import json

# Q Learning
from random import choice
import operator
from .models import *
import operator
import random
import operator
import numpy as np
from django.db.models import Q
import functools



# import sys
# import importlib

# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')



# Create your views here.

def available_actions(request,state):
    q_table = QTable.objects.get(user=request.user)
    R = np.array(q_table.R_array)
    current_state_row = R[state,]
    print("R[state,]",R[state,])
    av_act = np.where(current_state_row >= 0)[0]
    

    # print("RR",R)
    # print("state",state)
    # current_state_row = R[state,]
    # print("current_state_row",current_state_row)
    # av_act = np.where(current_state_row >= 0)
    # print("av_act",type(av_act))
    # return np.array(av_act)
    return av_act



def sample_next_action(available_actions_range):
    print("sample_next_action")
    action = int(np.random.choice(available_actions_range,size=1))

    next_state = action
    print("next_state",next_state)
    # Q[state,action] = R[state,action] + gamma * max(Q[next_state,:])

        #comment out the following 4 lines to skip to the result directly
    # print(np.rint(Q))
    # print('current state: ',state)
    # print(available_actions_range)
    # next_action = int(np.random.choice(available_actions_range,size=1))
    # next_action = int(np.random.choice(available_actions_range,1))
    return next_action

# action = sample_next_action(available_act)

def update(current_state, action, gamma):
    
  max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
  
  if max_index.shape[0] > 1:
      max_index = int(np.random.choice(max_index, size = 1))
  else:
      max_index = int(max_index)
  max_value = Q[action, max_index]
  
  Q[current_state, action] = R[current_state, action] + gamma * max_value
  print('max_value', R[current_state, action] + gamma * max_value)
  
  if (np.max(Q) > 0):
    return(np.sum(Q/np.max(Q)*100))
  else:
    return (0)
    
# update(initial_state, action, gamma)

def next_action(request,state,action):
    gamma = 0.8
    print("in action",action)
    action = int(action)
    current_state = int(state)
    # action = 0
    # action = int(np.random.choice(available_actions_range,size=1))
    # c_arr = QTable.objects.create(user=request.user)
    q_table = QTable.objects.get(user=request.user)
    R = np.array(q_table.R_array)
    Q = np.array(q_table.Q_array)
    print("Q",Q)
    max_index = np.where(Q[action,] == np.max(Q[action,]))[0]
    print("max_index.shape[0]",max_index.shape[0])
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    print("max_index",max_index)
    max_value = Q[action, max_index]
    print("max val",max_value)

    Q[current_state, action] = R[current_state, action] + gamma * max_value
    print('max_value', R[current_state, action] + gamma * max_value)

    Q_update = QTable.objects.filter(user=request.user).update(Q_array=Q.tolist())

    return JsonResponse(Q_update,safe=False)
    # Q[state,action] = R[state,action] + gamma * max(Q[next_state,:])

    # print(np.rint(Q))
    # print('current state: ',state)
    



    # print(available_actions_range)
    # next_action = int(np.random.choice(available_actions_range,size=1))
    # next_action = int(np.random.choice(available_actions_range,1))
    # return max_index

def getLocalTable(request):
    q_table = QTableLocal.objects.get(user=request.user)
    R = np.array(q_table.R_array)
    Q = np.array(q_table.Q_array)
    return Q,R

def getGlobalTable(request):
    q_table = QTableGlobal.objects.get(name="global")
    R = np.array(q_table.R_array)
    Q = np.array(q_table.Q_array)
    return Q,R

def get_feedback_from_user(request):
    if request.is_ajax():
        gamma = 0.8
        
        state = request.GET.get('state',False)
        action = request.GET.get('action',False)
        next_state = request.GET.get('next_state',False)

        state = int(state)
        action = int(action)
        print("state",state)
        print("action",action)
        print("next_state",next_state)

        next_state = int(next_state)    
        Q,R = getLcalTable(request)
        R[state,action] +=1
        print(" R[state,action]", R[state,action] )
        # update_rtable = QTableLocal.objects.filte(user=request.user).update(R_array = )

        Q[state,action] = R[state,action] + gamma * max(Q[next_state,:])

        update_qtable = QTableLocal.objects.filter(user=request.user).update(Q_array=Q.tolist(),R_array=R.tolist())
        print("update_qtable",update_qtable)
        return JsonResponse(update_qtable,safe=False)
def check_tag(menu):
    print("menu",menu)
    dic = {'name':'', 'count' : 0}
    count = 0
    store = menu.store
    tag = ""

    if 'อาหารตามสั่ง' in store.tags :
        count += 1
        tag = "อาหารตามสั่ง"
    elif 'ก๋วยเตี๋ยว' in store.tags :
        count += 1
        tag = "ก๋วยเตี๋ยว"
    elif 'ผัดไทย' in store.tags or 'ราดหน้า' in store.tags :
        count += 1
        tag = "ผัดไทย ราดหน้า"
    elif 'โจ๊ก' in store.tags or 'ข้าวต้ม' in store.tags :
        count += 1
        tag = "โจ๊ก ข้าวต้ม"
    elif 'โรตี' in store.tags :
        count += 1
        tag = "โรตี"
    elif 'สเต็ก' in store.tags :
        count += 1
        tag = "สเต็ก"
    elif 'ลูกชิ้น' in store.tags :
        count += 1
        tag = "ลูกชิ้น"
    elif 'ไส้กรอก' in store.tags :
        count += 1
        tag = "ไส้กรอก"
    elif 'หมูปิ้ง' in store.tags or 'ตับปิ้ง' in store.tags or 'ไก่ปิ้ง' in store.tags  :
        count += 1
        tag = "หมูปิ้ง ตับปิ้ง ไก่ปิ้ง"
    elif 'น้ำ' in store.tags or 'นำ้ปั่น' in store.tags:
        count += 1
        tag = "นำ้ปั่น น้ำ"
    elif 'ผลไม้' in store.tags :
        count += 1
        tag = "ผลไม้ "
    elif 'มันบด' in store.tags or 'แฮมเบอร์เกอร์' in store.tags or 'มันอบ' in store.tags  or 'เฟรนช์ฟรายส์' in store.tags :
        count += 1
        tag = "มันบด แฮมเบอร์เกอร์ มันอบ เฟรนช์ฟรายส์"
    elif 'ไก่' in store.tags or 'ข้าวหมูแดง' in store.tags or 'เป็ด' in store.tags :
        count += 1
        tag = "ไก่ ข้าวหมูแดง เป็ด "

    return tag,count         
    # if count > 0 :
    #     dic['name'] = store.name
    #     dic['count'] = count
    #     print("store.name",store.name)
    #     return store.name,count
    # else:
    #     return 

def tohroong(request):
    gamma = 0.8
    state = 1
    print(request.user)
    gender = ""
    
    try:
        info = Informations.objects.get(user=request.user)
        gender = info.sex
    except Exception as e:
        gender="unknown"
    
    if gender == "female":
        # state 0 1 2
        # print("random 6-8",np.random.randint(0,3))
        state = 0
        pass
    elif gender == "male":
        # state 3 4 5
        # print("random 6-8",np.random.randint(3,6))
        state = 3
    elif gender == "unknown":
        state = 6 

   
# state 6 7 8 
    # tohroong 's page is state = 0 
    next_state = 1        
        # num_actions =0
        # actions = 0 
        # valid_moves = R[state] >= 0
    q_table = QTableLocal.objects.get(user=request.user)
    print("q_table",q_table)
    R = np.array(q_table.R_array)
    print("RRRRRRRR",R)
    current_state_row = R[state,]
    print("R[state,]",R[state,])
    Q,R = getLocalTable(request)
    # av_act = np.where(current_state_row >= 0)[0]
    # action = int(np.random.choice(av_act,size=1))

    actions = np.where(Q[state]== np.max(Q[state]))[0]

    if actions.shape[0] >1:
        action = int(np.random.choice(actions,size=1))
    else:
        action = int(actions)

    in_cart_list = check_item_in_cart(request)
    actions=[]
    
    print("Q",Q)
    print("R",R)  
    print("actions",action)          
        # if item_in_cart:
        #     print("item_in_cartitem_in_cartitem_in_cartitem_in_cart")
        # else:
        #     print("item_in_cart",item_in_cart)
    # action = 2
    if action == 0:
        # Top-N
        
        all_ordered = Order.objects.filter(user=request.user)
        logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")
        # print("logs",logs)
        print("len(all_ordered)",len(all_ordered))
        # print("len(logs)",len(logs))
        if len(all_ordered) == 0 and len(logs) == 0:
            pass
        elif len(all_ordered) == 0 and len(logs) >= 1:

            for i in range(4):
                count = len(in_cart_list)
                ran_num = random.randint(0, count-1)
                menu = in_cart_list[ran_num]
                menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                count = len(menu_list)
                ran_in_store = random.randint(0, count-1)
                actions.append(menu_list[ran_in_store])
         

            print("actionsssss",actions)

        elif len(all_ordered) >= 1 and len(logs) >= 1:
            # have ordered and have session
            o_dict = {}
            order_list = []
            if len(all_ordered) >=1 and len(all_ordered) <=5:
                last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
                # print("last_2_ordered",last_2_ordered)
            elif len(all_ordered) >=5:
                last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
                # print("last_3_ordered",last_3_ordered)
            for i in last_ordered:

                for menu_id,amount in zip(i.menu,i.amount):
                 
                    try:
                        int(menu_id)
                        m = Menu.objects.get(id=menu_id)
                    
                    except Exception as e:
                        tuple_menu = literal_eval(m)
                        m = Menu.objects.get(id=tuple_menu[0])
                      
                    if m in o_dict:
                        v = o_dict[m] 
                        new_val = int(v)+1
                        o_dict[m] = new_val
                    else:
                        # first time add 
                        o_dict[m] = int(amount)

            print("o_dict ee",o_dict)      
            most_ordered = max(o_dict.items(), key=operator.itemgetter(1))[0]
            sorted_dict = sorted(o_dict, key=o_dict.get, reverse=True)
            print("most_ordered",most_ordered)
            print("sorted_dict",sorted_dict)
            print("in_cart_list",in_cart_list)
            print("in_cart_list",len(in_cart_list))

            count = 0
            for i in sorted_dict:
                
                # most_add_to_cart = i
                if count == 2:
                    break
                else:
                    print("i",i)
                    if i not in in_cart_list:
                        actions.append(i)
                        count +=1
                    else:
                        print("incart")
            print("actions",actions)
            print("else",count)
            add_list = []
            for i in logs:
                add_list.append(i.value)
                # print("เพิ่มเข้าตะกร้า",i.value)
            my_dict = {i:add_list.count(i) for i in add_list}
            print("my_dict",my_dict)
            most_add_to_cart = max(my_dict.items(), key=operator.itemgetter(1))[0]
            sorted_dict = sorted(my_dict, key=my_dict.get, reverse=True)
            print("most_add_to_cart most_add_to_cart",most_add_to_cart)
            # print("in_cart_list ",in_cart_list)
            count = 0
            more_actions = 4-len(actions)
          
            for i in sorted_dict:
                if count == more_actions:
                    break
                else:
                    sp = i.split(",")
                    # print("sp",sp)
                    # print("en(sp)",len(sp))
                    if len(sp) > 1: # id,บะหมี่
               
                        m = Menu.objects.get(id=sp[0])
                    
                    elif len(sp) == 1: # บะหมี่
                        menu = Menu.objects.filter(name=sp[0])
                        if len(menu) == 1:
                            m = Menu.objects.get(name=i)
            
                    if m not in in_cart_list:
                        if m not in actions:
                            count+=1
                            actions.append(m)
            print("actions a",actions)
            num_loop = 4-len(actions)
            print("xxxx")
            if num_loop >0:
                print("xxxx",num_loop)
                for i in range(num_loop):
                    count = len(in_cart_list)
                    ran_num = random.randint(0, count-1)
                    menu = in_cart_list[ran_num]
                    menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                    count = len(menu_list)
                    ran_in_store = random.randint(0, count-1)
                    actions.append(menu_list[ran_in_store])

            print("actions b",actions)
        
        # return state,action,actions  
    elif action ==1:
        # same things 
        all_ordered = Order.objects.filter(user=request.user)
        logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")


        if len(all_ordered) == 0 and len(logs) == 0:
            pass
        elif len(all_ordered) == 0 and len(logs) >= 1:
            for i in range(4):
                count = len(in_cart_list)
                ran_num = random.randint(0, count-1)
                menu = in_cart_list[ran_num]
                menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                count = len(menu_list)
                ran_in_store = random.randint(0, count-1)
                actions.append(menu_list[ran_in_store])
         

            print("actionsssss",actions)
        elif len(all_ordered) >= 1 :
            if len(all_ordered) >=1 and len(all_ordered) <=2:
                last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
                # print("last_2_ordered",last_2_ordered)
            elif len(all_ordered) >=3:
                last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
            print("last_ordered",last_ordered)
            o_dict = {}
            order_list = []
            for i in last_ordered:

                for menu_id,amount in zip(i.menu,i.amount):
                 
                    try:
                        int(menu_id)
                        m = Menu.objects.get(id=menu_id)
                    
                    except Exception as e:
                        tuple_menu = literal_eval(m)
                        m = Menu.objects.get(id=tuple_menu[0])
                      
                    if m in o_dict:
                        v = o_dict[m] 
                        new_val = int(v)+1
                        o_dict[m] = new_val
                    else:
                        # first time add 
                        o_dict[m] = int(amount)

            print("o_dict o_dict",o_dict)  
            dict_store_tags ={}
            for o in o_dict:
                # dic = {'name':'', 'count' : 0}
                tag, counter = check_tag(o)
                print("store_name",tag)
                print("counter",counter)   

                if counter > 0:
                    if tag in dict_store_tags:
                        v = dict_store_tags[tag] 
                        new_val = int(v)+counter
                        dict_store_tags[tag] = new_val
                    else:
                        dict_store_tags[tag] = counter

            print("dict_store_tags",dict_store_tags)
            # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
            sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
            print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
            # print("most_tags",most_tags)
            if len(sorted_dict_store_tags) >=2:  
                most_tags = sorted_dict_store_tags[:2]
                for m in most_tags:
                    stores = Store.objects.filter(tags__icontains=m)
                    count = len(stores)
                    ran_in_store = random.randint(0, count-1)
                    random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name=in_cart_list)[:2], key=lambda x: random.random())
           
                    for i in random_menues:
                        actions.append(i)
            elif len(sorted_dict_store_tags)==1:
                most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                stores = Store.objects.filter(tags__icontains=m)
                count = len(stores)
                ran_in_store = random.randint(0, count-1)
                random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name=in_cart_list)[:4], key=lambda x: random.random())
                for i in random_menues:
                    actions.append(i)


    elif action ==2:
        # dish & dessert
        if in_cart_list:
            print("in_cart_list")
            counter = 0
            category_dict = {}
            for menu in in_cart_list:
                if "โรตี"  in menu.name or "ขนมปัง" in menu.name:
                    if "ของหวาน" in category_dict:
                        v = category_dict["ของหวาน"] 
                        new_val = int(v)+1
                        category_dict["ของหวาน"] = new_val
                    else:
                        category_dict["ของหวาน"]  = 1

                elif "ลูกชิ้น" in menu.name or "ไส้กรอก" in menu.name or "เฟรนซ์ฟราย" in menu.name or "มันบด" in menu.name or "มันอบ" in menu.name: 
                    if "ของทานเล่น" in category_dict:
                        v = category_dict["ของทานเล่น"] 
                        new_val = int(v)+1
                        category_dict["ของทานเล่น"] = new_val
                    else:
                        category_dict["ของทานเล่น"]  = 1


                elif "Soda" in menu.name or "ปั่น" in menu.name or "นมสด" in menu.name or "น้ำเต้าหู้" in menu.name or "แก้ว" in menu.name: 
                    if "เครื่องดื่ม" in category_dict:
                        v = category_dict["เครื่องดื่ม"] 
                        new_val = int(v)+1
                        category_dict["เครื่องดื่ม"] = new_val
                    else:
                        category_dict["เครื่องดื่ม"]  = 1      

                else:
                    store=Store.objects.get(id=menu.store.id)
                    if store.category in category_dict:
                        v = category_dict[store.category] 
                        new_val = int(v)+1
                        category_dict[store.category] = new_val
                    else:
                        category_dict[store.category]  = 1

            print("category_dict",category_dict)
            max_cate = max(category_dict.items(), key=operator.itemgetter(1))[0]
            print("max_cate",max_cate)
            if max_cate == "อาหารไทย":
                # if "เครื่องดื่ม" not in category_dict:
                if category_dict["เครื่องดื่ม"] < category_dict["ของหวาน"] and category_dict["เครื่องดื่ม"] < category_dict["ของทานเล่น"]:
                    # have some drink
                
                    print("not drink")
                    keys = ['ปั่น',"แก้ว","นมสด","น่ำเต้าหู้","Soda"]
                    drink_list = []
                    # query = functools.reduce(operator.and_, (Q(name__contains = item) for item in ['ปั่น',]))
                    # result = Menu.objects.filter(query)
                    # drink = Menu.objects.annotate(search=SearchVector( 'name')).filter(name__in=["ปั่น",'แก้ว'])
                    # drink = Menu.objects.filter(Q(name__iendswith='ปั่น') | Q(name__icontains='แก้ว'))
                    # print("drink",drink)
                    for k in keys:
                        drink = Menu.objects.filter(name__contains=k)
                        if drink:
                            for d in drink:
                                if d not in in_cart_list:
                                    drink_list.append(d)
                
                    drink2 = Menu.objects.filter(store__id=15)# pangyen
                    for d in drink2:
                        if d not in in_cart_list:
                            drink_list.append(d)
                    
                    # add drink
                    count = len(drink_list)
                    temp = -1
                    for i in range(2):
                        print("i")
                        ran_drink_list = random.randint(0, count-1)
                        while temp == ran_drink_list:
                            ran_drink_list = random.randint(0, count-1)

                        actions.append(drink_list[ran_drink_list])
                        temp = ran_drink_list

                    if category_dict["ของหวาน"] == category_dict["ของทานเล่น"]:
                        count = len(drink_list)
                        # temp = -1
                        for i in range(2):
                            print("i")
                            ran_drink_list = random.randint(0, count-1)
                            temp = drink_list[ran_drink_list]
                            while temp in in_cart_list or temp in actions:
                                ran_drink_list = random.randint(0, count-1)
                                temp = drink_list[ran_drink_list]
                            actions.append(temp)
                            # temp = ran_drink_list
                        print("actions",actions)


                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        dessert_list = []
                        keys = ['โรตี',"ขนมปัง",]
                        for k in keys:
                            dessert = Menu.objects.filter(name__contains=k)
                            if dessert:
                                for d in dessert:
                                    if d not in in_cart_list:
                                        dessert_list.append(d)
                        dessert2 = Menu.objects.filter(store__id=14)
                        for d in dessert2:
                            if d not in in_cart_list:
                                dessert_list.append(d)

                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        snack_list = []
                        snack = Menu.objects.filter(store__id=17) # somjai lookchin
                        # keys = ['โรตี',"ขนมปัง",]
                        for s in snack:
                            if s not in in_cart_list:
                                snack_list.append(s)
                        frenchfries = Menu.objects.get(id=156)
                        nuggets = Menu.objects.get(id=155)
                        snack_list.append(frenchfries)
                        snack_list.append(nuggets)
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list


                    print("drink")

                    # a = sorted(drink_list, key=lambda x: random.random())
                    # print("a",a[:4])
                    # dessert_store = Store.objects.filter(tags= )
                elif category_dict["เครื่องดื่ม"] >= category_dict["ของหวาน"] or category_dict["เครื่องดื่ม"] >= category_dict["ของทานเล่น"]:
                    # have some drink
                    print("เครื่องดื่ม > ขนม")
                    dessert_list = []
                    keys = ['โรตี',"ขนมปัง",]
                    for k in keys:
                        dessert = Menu.objects.filter(name__contains=k)
                        if dessert:
                            for d in dessert:
                                if d not in in_cart_list:
                                    dessert_list.append(d)
                    keys = ["น้ำเปล่า","แก้ว","ปั่น"]
                    # temp = []
                  
                    dessert2 = Menu.objects.filter(store__id=14)
                        # .exclude(name__contains=k)
                        # temp.append(dessert2)
                    for d in dessert2:
                        if d not in in_cart_list:
                            if "น้ำเปล่า" not in d.name and "แก้ว" not in d.name and "ปั่น" not in d.name:
                                dessert_list.append(d)

                    snack_list = []
                    snack = Menu.objects.filter(store__id=17) # somjai lookchin
                    for s in snack:
                        if s not in in_cart_list:
                            snack_list.append(s)
                    frenchfries = Menu.objects.get(id=156)
                    nuggets = Menu.objects.get(id=155)
                    snack_list.append(frenchfries)
                    snack_list.append(nuggets)

                    if category_dict["ของหวาน"] ==category_dict["ของทานเล่น"]:

                    # if "ของหวาน" not in category and "ของทานเล่น" in category_dict:
                       
                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list

                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        print("ของหวาน < ทานเล่น")
                        # add dessert 
                        count = len(dessert_list)
                        for i in range(3):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            temp = dessert_list[ran_dessert_list]
                            while temp in in_cart_list or temp in actions:
                                ran_dessert_list = random.randint(0, count-1)
                                temp = dessert_list[ran_dessert_list]
                            actions.append(temp)

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        ran_snack_list = random.randint(0, count-1)
                        actions.append(snack_list[ran_snack_list])

                       
                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        
                        # add dessert 
                        count = len(dessert_list)
                        ran_dessert_list = random.randint(0, count-1)
                        actions.append(dessert_list[ran_dessert_list])
       
                        # add snack 
                        count = len(snack_list)
                        for i in range(3):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            temp = snack_list[ran_snack_list]
                            while temp in in_cart_list or temp in actions:
                                ran_snack_list = random.randint(0, count-1)
                                temp = snack_list[ran_snack_list]
                            actions.append(temp)
            else:
                keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
                dish_list = []
                for k in keys:
                    dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
                    for d in dish:
                        if d not in in_cart_list:
                            dish_list.append(d)
                count = len(dish_list)
                for i in range(4):
                    print("i")
                    ran_dish_list = random.randint(0, count-1)
                    temp = dish_list[ran_dish_list]
                    while temp in in_cart_list or temp in actions:
                        ran_dish_list = random.randint(0, count-1)
                        temp = dish_list[ran_dish_list]
                    actions.append(temp)
                # drink & dessert & snack is most
                # dish_store = Store.objects.filter(category="อาหารไทย")
                


            print("actions",actions)
            for i in actions:
                print("store", i.store)
                    

        else: # not have item in cart
            pass
        # next_state = action
        # print("next_state",next_state)



        # print("random 6-8",np.random.randint(6,9))
    # state,num_actions,actions = createActions(request,state)
    return render(request, 'tohroong.html',{'actions':actions,
        'state':state,
        'num_actions':action,'next_state':next_state,'in_cart_list':in_cart_list})

# def recommendation_actions(request,state):
#     gamma = 0.8
    
    

   
# # state 6 7 8 
#     # tohroong 's page is state = 0 
#     if state == 2 or state == 5 or state == 8:
#         next_state = state # isGoal == True      
#     else:
#         next_state = state +1
#         # num_actions =0
#         # actions = 0 
#         # valid_moves = R[state] >= 0
#     q_table = QTableLocal.objects.get(user=request.user)
#     print("q_table",q_table)
#     R = np.array(q_table.R_array)
#     print("RRRRRRRR",R)
#     current_state_row = R[state,]
#     print("R[state,]",R[state,])
#     Q,R = getTable(request)
#     # av_act = np.where(current_state_row >= 0)[0]
#     # action = int(np.random.choice(av_act,size=1))

#     actions = np.where(Q[state]== np.max(Q[state]))[0]

#     if actions.shape[0] >1:
#         action = int(np.random.choice(actions,size=1))
#     else:
#         action = int(actions)

#     in_cart_list = check_item_in_cart(request)
#     actions=[]
    
#     print("Q",Q)
#     print("R",R)  
#     print("actions",action)          
#         # if item_in_cart:
#         #     print("item_in_cartitem_in_cartitem_in_cartitem_in_cart")
#         # else:
#         #     print("item_in_cart",item_in_cart)
#     # action = 0
#     if action == 0:
#         # Top-N
        
#         all_ordered = Order.objects.filter(user=request.user)
#         logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")
#         # print("logs",logs)
#         print("len(all_ordered)",len(all_ordered))
#         # allOrdered = Order.objects.filter(created_at__gte=datetime.today()-timedelta(days=5))

#         # actions.append(sorted_dict[:4])
#         print("actions sorted_dict[:4]",actions)
      


#         if len(all_ordered) == 0 and len(logs) == 0:
#             fiveDaysAgo = datetime.today() - timedelta(days=25)
#             allOrdered = Order.objects.filter(created_at__gte=fiveDaysAgo)

#             # print("allOrdered",allOrdered)
#             allo_dict = {}
#             allorder_list = []
#             for i in allOrdered:
#                 print("i",i.menu)

#                 for menu_id,amount in zip(i.menu,i.amount):
                 
#                     try:
#                         int(menu_id)
#                         m = Menu.objects.get(id=menu_id)
                    
#                     except Exception as e:
#                         print("exc_clear",menu_id)
#                         tuple_menu = literal_eval(menu_id)
#                         m = Menu.objects.get(id=tuple_menu[0])
                      
#                     if m in allo_dict:
#                         v = allo_dict[m] 
#                         new_val = int(v)+1
#                         allo_dict[m] = new_val
#                     else:
#                         # first time add 
#                         allo_dict[m] = int(amount)

#             print("allo_dict",allo_dict)

#             mostOrdered = max(allo_dict.items(), key=operator.itemgetter(1))[0]
#             sorted_dict = sorted(allo_dict, key=allo_dict.get, reverse=True)
#             print("mostOrdered",mostOrdered)
#             print("sorted_dict",sorted_dict[:4])
#             for a in sorted_dict[:4]:
#                 actions.append(a)
            

            
#         elif len(all_ordered) == 0 and len(logs) >= 1:

#             for i in range(4):
#                 count = len(in_cart_list)
#                 ran_num = random.randint(0, count-1)
#                 menu = in_cart_list[ran_num]
#                 menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
#                 count = len(menu_list)
#                 ran_in_store = random.randint(0, count-1)
#                 actions.append(menu_list[ran_in_store])
         

#             print("actionsssss",actions)

#         elif len(all_ordered) >= 1 and len(logs) >= 1:
#             # have ordered and have session
#             o_dict = {}
#             order_list = []
#             if len(all_ordered) >=1 and len(all_ordered) <=5:
#                 last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
#                 # print("last_2_ordered",last_2_ordered)
#             elif len(all_ordered) >=5:
#                 last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
#                 # print("last_3_ordered",last_3_ordered)
#             for i in last_ordered:

#                 for menu_id,amount in zip(i.menu,i.amount):
                 
#                     try:
#                         int(menu_id)
#                         m = Menu.objects.get(id=menu_id)
                    
#                     except Exception as e:
#                         tuple_menu = literal_eval(m)
#                         m = Menu.objects.get(id=tuple_menu[0])
                      
#                     if m in o_dict:
#                         v = o_dict[m] 
#                         new_val = int(v)+1
#                         o_dict[m] = new_val
#                     else:
#                         # first time add 
#                         o_dict[m] = int(amount)

#             print("o_dict ee",o_dict)      
#             most_ordered = max(o_dict.items(), key=operator.itemgetter(1))[0]
#             sorted_dict = sorted(o_dict, key=o_dict.get, reverse=True)
#             print("most_ordered",most_ordered)
#             print("sorted_dict",sorted_dict)
#             print("in_cart_list",in_cart_list)
#             print("in_cart_list",len(in_cart_list))

#             count = 0
#             for i in sorted_dict:
                
#                 # most_add_to_cart = i
#                 if count == 2:
#                     break
#                 else:
#                     print("i",i)
#                     if i not in in_cart_list:
#                         actions.append(i)
#                         count +=1
#                     else:
#                         print("incart")
#             print("actions",actions)
#             print("else",count)
#             add_list = []
#             for i in logs:
#                 add_list.append(i.value)
#                 # print("เพิ่มเข้าตะกร้า",i.value)
#             my_dict = {i:add_list.count(i) for i in add_list}
#             print("my_dict",my_dict)
#             most_add_to_cart = max(my_dict.items(), key=operator.itemgetter(1))[0]
#             sorted_dict = sorted(my_dict, key=my_dict.get, reverse=True)
#             print("most_add_to_cart most_add_to_cart",most_add_to_cart)
#             # print("in_cart_list ",in_cart_list)
#             count = 0
#             more_actions = 4-len(actions)
          
#             for i in sorted_dict:
#                 if count == more_actions:
#                     break
#                 else:
#                     sp = i.split(",")
#                     # print("sp",sp)
#                     # print("en(sp)",len(sp))
#                     if len(sp) > 1: # id,บะหมี่
               
#                         m = Menu.objects.get(id=sp[0])
                    
#                     elif len(sp) == 1: # บะหมี่
#                         menu = Menu.objects.filter(name=sp[0])
#                         if len(menu) == 1:
#                             m = Menu.objects.get(name=i)
            
#                     if m not in in_cart_list:
#                         if m not in actions:
#                             count+=1
#                             actions.append(m)
#             print("actions a",actions)
#             num_loop = 4-len(actions)
#             print("xxxx")
#             if num_loop >0:
#                 print("xxxx",num_loop)
#                 for i in range(num_loop):
#                     count = len(in_cart_list)
#                     ran_num = random.randint(0, count-1)
#                     menu = in_cart_list[ran_num]
#                     menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
#                     count = len(menu_list)
#                     ran_in_store = random.randint(0, count-1)
#                     actions.append(menu_list[ran_in_store])

#             print("actions b",actions)
        
#         # return state,action,actions  
#     elif action ==1:
#         # same things 
#         all_ordered = Order.objects.filter(user=request.user)
#         logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")


#         if len(all_ordered) == 0 and len(logs) == 0:
#             fiveDaysAgo = datetime.today() - timedelta(days=25)
#             allOrdered = Order.objects.filter(created_at__gte=fiveDaysAgo)

#             # print("allOrdered",allOrdered)
#             allo_dict = {}
#             allorder_list = []
#             for i in allOrdered:
#                 print("i",i.menu)

#                 for menu_id,amount in zip(i.menu,i.amount):
                 
#                     try:
#                         int(menu_id)
#                         m = Menu.objects.get(id=menu_id)
                    
#                     except Exception as e:
#                         print("exc_clear",menu_id)
#                         tuple_menu = literal_eval(menu_id)
#                         m = Menu.objects.get(id=tuple_menu[0])
                      
#                     if m in allo_dict:
#                         v = allo_dict[m] 
#                         new_val = int(v)+1
#                         allo_dict[m] = new_val
#                     else:
#                         # first time add 
#                         allo_dict[m] = int(amount)

#             print("allo_dict",allo_dict)

#             mostOrdered = max(allo_dict.items(), key=operator.itemgetter(1))[0]
#             sorted_dict = sorted(allo_dict, key=allo_dict.get, reverse=True)
#             print("mostOrdered",mostOrdered)
#             print("sorted_dict",sorted_dict[:4])
#             for a in sorted_dict[:4]:
#                 actions.append(a)
#         elif len(all_ordered) == 0 and len(logs) >= 1:
#             for i in range(4):
#                 count = len(in_cart_list)
#                 ran_num = random.randint(0, count-1)
#                 menu = in_cart_list[ran_num]
#                 menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
#                 count = len(menu_list)
#                 ran_in_store = random.randint(0, count-1)
#                 actions.append(menu_list[ran_in_store])
         

#             print("actionsssss",actions)
#         elif len(all_ordered) >= 1 :
#             if len(all_ordered) >=1 and len(all_ordered) <=2:
#                 last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
#                 # print("last_2_ordered",last_2_ordered)
#             elif len(all_ordered) >=3:
#                 last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
#             print("last_ordered",last_ordered)
#             o_dict = {}
#             order_list = []
#             for i in last_ordered:

#                 for menu_id,amount in zip(i.menu,i.amount):
                 
#                     try:
#                         int(menu_id)
#                         m = Menu.objects.get(id=menu_id)
                    
#                     except Exception as e:
#                         tuple_menu = literal_eval(m)
#                         m = Menu.objects.get(id=tuple_menu[0])
                      
#                     if m in o_dict:
#                         v = o_dict[m] 
#                         new_val = int(v)+1
#                         o_dict[m] = new_val
#                     else:
#                         # first time add 
#                         o_dict[m] = int(amount)

#             print("o_dict o_dict",o_dict)  
#             dict_store_tags ={}
#             for o in o_dict:
#                 # dic = {'name':'', 'count' : 0}
#                 tag, counter = check_tag(o)
#                 print("store_name",tag)
#                 print("counter",counter)   

#                 if counter > 0:
#                     if tag in dict_store_tags:
#                         v = dict_store_tags[tag] 
#                         new_val = int(v)+counter
#                         dict_store_tags[tag] = new_val
#                     else:
#                         dict_store_tags[tag] = counter

#             print("dict_store_tags",dict_store_tags)
#             # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
#             sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
#             print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
#             # print("most_tags",most_tags)
#             if len(sorted_dict_store_tags) >=2:  
#                 most_tags = sorted_dict_store_tags[:2]
#                 for m in most_tags:
#                     stores = Store.objects.filter(tags__icontains=m)
#                     count = len(stores)
#                     ran_in_store = random.randint(0, count-1)
#                     random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name=in_cart_list)[:2], key=lambda x: random.random())
           
#                     for i in random_menues:
#                         actions.append(i)
#             elif len(sorted_dict_store_tags)==1:
#                 most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
#                 stores = Store.objects.filter(tags__icontains=m)
#                 count = len(stores)
#                 ran_in_store = random.randint(0, count-1)
#                 random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name=in_cart_list)[:4], key=lambda x: random.random())
#                 for i in random_menues:
#                     actions.append(i)


#     elif action ==2:
#         # dish & dessert
#         if in_cart_list:
#             print("in_cart_list")
#             counter = 0
#             category_dict = {"ของหวาน":0,"ของทานเล่น":0,"เครื่องดื่ม":0}
#             for menu in in_cart_list:
#                 if "โรตี"  in menu.name or "ขนมปัง" in menu.name:
#                     if "ของหวาน" in category_dict:
#                         v = category_dict["ของหวาน"] 
#                         new_val = int(v)+1
#                         category_dict["ของหวาน"] = new_val
#                     else:
#                         category_dict["ของหวาน"]  = 1

#                 elif "ลูกชิ้น" in menu.name or "ไส้กรอก" in menu.name or "เฟรนซ์ฟราย" in menu.name or "มันบด" in menu.name or "มันอบ" in menu.name: 
#                     if "ของทานเล่น" in category_dict:
#                         v = category_dict["ของทานเล่น"] 
#                         new_val = int(v)+1
#                         category_dict["ของทานเล่น"] = new_val
#                     else:
#                         category_dict["ของทานเล่น"]  = 1


#                 elif "Soda" in menu.name or "ปั่น" in menu.name or "นมสด" in menu.name or "น้ำเต้าหู้" in menu.name or "แก้ว" in menu.name: 
#                     if "เครื่องดื่ม" in category_dict:
#                         v = category_dict["เครื่องดื่ม"] 
#                         new_val = int(v)+1
#                         category_dict["เครื่องดื่ม"] = new_val
#                     else:
#                         category_dict["เครื่องดื่ม"]  = 1      

#                 else:
#                     store=Store.objects.get(id=menu.store.id)
#                     if store.category in category_dict:
#                         v = category_dict[store.category] 
#                         new_val = int(v)+1
#                         category_dict[store.category] = new_val
#                     else:
#                         category_dict[store.category]  = 1

#             print("category_dict",category_dict)
#             max_cate = max(category_dict.items(), key=operator.itemgetter(1))[0]
#             print("max_cate",max_cate)
#             if max_cate == "อาหารไทย":
#                 # if "เครื่องดื่ม" not in category_dict:
#                 if category_dict["เครื่องดื่ม"] < category_dict["ของหวาน"] and category_dict["เครื่องดื่ม"] < category_dict["ของทานเล่น"]:
#                     # have some drink
                
#                     print("not drink")
#                     keys = ['ปั่น',"แก้ว","นมสด","น่ำเต้าหู้","Soda"]
#                     drink_list = []
#                     # query = functools.reduce(operator.and_, (Q(name__contains = item) for item in ['ปั่น',]))
#                     # result = Menu.objects.filter(query)
#                     # drink = Menu.objects.annotate(search=SearchVector( 'name')).filter(name__in=["ปั่น",'แก้ว'])
#                     # drink = Menu.objects.filter(Q(name__iendswith='ปั่น') | Q(name__icontains='แก้ว'))
#                     # print("drink",drink)
#                     for k in keys:
#                         drink = Menu.objects.filter(name__contains=k)
#                         if drink:
#                             for d in drink:
#                                 if d not in in_cart_list:
#                                     drink_list.append(d)
                
#                     drink2 = Menu.objects.filter(store__id=15)# pangyen
#                     for d in drink2:
#                         if d not in in_cart_list:
#                             drink_list.append(d)
                    
#                     # add drink
#                     count = len(drink_list)
#                     temp = -1
#                     for i in range(2):
#                         print("i")
#                         ran_drink_list = random.randint(0, count-1)
#                         while temp == ran_drink_list:
#                             ran_drink_list = random.randint(0, count-1)

#                         actions.append(drink_list[ran_drink_list])
#                         temp = ran_drink_list

#                     if category_dict["ของหวาน"] == category_dict["ของทานเล่น"]:
#                         count = len(drink_list)
#                         # temp = -1
#                         for i in range(2):
#                             print("i")
#                             ran_drink_list = random.randint(0, count-1)
#                             temp = drink_list[ran_drink_list]
#                             while temp in in_cart_list or temp in actions:
#                                 ran_drink_list = random.randint(0, count-1)
#                                 temp = drink_list[ran_drink_list]
#                             actions.append(temp)
#                             # temp = ran_drink_list
#                         print("actions",actions)


#                     elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
#                         dessert_list = []
#                         keys = ['โรตี',"ขนมปัง",]
#                         for k in keys:
#                             dessert = Menu.objects.filter(name__contains=k)
#                             if dessert:
#                                 for d in dessert:
#                                     if d not in in_cart_list:
#                                         dessert_list.append(d)
#                         dessert2 = Menu.objects.filter(store__id=14)
#                         for d in dessert2:
#                             if d not in in_cart_list:
#                                 dessert_list.append(d)

                        
#                         # add dessert 
#                         count = len(dessert_list)
#                         temp = -1
#                         for i in range(2):
#                             print("i")
#                             ran_dessert_list = random.randint(0, count-1)
#                             while temp == ran_dessert_list:
#                                 ran_dessert_list = random.randint(0, count-1)

#                             actions.append(dessert_list[ran_dessert_list])
#                             temp = ran_dessert_list

#                     elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
#                         snack_list = []
#                         snack = Menu.objects.filter(store__id=17) # somjai lookchin
#                         # keys = ['โรตี',"ขนมปัง",]
#                         for s in snack:
#                             if s not in in_cart_list:
#                                 snack_list.append(s)
#                         frenchfries = Menu.objects.get(id=156)
#                         nuggets = Menu.objects.get(id=155)
#                         snack_list.append(frenchfries)
#                         snack_list.append(nuggets)
#                         # add snack 
#                         count = len(snack_list)
#                         temp = -1
#                         for i in range(2):
#                             print("i")
#                             ran_snack_list = random.randint(0, count-1)
#                             while temp == ran_snack_list:
#                                 ran_snack_list = random.randint(0, count-1)

#                             actions.append(snack_list[ran_snack_list])
#                             temp = ran_snack_list


#                     print("drink")

#                     # a = sorted(drink_list, key=lambda x: random.random())
#                     # print("a",a[:4])
#                     # dessert_store = Store.objects.filter(tags= )
#                 elif category_dict["เครื่องดื่ม"] >= category_dict["ของหวาน"] or category_dict["เครื่องดื่ม"] >= category_dict["ของทานเล่น"]:
#                     # have some drink
#                     print("เครื่องดื่ม > ขนม")
#                     dessert_list = []
#                     keys = ['โรตี',"ขนมปัง",]
#                     for k in keys:
#                         dessert = Menu.objects.filter(name__contains=k)
#                         if dessert:
#                             for d in dessert:
#                                 if d not in in_cart_list:
#                                     dessert_list.append(d)
#                     keys = ["น้ำเปล่า","แก้ว","ปั่น"]
#                     # temp = []
                  
#                     dessert2 = Menu.objects.filter(store__id=14)
#                         # .exclude(name__contains=k)
#                         # temp.append(dessert2)
#                     for d in dessert2:
#                         if d not in in_cart_list:
#                             if "น้ำเปล่า" not in d.name and "แก้ว" not in d.name and "ปั่น" not in d.name:
#                                 dessert_list.append(d)

#                     snack_list = []
#                     snack = Menu.objects.filter(store__id=17) # somjai lookchin
#                     for s in snack:
#                         if s not in in_cart_list:
#                             snack_list.append(s)
#                     frenchfries = Menu.objects.get(id=156)
#                     nuggets = Menu.objects.get(id=155)
#                     snack_list.append(frenchfries)
#                     snack_list.append(nuggets)

#                     if category_dict["ของหวาน"] ==category_dict["ของทานเล่น"]:

#                     # if "ของหวาน" not in category and "ของทานเล่น" in category_dict:
                       
                        
#                         # add dessert 
#                         count = len(dessert_list)
#                         temp = -1
#                         for i in range(2):
#                             print("i")
#                             ran_dessert_list = random.randint(0, count-1)
#                             while temp == ran_dessert_list:
#                                 ran_dessert_list = random.randint(0, count-1)

#                             actions.append(dessert_list[ran_dessert_list])
#                             temp = ran_dessert_list

#                     # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
#                         # add snack 
#                         count = len(snack_list)
#                         temp = -1
#                         for i in range(2):
#                             print("i")
#                             ran_snack_list = random.randint(0, count-1)
#                             while temp == ran_snack_list:
#                                 ran_snack_list = random.randint(0, count-1)

#                             actions.append(snack_list[ran_snack_list])
#                             temp = ran_snack_list

#                     elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
#                         print("ของหวาน < ทานเล่น")
#                         # add dessert 
#                         count = len(dessert_list)
#                         for i in range(3):
#                             print("i")
#                             ran_dessert_list = random.randint(0, count-1)
#                             temp = dessert_list[ran_dessert_list]
#                             while temp in in_cart_list or temp in actions:
#                                 ran_dessert_list = random.randint(0, count-1)
#                                 temp = dessert_list[ran_dessert_list]
#                             actions.append(temp)

#                     # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
#                         # add snack 
#                         count = len(snack_list)
#                         ran_snack_list = random.randint(0, count-1)
#                         actions.append(snack_list[ran_snack_list])

                       
#                     elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        
#                         # add dessert 
#                         count = len(dessert_list)
#                         ran_dessert_list = random.randint(0, count-1)
#                         actions.append(dessert_list[ran_dessert_list])
       
#                         # add snack 
#                         count = len(snack_list)
#                         for i in range(3):
#                             print("i")
#                             ran_snack_list = random.randint(0, count-1)
#                             temp = snack_list[ran_snack_list]
#                             while temp in in_cart_list or temp in actions:
#                                 ran_snack_list = random.randint(0, count-1)
#                                 temp = snack_list[ran_snack_list]
#                             actions.append(temp)
#             else:
#                 keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
#                 dish_list = []
#                 for k in keys:
#                     dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
#                     for d in dish:
#                         if d not in in_cart_list:
#                             dish_list.append(d)
#                 count = len(dish_list)
#                 for i in range(4):
#                     print("i")
#                     ran_dish_list = random.randint(0, count-1)
#                     temp = dish_list[ran_dish_list]
#                     while temp in in_cart_list or temp in actions:
#                         ran_dish_list = random.randint(0, count-1)
#                         temp = dish_list[ran_dish_list]
#                     actions.append(temp)
#                 # drink & dessert & snack is most
#                 # dish_store = Store.objects.filter(category="อาหารไทย")
                


#             print("actions",actions)
#             for i in actions:
#                 print("store", i.store)
                    

#         else: # not have item in cart
#             keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
#             dish_list = []
#             for k in keys:
#                 dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
#                 for d in dish:
#                     if d not in in_cart_list:
#                         dish_list.append(d)
#             count = len(dish_list)
#             for i in range(2):
#                 print("i")
#                 ran_dish_list = random.randint(0, count-1)
#                 temp = dish_list[ran_dish_list]
#                 while temp in in_cart_list or temp in actions:
#                     ran_dish_list = random.randint(0, count-1)
#                     temp = dish_list[ran_dish_list]
#                 actions.append(temp)

#                 dessert_list = []
#                 keys = ['โรตี',"ขนมปัง",]
#                 for k in keys:
#                     dessert = Menu.objects.filter(name__contains=k)
#                     if dessert:
#                         for d in dessert:
#                             if d not in in_cart_list:
#                                 dessert_list.append(d)
#                 dessert2 = Menu.objects.filter(store__id=14)
#                 for d in dessert2:
#                     if d not in in_cart_list:
#                         dessert_list.append(d)

                
#                 # add dessert 
#                 count = len(dessert_list)
#                 temp = -1
#                 for i in range(2):
#                     print("i")
#                     ran_dessert_list = random.randint(0, count-1)
#                     while temp == ran_dessert_list:
#                         ran_dessert_list = random.randint(0, count-1)

#                     actions.append(dessert_list[ran_dessert_list])
#                     temp = ran_dessert_list


#     num_actions = action

#     return actions,num_actions,next_state

def getMostOrderInFiveDaysAgo(request):
    actions = []
    fiveDaysAgo = datetime.today() - timedelta(days=25)
    allOrdered = Order.objects.filter(created_at__gte=fiveDaysAgo)

    # print("allOrdered",allOrdered)
    allo_dict = {}
    allorder_list = []
    for i in allOrdered:
       

        for menu_id,amount in zip(i.menu,i.amount):
         
            try:
                int(menu_id)
                m = Menu.objects.get(id=menu_id)
                if m.store.id != 24:
                    if m.store.id ==25:
                        if m.id !=504: #not set salad
                            if m in allo_dict:
                                v = allo_dict[m] 
                                new_val = int(v)+1
                                allo_dict[m] = new_val
                            else:
                                # first time add 
                                allo_dict[m] = int(amount)
                            # add_list.append(i.value)
                    else:
                        # add_list.append(i.value)
                        if m in allo_dict:
                            v = allo_dict[m] 
                            new_val = int(v)+1
                            allo_dict[m] = new_val
                        else:
                            # first time add 
                            allo_dict[m] = int(amount)
            
            except Exception as e:
                pass
      
    print("allo_dict",allo_dict)

    mostOrdered = max(allo_dict.items(), key=operator.itemgetter(1))[0]
    sorted_dict = sorted(allo_dict, key=allo_dict.get, reverse=True)
    print("mostOrdered",mostOrdered)
    print("sorted_dict",sorted_dict[:4])
    for a in sorted_dict[:4]:
        actions.append(a)
    return actions
def recommendation_actions(request,state):
    gamma = 0.8

    if state == 2 or state == 5 or state == 8:
        next_state = state # isGoal == True      
    else:
        next_state = state +1
      
    q_table = QTableLocal.objects.get(user=request.user)
    print("q_table",q_table)
    R = np.array(q_table.R_array)
    print("RRRRRRRR",R)
    current_state_row = R[state,]
    print("R[state,]",R[state,])
    Q,R = getLocalTable(request)
    # av_act = np.where(current_state_row >= 0)[0]
    # action = int(np.random.choice(av_act,size=1))
    epsilon = 0.0
    ran = np.random.rand()
    if ran > epsilon:
        actions = np.where(Q[state]== np.max(Q[state]))[0]
    elif ran <= epsilon:
        actions = np.where(Q[state]== np.min(Q[state]))[0]

    

    if actions.shape[0] >1:
        action = int(np.random.choice(actions,size=1))
    else:
        action = int(actions)

    in_cart_list = check_item_in_cart(request)
    actions=[]
    
    print("Q",Q)
    print("R",R)  
    print("actions",action)          
        # if item_in_cart:
        #     print("item_in_cartitem_in_cartitem_in_cartitem_in_cart")
        # else:
        #     print("item_in_cart",item_in_cart)
    # action =1
    if action == 0:
        # Top-N
        
        all_ordered = Order.objects.filter(user=request.user)
        logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")
        # print("logs",logs)
        print("len(all_ordered)",len(all_ordered))
        # allOrdered = Order.objects.filter(created_at__gte=datetime.today()-timedelta(days=5))

        # actions.append(sorted_dict[:4])
        print("actions sorted_dict[:4]",actions)
      


        if len(all_ordered) == 0 and len(logs) == 0:
            actions = getMostOrderInFiveDaysAgo(request)
            
            

            
        elif len(all_ordered) == 0 and len(logs) >= 1:
            if in_cart_list:
                for i in range(4):
                    count = len(in_cart_list)
                    ran_num = random.randint(0, count-1)
                    menu = in_cart_list[ran_num]
                    menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                    count = len(menu_list)
                    ran_in_store = random.randint(0, count-1)
                    actions.append(menu_list[ran_in_store])
         
            else:
                actions = getMostOrderInFiveDaysAgo(request)
            print("actionsssss",actions)

        elif len(all_ordered) >= 1 and len(logs) >= 1:
            # have ordered and have session
            if in_cart_list:

                o_dict = {}
                order_list = []
                if len(all_ordered) >=1 and len(all_ordered) <=5:
                    last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
                    # print("last_2_ordered",last_2_ordered)
                elif len(all_ordered) >=5:
                    last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
                    # print("last_3_ordered",last_3_ordered)
                for i in last_ordered:

                    for menu_id,amount in zip(i.menu,i.amount):
                     
                        try:
                            int(menu_id)
                            m = Menu.objects.get(id=menu_id)
                            if m.store.id != 24:
                                if m.store.id ==25:
                                    if m.id !=504: #not set salad
                                        if m in o_dict:
                                            v = o_dict[m] 
                                            new_val = int(v)+1
                                            o_dict[m] = new_val
                                        else:
                                            # first time add 
                                            o_dict[m] = int(amount)
                                        # add_list.append(i.value)
                                else:
                                    # add_list.append(i.value)
                                    if m in o_dict:
                                        v = o_dict[m] 
                                        new_val = int(v)+1
                                        o_dict[m] = new_val
                                    else:
                                        # first time add 
                                        o_dict[m] = int(amount)
                        
                        except Exception as e:
                            pass
                            # tuple_menu = literal_eval(m)
                            # m = Menu.objects.get(id=tuple_menu[0])
                          
                        

                print("o_dict ee",o_dict)      
                most_ordered = max(o_dict.items(), key=operator.itemgetter(1))[0]
                sorted_dict = sorted(o_dict, key=o_dict.get, reverse=True)
                print("most_ordered",most_ordered)
                print("sorted_dict",sorted_dict)
                print("in_cart_list",in_cart_list)
                print("in_cart_list",len(in_cart_list))

                count = 0
                for i in sorted_dict:
                    
                    # most_add_to_cart = i
                    if count == 2:
                        break
                    else:
                        print("i",i)
                        if i not in in_cart_list:
                            actions.append(i)
                            count +=1
                        else:
                            print("incart")
                print("actions",actions)
                print("else",count)
                add_list = []
                for i in logs:
                    # if
                    sp = i.value.split(",")
                    if len(sp) >1:
                        menu = Menu.objects.get(id=sp[0])
              
                        if menu.store.id != 24:
                            if menu.store.id ==25:
                                if menu.id !=504: #not set salad
                                    add_list.append(i.value)
                            else:
                                add_list.append(i.value)
                    elif len(sp) == 1:
                        m = Menu.objects.filter(name=sp[0])
                        if len(m) == 1:
                            menu= Menu.objects.get(name=sp[0])
                            # print("menuuuu",menu)
                            if menu.store.id != 24:
                                if menu.store.id ==25:
                                    if menu.id !=504: #not set salad
                                        add_list.append(i.value)
                                else:
                                    add_list.append(i.value)
                                # print("i.val",i.value)

                    # print("เพิ่มเข้าตะกร้า",i.value)
                my_dict = {i:add_list.count(i) for i in add_list}
                print("my_dictttttttrlrlrlrlrllrrllrrlrll",my_dict)
                most_add_to_cart = max(my_dict.items(), key=operator.itemgetter(1))[0]
                sorted_dict = sorted(my_dict, key=my_dict.get, reverse=True)
                print("most_add_to_cart most_add_to_cart",most_add_to_cart)
                # print("in_cart_list ",in_cart_list)
                count = 0
                more_actions = 4-len(actions)
              
                for i in sorted_dict:
                    if count == more_actions:
                        break
                    else:
                        sp = i.split(",")
                        # print("sp",sp)
                        # print("en(sp)",len(sp))
                        if len(sp) > 1: # id,บะหมี่
                   
                            m = Menu.objects.get(id=sp[0])
                        
                        elif len(sp) == 1: # บะหมี่
                            menu = Menu.objects.filter(name=sp[0])
                            if len(menu) == 1:
                                m = Menu.objects.get(name=sp[0])
                
                        if m not in in_cart_list:
                            if m not in actions:
                                count+=1
                                actions.append(m)
                print("actions a",actions)
                num_loop = 4-len(actions)
                print("xxxx")
                if num_loop >0:
                    print("xxxx",num_loop)
                    for i in range(num_loop):
                        count = len(in_cart_list)
                        ran_num = random.randint(0, count-1)
                        menu = in_cart_list[ran_num]
                        menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                        count = len(menu_list)
                        ran_in_store = random.randint(0, count-1)
                        actions.append(menu_list[ran_in_store])

                print("actions b",actions)
            else:
                print("ELSE")
                actions = getMostOrderInFiveDaysAgo(request)
        # return state,action,actions  
    elif action ==1:
        # same things 

        all_ordered = Order.objects.filter(user=request.user)
        logs = User_session.objects.filter(user=request.user,action="เพิ่มเข้าตะกร้า")


        if len(all_ordered) == 0 and len(logs) == 0:
            actions = getMostOrderInFiveDaysAgo(request)
            print("actionsactions",actions)
            
        elif len(all_ordered) == 0 and len(logs) >= 1:
            if in_cart_list:
                for i in range(4):
                    count = len(in_cart_list)
                    ran_num = random.randint(0, count-1)
                    menu = in_cart_list[ran_num]
                    menu_list = Menu.objects.filter(store=menu.store).exclude(name__in=in_cart_list)
                    count = len(menu_list)
                    ran_in_store = random.randint(0, count-1)
                    actions.append(menu_list[ran_in_store])
         
            else:
                add_list = []
                for i in logs:
                    # if
                    sp = i.value.split(",")
                    if len(sp) >1:
                        menu = Menu.objects.get(id=sp[0])
              
                        if menu.store.id != 24:
                            if menu.store.id ==25:
                                if menu.id !=504: #not set salad
                                    add_list.append(menu)
                            else:
                                add_list.append(menu)
                    elif len(sp) == 1:
                        m = Menu.objects.filter(name=sp[0])
                        if len(m) == 1:
                            menu= Menu.objects.get(name=sp[0])
                            # print("menuuuu",menu)
                            if menu.store.id != 24:
                                if menu.store.id ==25:
                                    if menu.id !=504: #not set salad
                                        add_list.append(menu)
                                else:
                                    add_list.append(menu)
                
         
                dict_store_tags ={}
                for i in add_list:
                    print("i",i)
                    # dic = {'name':'', 'count' : 0}
                    tag, counter = check_tag(i)
                    print("store_name",tag)
                    print("counter",counter)   

                    if counter > 0:
                        if tag in dict_store_tags:
                            v = dict_store_tags[tag] 
                            new_val = int(v)+counter
                            dict_store_tags[tag] = new_val
                        else:
                            dict_store_tags[tag] = counter

                print("dict_store_tags",dict_store_tags)
                # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
                print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
                # print("most_tags",most_tags)
                if len(sorted_dict_store_tags) >=2:  
                    most_tags = sorted_dict_store_tags[:2]
                    print("most_tags",most_tags)
                    for m in most_tags:
                        stores = Store.objects.filter(tags__icontains=m)
                        count = len(stores)
                        print("conuttttt",count)
                        ran_in_store = random.randint(0, count-1)
                        random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store])[:2], key=lambda x: random.random())
               
                        for i in random_menues:
                            print("i",i)
                            actions.append(i)

                elif len(sorted_dict_store_tags)==1:
                    print("elfiiiii")
                    most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                    stores = Store.objects.filter(tags__icontains=most_tags)
                    count = len(stores)
                    ran_in_store = random.randint(0, count-1)
                    random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store])[:4], key=lambda x: random.random())
                    for i in random_menues:
                        actions.append(i)

    
        elif len(all_ordered) >= 1 :
            if in_cart_list:
                dict_store_tags ={}
                for i in in_cart_list:
                    print("i",i)
                    # dic = {'name':'', 'count' : 0}
                    tag, counter = check_tag(i)
                    print("store_name",tag)
                    print("counter",counter)   

                    if counter > 0:
                        if tag in dict_store_tags:
                            v = dict_store_tags[tag] 
                            new_val = int(v)+counter
                            dict_store_tags[tag] = new_val
                        else:
                            dict_store_tags[tag] = counter

                print("dict_store_tags",dict_store_tags)
                # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
                print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
                # print("most_tags",most_tags)
                if len(sorted_dict_store_tags) >=2:  
                    most_tags = sorted_dict_store_tags[:2]
                    print("most_tags",most_tags)
                    for m in most_tags:
                        stores = Store.objects.filter(tags__icontains=m)
                        count = len(stores)
                        print("conuttttt",count)
                        ran_in_store = random.randint(0, count-1)
                        random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:2], key=lambda x: random.random())
               
                        for i in random_menues:
                            print("i",i)
                            actions.append(i)

                elif len(sorted_dict_store_tags)==1:
                    print("elfiiiii")
                    most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                    stores = Store.objects.filter(tags__icontains=most_tags)
                    count = len(stores)
                    ran_in_store = random.randint(0, count-1)
                    random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:4], key=lambda x: random.random())
                    for i in random_menues:
                        actions.append(i)
            else:
                # not item in cart
                add_list = []
                for i in logs:
                    # if
                    sp = i.value.split(",")
                    if len(sp) >1:
                        menu = Menu.objects.get(id=sp[0])
              
                        if menu.store.id != 24:
                            if menu.store.id ==25:
                                if menu.id !=504: #not set salad
                                    add_list.append(menu)
                            else:
                                add_list.append(menu)
                    elif len(sp) == 1:
                        m = Menu.objects.filter(name=sp[0])
                        if len(m) == 1:
                            menu= Menu.objects.get(name=sp[0])
                            # print("menuuuu",menu)
                            if menu.store.id != 24:
                                if menu.store.id ==25:
                                    if menu.id !=504: #not set salad
                                        add_list.append(menu)
                                else:
                                    add_list.append(menu)
                
         
                dict_store_tags ={}
                for i in add_list:
                    print("i",i)
                    # dic = {'name':'', 'count' : 0}
                    tag, counter = check_tag(i)
                    print("store_name",tag)
                    print("counter",counter)   

                    if counter > 0:
                        if tag in dict_store_tags:
                            v = dict_store_tags[tag] 
                            new_val = int(v)+counter
                            dict_store_tags[tag] = new_val
                        else:
                            dict_store_tags[tag] = counter

                print("dict_store_tags",dict_store_tags)
                # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
                print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
                # print("most_tags",most_tags)
                if len(sorted_dict_store_tags) >=2:  
                    most_tags = sorted_dict_store_tags[:2]
                    print("most_tags",most_tags)
                    for m in most_tags:
                        stores = Store.objects.filter(tags__icontains=m)
                        count = len(stores)
                        print("conuttttt",count)
                        ran_in_store = random.randint(0, count-1)
                        random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store])[:2], key=lambda x: random.random())
               
                        for i in random_menues:
                            print("i",i)
                            actions.append(i)

                elif len(sorted_dict_store_tags)==1:
                    print("elfiiiii")
                    most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                    stores = Store.objects.filter(tags__icontains=most_tags)
                    count = len(stores)
                    ran_in_store = random.randint(0, count-1)
                    random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store])[:4], key=lambda x: random.random())
                    for i in random_menues:
                        actions.append(i)
            

            # if len(all_ordered) >=1 and len(all_ordered) <=2:
            #     last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:len(all_ordered)]
            # elif len(all_ordered) >=3:
            #     last_ordered = Order.objects.filter(user=request.user).order_by('-id')[:3]
            # print("last_ordered",last_ordered)
            # o_dict = {}
            # order_list = []
            # for i in last_ordered:

            #     for menu_id,amount in zip(i.menu,i.amount):
                 
            #         try:
            #             int(menu_id)
            #             m = Menu.objects.get(id=menu_id)
            #             if m.store.id != 24:
            #                 if m.store.id ==25:
            #                     if m.id !=504: #not set salad
            #                         if m in o_dict:
            #                             v = o_dict[m] 
            #                             new_val = int(v)+1
            #                             o_dict[m] = new_val
            #                         else:
            #                             # first time add 
            #                             o_dict[m] = int(amount)
            #                         # add_list.append(i.value)
            #                 else:
            #                     # add_list.append(i.value)
            #                     if m in o_dict:
            #                         v = o_dict[m] 
            #                         new_val = int(v)+1
            #                         o_dict[m] = new_val
            #                     else:
            #                         # first time add 
            #                         o_dict[m] = int(amount)
                    
            #         except Exception as e:
            #             pass

            # print("o_dict o_dict",o_dict)  
            # dict_store_tags ={}
            # for o in o_dict:
            #     # dic = {'name':'', 'count' : 0}
            #     tag, counter = check_tag(o)
            #     print("store_name",tag)
            #     print("counter",counter)   

            #     if counter > 0:
            #         if tag in dict_store_tags:
            #             v = dict_store_tags[tag] 
            #             new_val = int(v)+counter
            #             dict_store_tags[tag] = new_val
            #         else:
            #             dict_store_tags[tag] = counter

            # print("dict_store_tags",dict_store_tags)
            # # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
            # sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
            # print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
            # # print("most_tags",most_tags)
            # if len(sorted_dict_store_tags) >=2:  
            #     most_tags = sorted_dict_store_tags[:2]
            #     for m in most_tags:
            #         stores = Store.objects.filter(tags__icontains=m)
            #         count = len(stores)
            #         ran_in_store = random.randint(0, count-1)
            #         random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:2], key=lambda x: random.random())
           
            #         for i in random_menues:
            #             actions.append(i)
            # elif len(sorted_dict_store_tags)==1:
            #     most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
            #     stores = Store.objects.filter(tags__icontains=most_tags)
            #     print("m",most_tags)
            #     print("stores",stores)
            #     count = len(stores)
            #     print("count",count)
            #     ran_in_store = random.randint(0, count-1)
            #     print("random_meran_in_storenues",ran_in_store)
            #     print("stores[ran_in_store]",stores[ran_in_store])
            #     random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:4], key=lambda x: random.random())
            #     print("random_menues",random_menues)
            #     for i in random_menues:
            #         actions.append(i)


    elif action ==2:
        # dish & dessert
        if in_cart_list:
            print("in_cart_list")
            counter = 0
            category_dict = {"ของหวาน":0,"ของทานเล่น":0,"เครื่องดื่ม":0}
            for menu in in_cart_list:
                if "โรตี"  in menu.name or "ขนมปัง" in menu.name:
                    if "ของหวาน" in category_dict:
                        v = category_dict["ของหวาน"] 
                        new_val = int(v)+1
                        category_dict["ของหวาน"] = new_val
                    else:
                        category_dict["ของหวาน"]  = 1

                elif "ลูกชิ้น" in menu.name or "ไส้กรอก" in menu.name or "เฟรนซ์ฟราย" in menu.name or "มันบด" in menu.name or "มันอบ" in menu.name: 
                    if "ของทานเล่น" in category_dict:
                        v = category_dict["ของทานเล่น"] 
                        new_val = int(v)+1
                        category_dict["ของทานเล่น"] = new_val
                    else:
                        category_dict["ของทานเล่น"]  = 1


                elif "Soda" in menu.name or "ปั่น" in menu.name or "นมสด" in menu.name or "น้ำเต้าหู้" in menu.name or "แก้ว" in menu.name: 
                    if "เครื่องดื่ม" in category_dict:
                        v = category_dict["เครื่องดื่ม"] 
                        new_val = int(v)+1
                        category_dict["เครื่องดื่ม"] = new_val
                    else:
                        category_dict["เครื่องดื่ม"]  = 1      

                else:
                    store=Store.objects.get(id=menu.store.id)
                    if store.category in category_dict:
                        v = category_dict[store.category] 
                        new_val = int(v)+1
                        category_dict[store.category] = new_val
                    else:
                        category_dict[store.category]  = 1

            print("category_dict",category_dict)
            max_cate = max(category_dict.items(), key=operator.itemgetter(1))[0]
            print("max_cate",max_cate)
            if max_cate == "อาหารไทย":
                # if "เครื่องดื่ม" not in category_dict:
                if category_dict["เครื่องดื่ม"] < category_dict["ของหวาน"] and category_dict["เครื่องดื่ม"] < category_dict["ของทานเล่น"]:
                    # have some drink
                
                    print("not drink")
                    keys = ['ปั่น',"แก้ว","นมสด","น่ำเต้าหู้","Soda"]
                    drink_list = []
                    # query = functools.reduce(operator.and_, (Q(name__contains = item) for item in ['ปั่น',]))
                    # result = Menu.objects.filter(query)
                    # drink = Menu.objects.annotate(search=SearchVector( 'name')).filter(name__in=["ปั่น",'แก้ว'])
                    # drink = Menu.objects.filter(Q(name__iendswith='ปั่น') | Q(name__icontains='แก้ว'))
                    # print("drink",drink)
                    for k in keys:
                        drink = Menu.objects.filter(name__contains=k)
                        if drink:
                            for d in drink:
                                if d not in in_cart_list:
                                    drink_list.append(d)
                
                    drink2 = Menu.objects.filter(store__id=15)# pangyen
                    for d in drink2:
                        if d not in in_cart_list:
                            drink_list.append(d)
                    
                    # add drink
                    count = len(drink_list)
                    temp = -1
                    for i in range(2):
                        print("i")
                        ran_drink_list = random.randint(0, count-1)
                        while temp == ran_drink_list:
                            ran_drink_list = random.randint(0, count-1)

                        actions.append(drink_list[ran_drink_list])
                        temp = ran_drink_list

                    if category_dict["ของหวาน"] == category_dict["ของทานเล่น"]:
                        count = len(drink_list)
                        # temp = -1
                        for i in range(2):
                            print("i")
                            ran_drink_list = random.randint(0, count-1)
                            temp = drink_list[ran_drink_list]
                            while temp in in_cart_list or temp in actions:
                                ran_drink_list = random.randint(0, count-1)
                                temp = drink_list[ran_drink_list]
                            actions.append(temp)
                            # temp = ran_drink_list
                        print("actions",actions)


                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        dessert_list = []
                        keys = ['โรตี',"ขนมปัง",]
                        for k in keys:
                            dessert = Menu.objects.filter(name__contains=k)
                            if dessert:
                                for d in dessert:
                                    if d not in in_cart_list:
                                        dessert_list.append(d)
                        dessert2 = Menu.objects.filter(store__id=14)
                        for d in dessert2:
                            if d not in in_cart_list:
                                dessert_list.append(d)

                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        snack_list = []
                        snack = Menu.objects.filter(store__id=17) # somjai lookchin
                        # keys = ['โรตี',"ขนมปัง",]
                        for s in snack:
                            if s not in in_cart_list:
                                snack_list.append(s)
                        frenchfries = Menu.objects.get(id=156)
                        nuggets = Menu.objects.get(id=155)
                        snack_list.append(frenchfries)
                        snack_list.append(nuggets)
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list


                    print("drink")

                    # a = sorted(drink_list, key=lambda x: random.random())
                    # print("a",a[:4])
                    # dessert_store = Store.objects.filter(tags= )
                elif category_dict["เครื่องดื่ม"] >= category_dict["ของหวาน"] or category_dict["เครื่องดื่ม"] >= category_dict["ของทานเล่น"]:
                    # have some drink
                    print("เครื่องดื่ม > ขนม")
                    dessert_list = []
                    keys = ['โรตี',"ขนมปัง",]
                    for k in keys:
                        dessert = Menu.objects.filter(name__contains=k)
                        if dessert:
                            for d in dessert:
                                if d not in in_cart_list:
                                    dessert_list.append(d)
                    keys = ["น้ำเปล่า","แก้ว","ปั่น"]
                    # temp = []
                  
                    dessert2 = Menu.objects.filter(store__id=14)
                        # .exclude(name__contains=k)
                        # temp.append(dessert2)
                    for d in dessert2:
                        if d not in in_cart_list:
                            if "น้ำเปล่า" not in d.name and "แก้ว" not in d.name and "ปั่น" not in d.name:
                                dessert_list.append(d)

                    snack_list = []
                    snack = Menu.objects.filter(store__id=17) # somjai lookchin
                    for s in snack:
                        if s not in in_cart_list:
                            snack_list.append(s)
                    frenchfries = Menu.objects.get(id=156)
                    nuggets = Menu.objects.get(id=155)
                    snack_list.append(frenchfries)
                    snack_list.append(nuggets)

                    if category_dict["ของหวาน"] ==category_dict["ของทานเล่น"]:

                    # if "ของหวาน" not in category and "ของทานเล่น" in category_dict:
                       
                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list

                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        print("ของหวาน < ทานเล่น")
                        # add dessert 
                        count = len(dessert_list)
                        for i in range(3):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            temp = dessert_list[ran_dessert_list]
                            while temp in in_cart_list or temp in actions:
                                ran_dessert_list = random.randint(0, count-1)
                                temp = dessert_list[ran_dessert_list]
                            actions.append(temp)

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        ran_snack_list = random.randint(0, count-1)
                        actions.append(snack_list[ran_snack_list])

                       
                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        
                        # add dessert 
                        count = len(dessert_list)
                        ran_dessert_list = random.randint(0, count-1)
                        actions.append(dessert_list[ran_dessert_list])
       
                        # add snack 
                        count = len(snack_list)
                        for i in range(3):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            temp = snack_list[ran_snack_list]
                            while temp in in_cart_list or temp in actions:
                                ran_snack_list = random.randint(0, count-1)
                                temp = snack_list[ran_snack_list]
                            actions.append(temp)
            else:
                keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
                dish_list = []
                for k in keys:
                    dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
                    for d in dish:
                        if d not in in_cart_list:
                            dish_list.append(d)
                count = len(dish_list)
                for i in range(4):
                    print("i")
                    ran_dish_list = random.randint(0, count-1)
                    temp = dish_list[ran_dish_list]
                    while temp in in_cart_list or temp in actions:
                        ran_dish_list = random.randint(0, count-1)
                        temp = dish_list[ran_dish_list]
                    actions.append(temp)
                # drink & dessert & snack is most
                # dish_store = Store.objects.filter(category="อาหารไทย")
                


            print("actions",actions)
            for i in actions:
                print("store", i.store)
                    

        else: # not have item in cart
            keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
            dish_list = []
            for k in keys:
                dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
                for d in dish:
                    dish_list.append(d)
            count = len(dish_list)
            for i in range(2):
                print("i")
                ran_dish_list = random.randint(0, count-1)
                temp = dish_list[ran_dish_list]
                while temp in actions:
                    ran_dish_list = random.randint(0, count-1)
                    temp = dish_list[ran_dish_list]
                actions.append(temp)

                dessert_list = []
                keys = ['โรตี',"ขนมปัง",]
                for k in keys:
                    dessert = Menu.objects.filter(name__contains=k)
                    if dessert:
                        for d in dessert:
                            dessert_list.append(d)
                dessert2 = Menu.objects.filter(store__id=14)
                for d in dessert2:
                    dessert_list.append(d)

                
            # add dessert 
            count = len(dessert_list)
            temp = -1
            for i in range(2):
                print("i")
                ran_dessert_list = random.randint(0, count-1)
                while temp == ran_dessert_list:
                    ran_dessert_list = random.randint(0, count-1)

                actions.append(dessert_list[ran_dessert_list])
                temp = ran_dessert_list


        # next_state = action
        # print("next_state",next_state)

    num_actions = action

    return actions,num_actions,next_state
    
def recommendation_actions_whole_system(request,state):
    gamma = 0.8

    if state == 2 or state == 5 or state == 8:
        next_state = state # isGoal == True      
    else:
        next_state = state +1
      
    q_table = QTableGlobal.objects.get(name="global")

    R = np.array(q_table.R_array)
   
    current_state_row = R[state,]

    Q,R = getGlobalTable(request)
    # av_act = np.where(current_state_row >= 0)[0]
    # action = int(np.random.choice(av_act,size=1))

    actions = np.where(Q[state]== np.max(Q[state]))[0]

    if actions.shape[0] >1:
        action = int(np.random.choice(actions,size=1))
    else:
        action = int(actions)

    in_cart_list = check_item_in_cart(request)
    actions=[]
    
    print("Q",Q)
    print("R",R)  
    print("actions",action)          
        # if item_in_cart:
        #     print("item_in_cartitem_in_cartitem_in_cartitem_in_cart")
        # else:
        #     print("item_in_cart",item_in_cart)
    action = 1
    if action == 0:
        # Top-N
     
        fiveDaysAgo = datetime.today() - timedelta(days=25)
        allOrdered = Order.objects.filter(created_at__gte=fiveDaysAgo)

        # print("allOrdered",allOrdered)
        allo_dict = {}
        allorder_list = []
        for i in allOrdered:
            print("i",i.menu)

            for menu_id,amount in zip(i.menu,i.amount):
                try:
                    int(menu_id)
                    m = Menu.objects.get(id=menu_id)
                    if m.store.id != 24:
                        if m.store.id ==25:
                            if m.id !=504: #not set salad
                                if m in allo_dict:
                                    v = allo_dict[m] 
                                    new_val = int(v)+1
                                    allo_dict[m] = new_val
                                else:
                                    # first time add 
                                    allo_dict[m] = int(amount)
                        else:
                            # add_list.append(i.value)
                            if m in allo_dict:
                                v = allo_dict[m] 
                                new_val = int(v)+1
                                allo_dict[m] = new_val
                            else:
                                # first time add 
                                allo_dict[m] = int(amount)
                
                except Exception as e:
                    # if it is a set of salad
                    pass
                  
        print("allo_dict",allo_dict)

        mostOrdered = max(allo_dict.items(), key=operator.itemgetter(1))[0]
        sorted_dict = sorted(allo_dict, key=allo_dict.get, reverse=True)
        print("mostOrdered",mostOrdered)
        print("sorted_dict",sorted_dict[:4])
        for a in sorted_dict[:4]:
            actions.append(a)
            

            
        
        
        # return state,action,actions  
    elif action ==1:
        # same things
        if in_cart_list:
         
            dict_store_tags ={}
            for i in in_cart_list:
                print("i",i)
                # dic = {'name':'', 'count' : 0}
                tag, counter = check_tag(i)
                print("store_name",tag)
                print("counter",counter)   

                if counter > 0:
                    if tag in dict_store_tags:
                        v = dict_store_tags[tag] 
                        new_val = int(v)+counter
                        dict_store_tags[tag] = new_val
                    else:
                        dict_store_tags[tag] = counter

            print("dict_store_tags",dict_store_tags)
            # most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
            sorted_dict_store_tags = sorted(dict_store_tags, key=dict_store_tags.get, reverse=True)
            print("sorted_dict_store_tags",sorted_dict_store_tags[:2])
            # print("most_tags",most_tags)
            if len(sorted_dict_store_tags) >=2:  
                most_tags = sorted_dict_store_tags[:2]
                print("most_tags",most_tags)
                for m in most_tags:
                    stores = Store.objects.filter(tags__icontains=m)
                    count = len(stores)
                    print("conuttttt",count)
                    ran_in_store = random.randint(0, count-1)
                    random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:2], key=lambda x: random.random())
           
                    for i in random_menues:
                        print("i",i)
                        actions.append(i)

            elif len(sorted_dict_store_tags)==1:
                print("elfiiiii")
                most_tags = max(dict_store_tags.items(), key=operator.itemgetter(1))[0]
                stores = Store.objects.filter(tags__icontains=most_tags)
                count = len(stores)
                ran_in_store = random.randint(0, count-1)
                random_menues = sorted(Menu.objects.filter(store=stores[ran_in_store]).exclude(name__in=in_cart_list)[:4], key=lambda x: random.random())
                for i in random_menues:
                    actions.append(i)

        else:
            # not have item in basket
            fiveDaysAgo = datetime.today() - timedelta(days=25)
            allOrdered = Order.objects.filter(created_at__gte=fiveDaysAgo)

            # print("allOrdered",allOrdered)
            allo_dict = {}
            allorder_list = []
            for i in allOrdered:
                print("i",i.menu)

                for menu_id,amount in zip(i.menu,i.amount):
                    try:
                        int(menu_id)
                        m = Menu.objects.get(id=menu_id)
                        if m.store.id != 24:
                            if m.store.id ==25:
                                if m.id !=504: #not set salad
                                    if m in allo_dict:
                                        v = allo_dict[m] 
                                        new_val = int(v)+1
                                        allo_dict[m] = new_val
                                    else:
                                        # first time add 
                                        allo_dict[m] = int(amount)
                            else:
                                # add_list.append(i.value)
                                if m in allo_dict:
                                    v = allo_dict[m] 
                                    new_val = int(v)+1
                                    allo_dict[m] = new_val
                                else:
                                    # first time add 
                                    allo_dict[m] = int(amount)
                    
                    except Exception as e:
                        # if it is a set of salad
                        pass
                      
            print("allo_dict",allo_dict)

            mostOrdered = max(allo_dict.items(), key=operator.itemgetter(1))[0]
            sorted_dict = sorted(allo_dict, key=allo_dict.get, reverse=True)
            print("mostOrdered",mostOrdered)
            print("sorted_dict",sorted_dict[:4])
            for a in sorted_dict[:4]:
                actions.append(a)
    elif action ==2:
        # dish & dessert
        if in_cart_list:
            print("in_cart_list")
            counter = 0
            category_dict = {"ของหวาน":0,"ของทานเล่น":0,"เครื่องดื่ม":0}
            for menu in in_cart_list:
                if "โรตี"  in menu.name or "ขนมปัง" in menu.name:
                    if "ของหวาน" in category_dict:
                        v = category_dict["ของหวาน"] 
                        new_val = int(v)+1
                        category_dict["ของหวาน"] = new_val
                    else:
                        category_dict["ของหวาน"]  = 1

                elif "ลูกชิ้น" in menu.name or "ไส้กรอก" in menu.name or "เฟรนซ์ฟราย" in menu.name or "มันบด" in menu.name or "มันอบ" in menu.name: 
                    if "ของทานเล่น" in category_dict:
                        v = category_dict["ของทานเล่น"] 
                        new_val = int(v)+1
                        category_dict["ของทานเล่น"] = new_val
                    else:
                        category_dict["ของทานเล่น"]  = 1


                elif "Soda" in menu.name or "ปั่น" in menu.name or "นมสด" in menu.name or "น้ำเต้าหู้" in menu.name or "แก้ว" in menu.name: 
                    if "เครื่องดื่ม" in category_dict:
                        v = category_dict["เครื่องดื่ม"] 
                        new_val = int(v)+1
                        category_dict["เครื่องดื่ม"] = new_val
                    else:
                        category_dict["เครื่องดื่ม"]  = 1      

                else:
                    store=Store.objects.get(id=menu.store.id)
                    if store.category in category_dict:
                        v = category_dict[store.category] 
                        new_val = int(v)+1
                        category_dict[store.category] = new_val
                    else:
                        category_dict[store.category]  = 1

            print("category_dict",category_dict)
            max_cate = max(category_dict.items(), key=operator.itemgetter(1))[0]
            print("max_cate",max_cate)
            if max_cate == "อาหารไทย":
                # if "เครื่องดื่ม" not in category_dict:
                if category_dict["เครื่องดื่ม"] < category_dict["ของหวาน"] and category_dict["เครื่องดื่ม"] < category_dict["ของทานเล่น"]:
                    # have some drink
                
                    print("not drink")
                    keys = ['ปั่น',"แก้ว","นมสด","น่ำเต้าหู้","Soda"]
                    drink_list = []
                    # query = functools.reduce(operator.and_, (Q(name__contains = item) for item in ['ปั่น',]))
                    # result = Menu.objects.filter(query)
                    # drink = Menu.objects.annotate(search=SearchVector( 'name')).filter(name__in=["ปั่น",'แก้ว'])
                    # drink = Menu.objects.filter(Q(name__iendswith='ปั่น') | Q(name__icontains='แก้ว'))
                    # print("drink",drink)
                    for k in keys:
                        drink = Menu.objects.filter(name__contains=k)
                        if drink:
                            for d in drink:
                                if d not in in_cart_list:
                                    drink_list.append(d)
                
                    drink2 = Menu.objects.filter(store__id=15)# pangyen
                    for d in drink2:
                        if d not in in_cart_list:
                            drink_list.append(d)
                    
                    # add drink
                    count = len(drink_list)
                    temp = -1
                    for i in range(2):
                        print("i")
                        ran_drink_list = random.randint(0, count-1)
                        while temp == ran_drink_list:
                            ran_drink_list = random.randint(0, count-1)

                        actions.append(drink_list[ran_drink_list])
                        temp = ran_drink_list

                    if category_dict["ของหวาน"] == category_dict["ของทานเล่น"]:
                        count = len(drink_list)
                        # temp = -1
                        for i in range(2):
                            print("i")
                            ran_drink_list = random.randint(0, count-1)
                            temp = drink_list[ran_drink_list]
                            while temp in in_cart_list or temp in actions:
                                ran_drink_list = random.randint(0, count-1)
                                temp = drink_list[ran_drink_list]
                            actions.append(temp)
                            # temp = ran_drink_list
                        print("actions",actions)


                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        dessert_list = []
                        keys = ['โรตี',"ขนมปัง",]
                        for k in keys:
                            dessert = Menu.objects.filter(name__contains=k)
                            if dessert:
                                for d in dessert:
                                    if d not in in_cart_list:
                                        dessert_list.append(d)
                        dessert2 = Menu.objects.filter(store__id=14)
                        for d in dessert2:
                            if d not in in_cart_list:
                                dessert_list.append(d)

                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        snack_list = []
                        snack = Menu.objects.filter(store__id=17) # somjai lookchin
                        # keys = ['โรตี',"ขนมปัง",]
                        for s in snack:
                            if s not in in_cart_list:
                                snack_list.append(s)
                        frenchfries = Menu.objects.get(id=156)
                        nuggets = Menu.objects.get(id=155)
                        snack_list.append(frenchfries)
                        snack_list.append(nuggets)
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list


                    print("drink")

                    # a = sorted(drink_list, key=lambda x: random.random())
                    # print("a",a[:4])
                    # dessert_store = Store.objects.filter(tags= )
                elif category_dict["เครื่องดื่ม"] >= category_dict["ของหวาน"] or category_dict["เครื่องดื่ม"] >= category_dict["ของทานเล่น"]:
                    # have some drink
                    print("เครื่องดื่ม > ขนม")
                    dessert_list = []
                    keys = ['โรตี',"ขนมปัง",]
                    for k in keys:
                        dessert = Menu.objects.filter(name__contains=k)
                        if dessert:
                            for d in dessert:
                                if d not in in_cart_list:
                                    dessert_list.append(d)
                    keys = ["น้ำเปล่า","แก้ว","ปั่น"]
                    # temp = []
                  
                    dessert2 = Menu.objects.filter(store__id=14)
                        # .exclude(name__contains=k)
                        # temp.append(dessert2)
                    for d in dessert2:
                        if d not in in_cart_list:
                            if "น้ำเปล่า" not in d.name and "แก้ว" not in d.name and "ปั่น" not in d.name:
                                dessert_list.append(d)

                    snack_list = []
                    snack = Menu.objects.filter(store__id=17) # somjai lookchin
                    for s in snack:
                        if s not in in_cart_list:
                            snack_list.append(s)
                    frenchfries = Menu.objects.get(id=156)
                    nuggets = Menu.objects.get(id=155)
                    snack_list.append(frenchfries)
                    snack_list.append(nuggets)

                    if category_dict["ของหวาน"] ==category_dict["ของทานเล่น"]:

                    # if "ของหวาน" not in category and "ของทานเล่น" in category_dict:
                       
                        
                        # add dessert 
                        count = len(dessert_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            while temp == ran_dessert_list:
                                ran_dessert_list = random.randint(0, count-1)

                            actions.append(dessert_list[ran_dessert_list])
                            temp = ran_dessert_list

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        temp = -1
                        for i in range(2):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            while temp == ran_snack_list:
                                ran_snack_list = random.randint(0, count-1)

                            actions.append(snack_list[ran_snack_list])
                            temp = ran_snack_list

                    elif category_dict["ของหวาน"] < category_dict["ของทานเล่น"]:
                        print("ของหวาน < ทานเล่น")
                        # add dessert 
                        count = len(dessert_list)
                        for i in range(3):
                            print("i")
                            ran_dessert_list = random.randint(0, count-1)
                            temp = dessert_list[ran_dessert_list]
                            while temp in in_cart_list or temp in actions:
                                ran_dessert_list = random.randint(0, count-1)
                                temp = dessert_list[ran_dessert_list]
                            actions.append(temp)

                    # elif "ของทานเล่น" not in category and "ของหวาน" in category_dict:
                        
                        # add snack 
                        count = len(snack_list)
                        ran_snack_list = random.randint(0, count-1)
                        actions.append(snack_list[ran_snack_list])

                       
                    elif category_dict["ของหวาน"] > category_dict["ของทานเล่น"]:
                        
                        # add dessert 
                        count = len(dessert_list)
                        ran_dessert_list = random.randint(0, count-1)
                        actions.append(dessert_list[ran_dessert_list])
       
                        # add snack 
                        count = len(snack_list)
                        for i in range(3):
                            print("i")
                            ran_snack_list = random.randint(0, count-1)
                            temp = snack_list[ran_snack_list]
                            while temp in in_cart_list or temp in actions:
                                ran_snack_list = random.randint(0, count-1)
                                temp = snack_list[ran_snack_list]
                            actions.append(temp)
            else:
                keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
                dish_list = []
                for k in keys:
                    dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
                    for d in dish:
                        if d not in in_cart_list:
                            dish_list.append(d)
                count = len(dish_list)
                for i in range(4):
                    print("i")
                    ran_dish_list = random.randint(0, count-1)
                    temp = dish_list[ran_dish_list]
                    while temp in in_cart_list or temp in actions:
                        ran_dish_list = random.randint(0, count-1)
                        temp = dish_list[ran_dish_list]
                    actions.append(temp)
                # drink & dessert & snack is most
                # dish_store = Store.objects.filter(category="อาหารไทย")
                


            print("actions",actions)
            for i in actions:
                print("store", i.store)
                    

        else: # not have item in cart
            keys = ["ข้าว","สุกี้","ไก่","ผัด","มักกะโรนี","สปาเก็ตตี้"]
            dish_list = []
            for k in keys:
                dish = Menu.objects.filter(name__icontains=k).exclude(name__in=dish_list)
                for d in dish:
                    dish_list.append(d)
            count = len(dish_list)
            for i in range(2):
                print("i")
                ran_dish_list = random.randint(0, count-1)
                temp = dish_list[ran_dish_list]
                while temp in actions:
                    ran_dish_list = random.randint(0, count-1)
                    temp = dish_list[ran_dish_list]
                actions.append(temp)

                dessert_list = []
                keys = ['โรตี',"ขนมปัง",]
                for k in keys:
                    dessert = Menu.objects.filter(name__contains=k)
                    if dessert:
                        for d in dessert:
                            dessert_list.append(d)
                dessert2 = Menu.objects.filter(store__id=14)
                for d in dessert2:
                    dessert_list.append(d)

                
            # add dessert 
            count = len(dessert_list)
            temp = -1
            for i in range(2):
                print("i")
                ran_dessert_list = random.randint(0, count-1)
                while temp == ran_dessert_list:
                    ran_dessert_list = random.randint(0, count-1)

                actions.append(dessert_list[ran_dessert_list])
                temp = ran_dessert_list


        # next_state = action
        # print("next_state",next_state)

    num_actions = action

    return actions,num_actions,next_state
  

def q_learning(request):
    gamma = 0.8
    state = 1
    print(request.user)
    state,num_actions,actions = createActions(request,state)
    return render(request, 'q_learning.html',{'actions':actions,
        'state':state,
        'num_actions':num_actions})

    # print( Menu.objects.all())
    # all_menues = list(Menu.objects.all())
    # random_menues = sorted(Menu.objects.all(), key=lambda x: random.random())
    # print(random_menues[:4])
    # # info = Informations.objects.get(user=request.user)
    # # print(info.japanese)
    # # c_arr = QTable.objects.create(user=request.user)



    # b = QTable.objects.get(user=request.user)
    # # Q_learning 
    # actions = np.arange(3) # 0 1 2 3

    # q_table = QTable.objects.get(user=request.user)
    # R = np.array(q_table.R_array)
    # Q = np.array(q_table.Q_array)
    # valid_moves = R[state] >= 0
    # print("valid_moves",valid_moves)
    # valid_actions = actions[valid_moves == True]
    # print("valid_actions",valid_actions)
    # action = int(np.random.choice(valid_actions,size=1))

    # next_state = action
    # print("next_state",next_state)

    # # if this menu click 
    # Q[state,action] = R[state,action] + gamma * max(Q[next_state,:])
    # print("q[state,action]",Q[state,action])



    # Q = np.array(b.Q_array)
    # # Q[1,3]=0.
    # # Q[2,3]=0.
    # # print("Q",Q)
    
    # a = QTable.objects.filter(user=request.user).update(Q_array=Q.tolist())
    # # print("Q",Q.shape)
    
    # arr = QTable.objects.get(user=request.user)
    # # print("arr",np.array(arr.Q_array))
    # # print("r ",arr.r_array)
    # most_add_to_cart , most_ordered= createActions(request,state)
    
    
    # order = (12,13)
    # for i in order:
    #   m = Menues.objects.get(id=i)
    #   store_cate_from_order.append(m.store.category)
    #   if m.store.category =="อาหารไทย":
    #       if info.thai:
    #           score+=1
                


    # print("store_cate_from_order",store_cate_from_order)
    # menu1 = Menues.objects.get(id=12)
    # menu2 = Menues.objects.get(id=13)

    
    # store_cate_thai = []
    # if info.thai:
    #   store_cate_thai = Store.objects.filter(category="อาหารไทย")
    # print(store_cate_thai)    

    # all_menues = Menues.object.all()[4:]

   
    # return render(request, 'q_learning.html',{'most_ordered':most_ordered,'most_add_to_cart':most_add_to_cart})
def check_item_in_cart(request):
    if request.session.get('mycart',False):
        
        my_item_in_cart = request.session.get('mycart',[])
        temp_del = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                print("i0",i[0])
                menu = Menu.objects.get(id=i[0])
                print("store id",menu.store.id)
                print("type store id",type(menu.store.id))
                # store = Store.objects.get(store=menu.store)
                if menu.store.id != 25:
                    temp_del.append(i)
            else:
                try:
                    menu = Menu.objects.get(id=i)
                    tohrung = Tohrung2.objects.get(store=menu.store) 
                    
                except Tohrung2.DoesNotExist as e:

                    menu = Menu.objects.get(id=i)
                    print("Tohrung2.DoesNotExist",menu.store)
                    if menu.store.id != 25:
                        temp_del.append(i)
                
                    
        a = [x for x in my_item_in_cart if x not in temp_del]
        del request.session['mycart']
        request.session['mycart'] = a  
        

        item_in_cart = len(request.session.get('mycart'))
        # my_item_in_cart = request.session.get('mycart',[])

        temp_cart = []

        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        in_cart_list = []
        my_dict = {i:temp_cart.count(i) for i in temp_cart}
        print("my_dict",my_dict)
        
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[]}
            temp['amount'] = amount
            if isinstance(m_id, tuple):
                # set steak or set salad
                # pass
                # temp_set = {"menu_name":"","ingredient":[],"sauce":"","price":0.0,}
                
                menu = Menu.objects.get(id=m_id[0])
                in_cart_list.append(menu)


                # temp_set["menu_name"] = menu.name
                # index = 0
                # for i in m_id:
                #     if index >=2:
                #         temp_set["ingredient"].append(i)
                #     index+=1

                # temp_price = int(menu.price)+ int(m_id[1])
                # set_price = temp_price*int(amount)
                # temp['price'] = set_price
                # temp['set'] = temp_set
                # output.append(temp)
                

            else:
                menu = Menu.objects.get(id=m_id)
                in_cart_list.append(menu)
                print("menu in cart",menu)
        return in_cart_list
                # print
                # temp['menu_id'] = m_id
                # temp['name'] = menu.name
                # temp['price'] = int(menu.price)*int(amount)
                # output.append(temp)
    
    else:
        print("no len")
        item_in_cart = None
        return None



def createActions(request,state):

    if request.session.get('mycart',False):
        
        my_item_in_cart = request.session.get('mycart',[])
        temp_del = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                print("i0",i[0])
                menu = Menu.objects.get(id=i[0])
                print("store id",menu.store.id)
                print("type store id",type(menu.store.id))
                # store = Store.objects.get(store=menu.store)
                if menu.store.id != 25:
                    temp_del.append(i)
            else:
                try:
                    menu = Menu.objects.get(id=i)
                    tohrung = Tohrung2.objects.get(store=menu.store) 
                    
                except Tohrung2.DoesNotExist as e:

                    menu = Menu.objects.get(id=i)
                    print("Tohrung2.DoesNotExist",menu.store)
                    if menu.store.id != 25:
                        temp_del.append(i)
                
                    
        a = [x for x in my_item_in_cart if x not in temp_del]
        del request.session['mycart']
        request.session['mycart'] = a  
        

        item_in_cart = len(request.session.get('mycart'))
        # my_item_in_cart = request.session.get('mycart',[])

        temp_cart = []

        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        in_cart_list = []
        my_dict = {i:temp_cart.count(i) for i in temp_cart}
        print("my_dict",my_dict)
        
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[]}
            temp['amount'] = amount
            if isinstance(m_id, tuple):
                # set steak or set salad
                # pass
                # temp_set = {"menu_name":"","ingredient":[],"sauce":"","price":0.0,}
                
                menu = Menu.objects.get(id=m_id[0])
                in_cart_list.append(menu)


                # temp_set["menu_name"] = menu.name
                # index = 0
                # for i in m_id:
                #     if index >=2:
                #         temp_set["ingredient"].append(i)
                #     index+=1

                # temp_price = int(menu.price)+ int(m_id[1])
                # set_price = temp_price*int(amount)
                # temp['price'] = set_price
                # temp['set'] = temp_set
                # output.append(temp)
                

            else:
                menu = Menu.objects.get(id=m_id)
                in_cart_list.append(menu)
                print("menu in cart",menu)
                # print
                # temp['menu_id'] = m_id
                # temp['name'] = menu.name
                # temp['price'] = int(menu.price)*int(amount)
                # output.append(temp)
    
    else:
        print("no len")
        item_in_cart = None
    gamma=0.8
    epsilon = 0.0
    random_probability = np.random.rand()
    actions = []
    valid_actions = np.arange(3)
    q_table = QTable.objects.get(name="global")
  
    Q = np.array(q_table.Q_array)

    #   q_table_local =     QTableLocal.objects.update_or_create(user=request.user,
    #             defaults={'R_array':[
    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],
        
    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],

    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],
    # ],'Q_array':[
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],
        
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],

    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    # ]})
    # R = np.array(q_table.R_array) 
    # qupdate = QTable.objects.filter(name="global").update(R_array =[
    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],
        
    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],

    #     [0., 0, 100.],
    #     [100., 0., 0.],
    #     [0.,100., 0.],
    # ],Q_array = [
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],
        
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],
        
    #     [0., 0., 0.],
    #     [0., 0., 0.],
    #     [0., 0., 0.],
        
    # ] ) 
    print("Q",Q.shape)
    # print("Q ta",Q)
    # print("q_table.Q_array",q_table.Q_array)

    
    # current_state = np.random.randint(0, int(Q.shape[0]))
    # print("current_state",current_state)
    # available_act = available_actions(request,current_state)
    # print("available_act",available_act)
    # action = sample_next_action(available_act)
    # score = update(current_state,action,gamma)



    fai = User.objects.get(username="PanatchakornLeeprasert")
    # fai = User.objects.get(username="TuanrusdeeChanurong")
    if state == 1:
        # action = int(np.random.choice(valid_actions,size=1))
        action = 0
        if action == 0: # Top N 
            all_ordered = Order.objects.filter(user=fai)
            if len(all_ordered) == 0:
                print("no order")
            else:
                pass
                
                # bc not have order enough to make action


                    # break
            # most_click = User_session.objects.filter(action=enter_store)
            # print
            
            logs = User_session.objects.filter(user=fai,action="เพิ่มเข้าตะกร้า")
            # print("logs",logs)
            print("len(all_ordered)",len(all_ordered))
            # print("len(logs)",len(logs))
            if len(all_ordered) == 0 and len(logs) == 0:
                pass
            elif len(all_ordered) == 0 and len(logs) >= 1:
     
                for i in range(4):
                    count = len(in_cart_list)
                    ran_num = random.randint(0, count-1)
                    menu = in_cart_list[ran_num]
                    menu_list = Menu.objects.filter(store=menu.store).exclude(name=in_cart_list)
                    count = len(menu_list)
                    ran_in_store = random.randint(0, count-1)
                    actions.append(menu_list[ran_in_store])
             

                print("actionsssss",actions)

            elif len(all_ordered) >= 1 and len(logs) >= 1:
                # have ordered and have session
                o_dict = {}
                order_list = []
                for i in all_ordered:

                    for menu_id,amount in zip(i.menu,i.amount):
                     
                        try:
                            int(menu_id)
                            m = Menu.objects.get(id=menu_id)
                        
                        except Exception as e:
                            tuple_menu = literal_eval(m)
                            m = Menu.objects.get(id=tuple_menu[0])
                          
                        if m in o_dict:
                            v = o_dict[m] 
                            new_val = int(v)+1
                            o_dict[m] = new_val
                        else:
                            # first time add 
                            o_dict[m] = int(amount)

                print("o_dict ee",o_dict)      
                most_ordered = max(o_dict.items(), key=operator.itemgetter(1))[0]
                sorted_dict = sorted(o_dict, key=o_dict.get, reverse=True)
                print("most_ordered",most_ordered)
                print("sorted_dict",sorted_dict)
                print("in_cart_list",in_cart_list)
                print("in_cart_list",len(in_cart_list))

                count = 0
                for i in sorted_dict:
                    
                    # most_add_to_cart = i
                    if count == 2:
                        break
                    else:
                        print("i",i)
                        if i not in in_cart_list:
                            actions.append(i)
                            count +=1
                        else:
                            print("incart")
                print("actions",actions)
                print("else",count)
                add_list = []
                for i in logs:
                    add_list.append(i.value)
                    # print("เพิ่มเข้าตะกร้า",i.value)
                my_dict = {i:add_list.count(i) for i in add_list}
                # print("my_dict",my_dict)
                most_add_to_cart = max(my_dict.items(), key=operator.itemgetter(1))[0]
                sorted_dict = sorted(my_dict, key=my_dict.get, reverse=True)
                # print("sorted_dict",sorted_dict)
                # print("in_cart_list ",in_cart_list)
                count = 0
                more_actions = 4-len(actions)
              
                for i in sorted_dict:
                    if count == more_actions:
                        break
                    else:
                        sp = i.split(",")
                        if len(sp) > 1:
                            m = Menu.objects.get(id=sp[0],name=sp[1])
                        
                        elif len(sp) == 1:
                            menu = Menu.objects.filter(name=sp[0])
                            if len(menu) == 1:
                                m = Menu.objects.get(name=i)
                
                        if m not in in_cart_list:
                            if m not in actions:
                                count+=1
                                actions.append(m)
           
                num_loop = 4-len(actions)
                if num_loop >0:
                    for i in range(num_loop):
                        count = len(in_cart_list)
                        ran_num = random.randint(0, count-1)
                        menu = in_cart_list[ran_num]
                        menu_list = Menu.objects.filter(store=menu.store).exclude(name=in_cart_list)
                        count = len(menu_list)
                        ran_in_store = random.randint(0, count-1)
                        # if 
                        actions.append(menu_list[ran_in_store])

                print("actions aaaa",actions)
            
            return state,action,actions 

        elif action ==1:
            pass
        elif action == 2:
            pass    

        
    elif state == 0:
        pass
    elif state == 2:
        pass 



#     if random_probability > epsilon: # explore
#         pass
#     else: # Act greedy , selected based on value
                
#         logs = User_session.objects.filter(user=request.user,action="enter_store")
#         enter_store_list = []
#         for i in logs:
#             enter_store_list.append(i.value)
#             print("enter_store",i.value)
#         my_dict = {i:enter_store_list.count(i) for i in enter_store_list}
#         # print("my_dict",my_dict)
#         max_entered = max(my_dict.items(), key=operator.itemgetter(1))[0]
#         # print("co",max_entered)
#         split = max_entered.split(",")
#         print("lensp",len(split))
#         if len(split) == 2:
#             random_menues = sorted(Menu.objects.filter(store__id=split[0],store__name=split[1]), key=lambda x: random.random())

#         elif len(split) == 1:
#             random_menues = sorted(Menu.objects.filter(store__name=split[0]), key=lambda x: random.random())

#         for i in random_menues[:1]:
#             temp_actions = {"menu":i}
#             actions.append(temp_actions)



# # len(temp)

#     score = 0
#     store_cate_from_order=[]
     
#     # ordered
#     # ordered_list = []
#     all_ordered = Order.objects.filter(user=fai)
    
#     o_dict = {}
#     order_store_list = []
#     for i in all_ordered:
        
#         # m = Menues.objects.get(id=o.)
#         for menu_id,amount in zip(i.menu,i.amount):
#             temp = {"menu":None,"amount":amount}

#             # ma = {'menu':None,'amount':a,}
#             m = Menu.objects.get(id=menu_id)
#             order_store_list.append(m.store)
#             temp["menu"] = m.name
#             # print("o_dict",o_dict)    
#             if m in o_dict:
#                 print("in if")
#                 v = o_dict[m] 
#                 new_val = int(v)+1
#                 o_dict[m] = new_val
#             else:
#                 o_dict[m] = int(amount)

#     print("o_dict",o_dict)      
#     most_ordered = max(o_dict.items(), key=operator.itemgetter(1))[0]
#     print("most_ordered",most_ordered)
#     random_menues = sorted(Menu.objects.filter(store=most_ordered.store), key=lambda x: random.random())
#     # print("random_menues",random_menues)
#     for i in random_menues[:1]:
#         temp_actions = {"menu":i}
#         actions.append(temp_actions)


#     random_store = sorted(order_store_list, key=lambda x: random.random())
#     random_menues = sorted(Menu.objects.filter(store=random_store[0]), key=lambda x: random.random())
#     # for i in random_menues[:1]:
#     count = len(random_menues)
#     ran_num = random.randint(0, count-1) 
#     # print("ran_num",ran_num)
#     temp_actions = {"menu":random_menues[ran_num]}
#     print("actions before loop",actions)
#     while True:

#         # for i in actions:
#         if temp_actions in actions:
#             # a = [x for x in actions if x != temp_actions]
#             # print ("a",a)
#             # actions = a
#             ran_num = random.randint(0, count-1) 
#             temp_actions = {"menu":random_menues[ran_num]}
#             # actions.append(temp_actions)
#         else:
#             actions.append(temp_actions)
#             print("temp_actions",temp_actions)
#             break

 

        
#     print("actions",actions)
    # return most_add_to_cart,most_ordered
    # print("ordered_list",ordered_list)        # 
    # count = Menues.objects.filter(store=m.store).count()
            # print("count",count)


# def add_to_cart(request, menu_id, quantity):
#     # force quantity = 1
#     if request.method == 'POST':

#         # request.session['mycart']= menu_id
#         # del request.session['mycart']
#         menu_list = []
#         print("test",request.session.get('mycart',[]))
#         menu_list = request.session.get('mycart',[])
#         print("type",type(menu_list))
#         menu_list.append(menu_id)
#         request.session['mycart'] = menu_list


#         print("menu_id",menu_id)
#         print("quantity",quantity)
#         print("session",request.session.get('mycart'))
#     # menu = Menu.objects.get(id=menu_id)
#     # cart = Cart(request)
#     # cart.add(menu, menu.price, quantity)

#     # render(request, 'stores.html',)
#         next_page = "/store/พินิจโต้รุ่ง/"+str(quantity)
#         # return redirect('about_us')
#         return HttpResponseRedirect(next_page)

def steakholder(request):
    collect_session(request,"enter_store","24,SteakHolder")
    
    output_store = []
    main_dish_list = []
    solo_dish_list = []
    side_dish_list = []
    sauce_list = []
    store = Store.objects.get(name="SteakHolder")
    menues = Menu.objects.filter(store=store)
    print("menuuuuu")
    for menu in menues :
        temp = {'name':"",'image':None,'price':0.0,"menu_id":menu.id}
        
        temp['image'] = menu.image.url
        temp['price'] = menu.price

        if "Steak" in menu.name:
            temp['name'] = menu.name
            main_dish_list.append(temp)

        elif "Solo" in menu.name:
            temp['name'] = menu.name.replace('(Solo)', '')
            solo_dish_list.append(temp) 

        elif "Side" in menu.name:
            temp['name'] = menu.name.replace('(Side)', '')
            side_dish_list.append(temp) 

        elif "Sauce" in menu.name:
            temp['name'] = menu.name.replace('(Sauce)', '')
            sauce_list.append(temp)        

    
    reviews = Review.objects.filter(store=store)
    # getreview and love
    
    time_status = 0
    delivery = False
    is_delivery = False
    if "delivery" in store.tags :
        delivery = True

        try :
            time = DeliveryTime.objects.get(store=store)
                # print(calendar.day_name[date.today().weekday()])
            day = date.today().weekday()
            time_now = datetime.datetime.now().time()
            time_status = 0
            if day == 0 :# monday

                if time.monday :
                    time_open = time.monday_open
                    time_close = time.monday_close
                    if time_open is None and time_close is None:
                        time_status = 0

                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 1:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0
                                        
                                        
                            else:
                                if time_now <= time_close :
                                    time_status = 1
                                else:
                                    time_status = 0
                        else:
                            time_status = 0

                else :
                    time_status = 0

                is_delivery = time.monday
                    
            elif day == 1 :# tuesday
                if time.tuesday :
                    time_open = time.tuesday_open
                    time_close = time.tuesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.tuesday

            elif day == 2:  # wednesday
                if time.wednesday :
                    time_open = time.wednesday_open
                    time_close = time.wednesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 3:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                            
                            else:
                                if time_now <= time_close :
                                    time_status = 1

                                else:
                                    time_status = 0
                        else:

                            time_status = 0
                else :
                    time_status = 0
                    
                is_delivery = time.wednesday


            elif day == 3 :# thursday
                if time.thursday :
                    time_open = time.thursday_open
                    time_close = time.thursday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0

                is_delivery = time.thursday
                    
            elif day == 4:# friday
                if time.friday :
                    time_open = time.friday_open
                    time_close = time.friday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.friday
                    
            elif day == 5 :# saturday
                if time.saturday :
                    time_open = time.saturday_open
                    time_close = time.saturday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.saturday
            elif day == 6:# sunday
                    # print(time.sunday)
                if time.sunday :
                    time_open = time.sunday_open
                    time_close = time.sunday_close
                        # print(time_close)
                        # print(time_open)
                    if time_open is None and time_close is None:
                        time_status = 0
                        # print(None)
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.sunday
        except :
            pass
    
    rate = []
    profile_picture = []
    store_loved_color = None
    if request.user.is_authenticated:
        user = request.user
        store = get_object_or_404(Store, id=store.id)
        if store.likes.filter(id=user.id).exists():
            store_loved_color= True
        else:
            store_loved_color = None

    for i in reviews:
        p = Profile.objects.get(user=i.user)
        temp = { 'rating_color': 0,'rating_no_color': 0,'username':""}
        temp['username'] = p.name
        temp['rating_color'] = i.rating
        temp['rating_no_color'] = 5 - temp['rating_color']
        rate.append(temp)
        try :
            profile_picture.append(Profile.objects.get(user=i.user).picture.url)
        except:
            raise
# raise Http404

    out = zip(reviews,rate,profile_picture)

    reviewForm = ReviewForm()
    # store = Store.objects.get(id=store_id)
    # reviews = Review.objects.filter(store=store)
    output = []
    # del request.session['mycart']
    print("earn")
    if request.session.get('mycart',False):
        
        my_item_in_cart = request.session.get('mycart',[])
        temp_del_steak = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                pass
            else:
                try:
                    menu = Menu.objects.get(id=i)
                    tohrung = Tohrung2.objects.get(store=menu.store) 
                    temp_del_steak.append(i)
                except Tohrung2.DoesNotExist as e:
                    pass
                
                    
        a = [x for x in my_item_in_cart if x not in temp_del_steak]
        del request.session['mycart']
        request.session['mycart'] = a  
        # pass

        item_in_cart = len(request.session.get('mycart'))
        my_item_in_cart = request.session.get('mycart',[])

        temp_cart = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        my_dict = {i:temp_cart.count(i) for i in temp_cart}
        print("my_dict",my_dict)
        
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[]}
            temp['amount'] = amount
            if isinstance(m_id, tuple):
                temp_set = {"main":"","side":"","sauce":"","price":0.0,}
                
                # print("mid",m_id[0])
                # print("mid",m_id[1])
                # print("mid",m_id[2])
                # main = Menu.objects.get(id=m_id[0])
                # sauce = Menu.objects.get(id=m_id[2])
                # sauce_name = sauce.name.replace('(Sauce)', '')

                # if m_id[1]== '-1':
                #     side_name = "ไม่เลือก"
                    
                # else:
                #     side = Menu.objects.get(id=m_id[1])
                #     side_name = side.name.replace('(Side)', '')

                # temp = str_set_steak.replace("main",main.name)
                # temp2 = temp.replace("amount",str(amount))
                # temp3 = temp2.replace("sauce",sauce_name)

                # set_price = 0 
                # if side_name == "ไม่เลือก":
                #     temp4 = temp3.replace("+ side_dish","")
                #     set_price = int(main.price)*int(amount)
                # else:
                #     temp4 = temp3.replace("side_dish",side_name)
                #     set_price = (int(main.price)+30.0)*int(amount)   



                main = Menu.objects.get(id=m_id[0])
                sauce = Menu.objects.get(id=m_id[2])
                set_price = 0

                if m_id[1]== '-1':
                    side_name = "ไม่เลือก"
                    set_price = int(main.price)*int(amount)
                    
                else:
                    side = Menu.objects.get(id=m_id[1])
                    side_name = side.name.replace('(Side)', '')
                    set_price = (int(main.price)+30.0)*int(amount)

                temp_set["main"] = main.name
                temp_set["side"] = side_name
                temp_set["sauce"] = sauce.name.replace('(Sauce)', '')

                temp['price'] = set_price
                temp['set'] = temp_set
                output.append(temp)
                

            else:
                menu = Menu.objects.get(id=m_id)
                temp['menu_id'] = m_id
                if "Solo" in menu.name:
                    temp['name'] = menu.name.replace('(Solo)', '')
                else:
                    temp['name'] = menu.name
                
                temp['price'] = int(menu.price)*int(amount)
                output.append(temp)
                # temp_cart_list.append(m_id) # add set steak
                # main = Menu.objects.get(id=main_id)
                # side = Menu.objects.get(id=side_id)
                # sauce = Menu.objects.get(id=sauce_id)
                
                # temp = str_set_steak.replace("main",main.name)
                # temp2 = temp.replace("amount",str(amount))
                # temp3 = temp2.replace("side_dish",side.name.replace('(Side)', ''))
                # temp4 = temp3.replace("amount",sauce.name.replace('(Sauce)', ''))
                
                # str_table = temp4.replace("20",str(int(main.price)*int(amount)))
                # table.append(str_table)
                
                
            # menu = Menu.objects.get(id=m_id)
            # temp['menu_id'] = m_id
            # temp['name'] = menu.name
            # temp['amount'] = amount
            # temp['price'] = int(menu.price)*int(amount)
            # output.append(temp)
    else:
        print("no len")
        item_in_cart = None

    if request.method == 'POST':
        if "review" in request.POST:
            try:
                star = request.POST['star']
            except Exception as e:
                star = 0;
        
            
            print ("star: ",star)
            reviewForm = ReviewForm(request.POST, request.FILES)
            if reviewForm.is_valid():
                review = Review.objects.create(user = request.user,
                store = store,
                comment = reviewForm.cleaned_data['comment'],
                rating = star,)
                DisplayHome.objects.create(user=request.user,review=review)
                next_page = "steak-holder"
                print("redirect")
                # return shop_decision(requset,store.name,store.id)
                # next_page = "/store/"+store.name+"/"+str(store_id)
                return HttpResponseRedirect(next_page)

    # print((request.session.get('mycart')))
    # print(len(request.session.get('mycart')))
    # item_in_cart = len(request.session.get('mycart'))
    # 'reviews':reviews,'out':out,'store':store,'delivery':delivery,'category':cate,
    #     'store_loved_color':store_loved_color,
    return render(request, 'steakholder.html',{'store':store,
        'main_dish_list':reversed(main_dish_list),
        'solo_dish_list':reversed(solo_dish_list),
        'side_dish_list':reversed(side_dish_list),
        'sauce_list':reversed(sauce_list),

        'main_dish_list_mobile':reversed(main_dish_list),
        'solo_dish_list_mobile':reversed(solo_dish_list),
        'side_dish_list_mobile':reversed(side_dish_list),
        'sauce_list_mobile':reversed(sauce_list),

        'main_dish_list_modal':reversed(main_dish_list),
        'side_dish_list_modal':reversed(side_dish_list),
        'sauce_list_modal':reversed(sauce_list),

        'is_delivery':is_delivery,
        'time_status':time_status,
        'store_loved_color':store_loved_color,
        'reviews':reviews,
        'reviewForm':reviewForm,
        "output_in_cart":output,
        'item_in_cart':item_in_cart,
        'out_review':out,


        })
   # return render(request, 'until_dawn_canteen.html',{'store':store,
   #                "menues":reversed(menues) ,"mobile_menues":reversed(menues),'reviewForm':reviewForm,
   #                'item_in_cart':item_in_cart,"output":output    ,'store_loved_color':store_loved_color,
   #                'reviews':reviews,'out':out,'menues_list':menues_list,'time_status':time_status,
   #                'is_delivery':is_delivery})


@login_required
def change_status(request):
    
    if request.method == 'POST':
        status = int(request.POST.get('status', None))
        order_id = int(request.POST.get('order_id', None))

        s = "รับออเดอร์"
        print(order_id)
        print(status)
        if status == 0 :
            s = "รับออเดอร์"
            print(s)     
        elif status == 1:
            s = "กำลังทำอาหาร"
            print(s)
        elif status == 2 :
            s = "กำลังส่ง"
            print(s)
                                                
                                                
        Order.objects.filter(id=order_id).update(status=s)
        return JsonResponse({'status':True},safe=False)

@login_required
def update_status(request):
    order = Order.objects.all().order_by('-id')

    order_list = []
    menu_list = []
    amount_list = []
    
    for i in order :
        temp = {'user_name':"",'id':0,'name':"",'menu_amount':[],'date':None,
                    'status':'','total':0.0,'isSuccess':False,'create_at':""}

        temp['id'] = i.id
        temp['name'] = i.store.name
        temp['date'] = i.date
        temp['status'] = i.status
        temp['user_name'] = i.user.username
        temp['total'] = i.total
        temp['isSuccess'] = i.isSuccess
        temp['created_at'] = i.created_at
              
                
        for m,a in zip(i.menu,i.amount):
            ma = {'menu':None,'amount':a,}
                    
                   
            try:
                int(m)
                # m = Menu.objects.get(id=m)
                # ma['menu'] = m
               
                ma = {'menu':Menu.objects.get(id=m),'amount':a}
                temp['menu_amount'].append(ma)
                menu_list.append(Menu.objects.get(id=m))
                amount_list.append(a)


                        # ma = {'menu':Menu.objects.get(id=m).name,'amount':a}
                # temp['menu_amount'].append(ma)
                # print("temp",temp)
                        
                    
            except Exception as e:
                tuple_menu = literal_eval(m)
                main = Menu.objects.get(id=tuple_menu[0])
                ma['menu'] = main
                temp['menu_amount'].append(ma)
                menu_list.append(main)
                amount_list.append(a)

                    
        order_list.append(temp)
        # temp = {'user_name':"",'id':0,'name':"",'menu_amount':[],'total':0,'status':"",'isSuccess':False,'create_at':""}
        # temp['id'] = i.id
        # temp['name'] = i.store.name
        # temp['total'] = i.total
        # temp['status'] = i.status 
        # temp['user_name'] = i.user.username
        # temp['isSuccess'] = i.isSuccess
        # temp['created_at'] = i.created_at

        # for m,a in zip(i.menu,i.amount):
        
        #     ma = {'menu':Menu.objects.get(id=m),'amount':a}
        #     temp['menu_amount'].append(ma)
        #         #         #             menu_list.append(Menu.objects.get(id=m))
        #         #         #             amount_list.append(a)
                
        # order_list.append(temp)
                    
                    
    return render(request, 'update_status.html',{'order_list':order_list})
def check_time_open(store_id):
    try :   
        store = Store.objects.get(id=store_id)
        time = DeliveryTime.objects.get(store=store)
            # print(calendar.day_name[date.today().weekday()])
        day = date.today().weekday()
        print("day",day)
        time_now = datetime.now().time()
        print("time_now",time_now)
        time_status = 0
        if day == 0 :# monday

            if time.monday :
                time_open = time.monday_open
                time_close = time.monday_close
                if time_open is None and time_close is None:
                    time_status = 0

                else :
                    if time_now >= time_open :
                        if time_close < time_open : # ex. close 01.00
                            if date.today().weekday() == 1:
                                if time_now <= time_close:
                                    time_status = 1
                                else:
                                    time_status = 0 
                            else:
                                if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                    time_status = 1
                                else:
                                    time_status = 0
                                    
                                    
                        else:
                            if time_now <= time_close :
                                time_status = 1
                            else:
                                time_status = 0
                    else:
                        time_status = 0

            else :
                time_status = 0

            is_delivery = time.monday
                
        elif day == 1 :# tuesday
            if time.tuesday :
                time_open = time.tuesday_open
                time_close = time.tuesday_close
                if time_open is None and time_close is None:
                    time_status = 0
                else :
                    if time_now >= time_open and time_now <= time_close :
                        time_status = 1
            else :
                time_status = 0
            is_delivery = time.tuesday

        elif day == 2:  # wednesday
            if time.wednesday :
                time_open = time.wednesday_open
                time_close = time.wednesday_close
                if time_open is None and time_close is None:
                    time_status = 0
                else :
                    if time_now >= time_open :
                        if time_close < time_open : # ex. close 01.00
                            if date.today().weekday() == 3:
                                if time_now <= time_close:
                                    time_status = 1
                                else:
                                    time_status = 0 
                            else:
                                if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                    time_status = 1
                                else:
                                    time_status = 0 
                                        
                        else:
                            if time_now <= time_close :
                                time_status = 1

                            else:
                                time_status = 0
                    else:

                        time_status = 0
            else :
                time_status = 0
                
            is_delivery = time.wednesday


        elif day == 3 :# thursday
            if time.thursday :
                time_open = time.thursday_open
                time_close = time.thursday_close
                if time_open is None and time_close is None:
                    time_status = 0
                else :
                    if time_now >= time_open and time_now <= time_close :
                        time_status = 1
            else :
                time_status = 0

            is_delivery = time.thursday
                
        elif day == 4:# friday
            if time.friday :
                time_open = time.friday_open
                time_close = time.friday_close
                if time_open is None and time_close is None:
                    time_status = 0
                else :
                    if time_now >= time_open and time_now <= time_close :
                        time_status = 1
            else :
                time_status = 0
            is_delivery = time.friday
                
        elif day == 5 :# saturday
            if time.saturday :
                time_open = time.saturday_open
                time_close = time.saturday_close
                if time_open is None and time_close is None:
                    time_status = 0
                else :
                    if time_now >= time_open and time_now <= time_close :
                        time_status = 1
            else :
                time_status = 0
            is_delivery = time.saturday
        elif day == 6:# sunday
                # print(time.sunday)
            if time.sunday :
                time_open = time.sunday_open
                time_close = time.sunday_close
                    # print(time_close)
                    # print(time_open)
                if time_open is None and time_close is None:
                    time_status = 0
                    # print(None)
                else :
                    if time_now >= time_open and time_now <= time_close :
                        time_status = 1
            else :
                time_status = 0
            is_delivery = time.sunday

        return is_delivery,time_status
    except Exception as e:
        raise
        # print("eee",e)
        # return is_delivery,time_status
# def home_tohrung(request):
#     print(request.user)
    
#     print("actions",actions)
#     print("num_actions",num_actions)
#     print("next_state",next_state)
#     time_status = 0
#     delivery = False
#     is_delivery = False
#     store = Store.objects.get(name="พินิจโต้รุ่ง")
#     if "delivery" in store.tags :
#         delivery = True
#         is_delivery,time_status= check_time_open(store.id)
#         print("is_delivery",is_delivery)
#         print("time_status",time_status)

#     collect_session(request,"enter","โรงอาหารโต้รุ่ง")
#     output = []
#     print("earn")
#     if request.session.get('mycart',False):
        
#         my_item_in_cart = request.session.get('mycart',[])
#         temp_del = []
#         for i in my_item_in_cart:
#             if isinstance(i, list):
#                 print("i0",i[0])
#                 menu = Menu.objects.get(id=i[0])
#                 print("store id",menu.store.id)
#                 print("type store id",type(menu.store.id))
#                 # store = Store.objects.get(store=menu.store)
#                 if menu.store.id != 25:
#                     temp_del.append(i)
#             else:
#                 try:
#                     menu = Menu.objects.get(id=i)
#                     tohrung = Tohrung2.objects.get(store=menu.store) 
                    
#                 except Tohrung2.DoesNotExist as e:

#                     menu = Menu.objects.get(id=i)
#                     print("Tohrung2.DoesNotExist",menu.store)
#                     if menu.store.id != 25:
#                         temp_del.append(i)
                
                    
#         a = [x for x in my_item_in_cart if x not in temp_del]
#         del request.session['mycart']
#         request.session['mycart'] = a  
        

#         item_in_cart = len(request.session.get('mycart'))
#         # my_item_in_cart = request.session.get('mycart',[])

#         temp_cart = []
#         for i in my_item_in_cart:
#             if isinstance(i, list):
#                 temp_cart.append(tuple(i))
#             else:
#                 temp_cart.append(i)
        
#         # print("my_item_in_cart",my_item_in_cart)
#         my_dict = {i:temp_cart.count(i) for i in temp_cart}
#         print("my_dict",my_dict)
        
#         for m_id,amount in my_dict.items():
#             temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[]}
#             temp['amount'] = amount
#             if isinstance(m_id, tuple):
#                 # set steak or set salad
#                 # pass
#                 temp_set = {"menu_name":"","ingredient":[],"sauce":"","price":0.0,}
                
#                 menu = Menu.objects.get(id=m_id[0])


#                 temp_set["menu_name"] = menu.name
#                 index = 0
#                 for i in m_id:
#                     if index >=2:
#                         temp_set["ingredient"].append(i)
#                     index+=1

#                 # temp_set["side"] = side_name
#                 # temp_set["sauce"] = sauce.name.replace('(Sauce)', '')
#                 temp_price = int(menu.price)+ int(m_id[1])
#                 set_price = temp_price*int(amount)
#                 temp['price'] = set_price
#                 temp['set'] = temp_set
#                 output.append(temp)
                

#             else:
#                 menu = Menu.objects.get(id=m_id)
#                 temp['menu_id'] = m_id
#                 temp['name'] = menu.name
#                 temp['price'] = int(menu.price)*int(amount)
#                 output.append(temp)
    
#     else:
#         print("no len")
#         item_in_cart = None


#     return render(request, 'midnight.html',
#         {'item_in_cart':item_in_cart,
#         # 'output':output,
#         'output_in_cart':output,
#         'is_delivery':is_delivery,
#         'time_status':time_status,
#         })

def home_tohrung(request):
    gender = ""
    
    try:
        info = Informations.objects.get(user=request.user)
        gender = info.sex
    except Exception as e:
        gender="unknown"
    
    if gender == "female":
        # state 0 1 2
        # print("random 6-8",np.random.randint(0,3))
        state = 0
        pass
    elif gender == "male":
        # state 3 4 5
        # print("random 6-8",np.random.randint(3,6))
        state = 3
    elif gender == "unknown":
        state = 6 
    epsilon = 0.0
    ran = np.random.rand()
    if ran > epsilon:
        actions,num_actions,next_state= recommendation_actions(request,state)
    elif ran <= epsilon:
        actions,num_actions,next_state= recommendation_actions_whole_system(request,state)

    print("state",state)
    print("actions",actions)
    print("num_actions",num_actions)
    print("next_state",next_state)
    time_status = 0
    delivery = False
    is_delivery = False
    store = Store.objects.get(name="พินิจโต้รุ่ง")
    if "delivery" in store.tags :
        delivery = True

        try :
            time = DeliveryTime.objects.get(store=store)
                # print(calendar.day_name[date.today().weekday()])
            day = date.today().weekday()
            time_now = datetime.datetime.now().time()
            time_status = 0
            if day == 0 :# monday

                if time.monday :
                    time_open = time.monday_open
                    time_close = time.monday_close
                    if time_open is None and time_close is None:
                        time_status = 0

                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 1:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0
                                        
                                        
                            else:
                                if time_now <= time_close :
                                    time_status = 1
                                else:
                                    time_status = 0
                        else:
                            time_status = 0

                else :
                    time_status = 0

                is_delivery = time.monday
                    
            elif day == 1 :# tuesday
                if time.tuesday :
                    time_open = time.tuesday_open
                    time_close = time.tuesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.tuesday

            elif day == 2:  # wednesday
                if time.wednesday :
                    time_open = time.wednesday_open
                    time_close = time.wednesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 3:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                            
                            else:
                                if time_now <= time_close :
                                    time_status = 1

                                else:
                                    time_status = 0
                        else:

                            time_status = 0
                else :
                    time_status = 0
                    
                is_delivery = time.wednesday


            elif day == 3 :# thursday
                if time.thursday :
                    time_open = time.thursday_open
                    time_close = time.thursday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0

                is_delivery = time.thursday
                    
            elif day == 4:# friday
                if time.friday :
                    time_open = time.friday_open
                    time_close = time.friday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.friday
                    
            elif day == 5 :# saturday
                if time.saturday :
                    time_open = time.saturday_open
                    time_close = time.saturday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.saturday
            elif day == 6:# sunday
                    # print(time.sunday)
                if time.sunday :
                    time_open = time.sunday_open
                    time_close = time.sunday_close
                        # print(time_close)
                        # print(time_open)
                    if time_open is None and time_close is None:
                        time_status = 0
                        # print(None)
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.sunday
        except :
            pass
    collect_session(request,"enter","โรงอาหารโต้รุ่ง")
    output = []
    print("earn")
    if request.session.get('mycart',False):
        
        my_item_in_cart = request.session.get('mycart',[])
        temp_del_steak = []
        print("my_item_in_cart",my_item_in_cart)  
        for i in my_item_in_cart:
          
            if isinstance(i, list):
                temp_del_steak.append(i)
               
            else:
                try:
                    menu = Menu.objects.get(id=i)
                    tohrung = Tohrung2.objects.get(store=menu.store) 
                except Tohrung2.DoesNotExist as e:
                    temp_del_steak.append(i)
                    
        a = [x for x in my_item_in_cart if x not in temp_del_steak]
        del request.session['mycart']
        request.session['mycart'] = a  

        # print("temp_del_steak ",temp_del_steak )

        # request.session['mycart'] = my_item_in_cart  
        item_in_cart = len(request.session.get('mycart'))
        my_item_in_cart = request.session.get('mycart',[])
        print("my_item_in_cart",my_item_in_cart) 

        my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}
        print("my_dict",my_dict)
        
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0}
            
            
            menu = Menu.objects.get(id=m_id)
            temp['menu_id'] = m_id
            temp['name'] = menu.name
            temp['amount'] = amount
            temp['price'] = int(menu.price)*int(amount)
            output.append(temp)
    else:
        print("no len")
        item_in_cart = None
        
    recommendIsOpen = []
    recommendedList = []
    for a in actions:
        temp = {"menu":None,"is_delivery":True,"time_status":1}

        # d = DeliveryTime.objects.get(store__id=a.store.id)
        temp["menu"] = a

        is_delivery,time_status= check_time_open(a.store.id)
      
        # temp["is_delivery"] = is_delivery
        # temp["time_status"] = time_status
        print("is_delivery",temp["is_delivery"])
        print("time_status", temp["time_status"])
        recommendedList.append(temp)
    return render(request, 'midnight.html',
        {'item_in_cart':item_in_cart,
        'output':output,
        'is_delivery':is_delivery,
        'time_status':time_status,
        'num_actions':num_actions,
        'actions':actions,
        'state':state,
        'next_state':next_state,
        'recommendedList':recommendedList
        })


def add_steak_to_cart(request):
    # force quantity = 1
    if request.is_ajax():
        
        
        main_id = request.GET.get('main_id',False)
        side_id = request.GET.get('side_id',False)
        sauce_id = request.GET.get('sauce_id',False)
        menu_list = request.session.get('mycart',[])

        if main_id == side_id and side_id == sauce_id:
            menu_list.append(main_id)
        else:
            steak_set = []
            steak_set.append(main_id)
            steak_set.append(side_id)
            steak_set.append(sauce_id)
            cv_to_tuple = tuple(steak_set)
            menu_list.append(cv_to_tuple)

        request.session['mycart'] = menu_list
    
        item_in_cart = len(request.session.get('mycart'))

        output_list = []
        str_tr = "  <tr><td>฿ 20 </td><td>ชื่อ </td><td>x amount </td></tr>"
        str_set_steak = "  <tr><td>฿ 20 </td><td> <p> main </p>   <p> + side_dish </p> <p> + sauce </p> </td><td>x amount </td></tr>"
        # str_set_steak += "  <tr ><td>  </td><td> + side_dish </td></tr>"
        # str_set_steak += "  <tr><td>  </td><td> + sauce </td></tr>"
        table = []
        # for menu_id in reversed(request.session['mycart']):

        my_item_in_cart = request.session.get('mycart')
        temp_cart = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        my_dict = {i:temp_cart.count(i) for i in temp_cart}
        print("my_dict",my_dict)
        temp_cart_list = []
        for m_id,amount in my_dict.items():

            if isinstance(m_id, tuple):
                # temp_cart_list.append(tuple(m_id)) # add set steak
               
                main = Menu.objects.get(id=m_id[0])
                sauce = Menu.objects.get(id=m_id[2])
                sauce_name = sauce.name.replace('(Sauce)', '')

                if m_id[1]== '-1':
                    side_name = "ไม่เลือก"
                    
                else:
                    side = Menu.objects.get(id=m_id[1])
                    side_name = side.name.replace('(Side)', '')

                temp = str_set_steak.replace("main",main.name)
                temp2 = temp.replace("amount",str(amount))
                temp3 = temp2.replace("sauce",sauce_name)

                set_price = 0 
                if side_name == "ไม่เลือก":
                    set_price = int(main.price)*int(amount)
                else:
                    set_price = (int(main.price)+30.0)*int(amount)   

                temp4 = temp3.replace("side_dish",side_name)
                
               
                str_table = temp4.replace("20",str(set_price))
                table.append(str_table)
           
            else:
                try:
                    menu = Menu.objects.get(id=m_id)
                    tohrung = Tohrung2.objects.get(store=menu.store) 
                    # menu_list = request.session.get('mycart',[])
                 

        
                except Tohrung2.DoesNotExist as e:
                    # not in tohroong
                    temp_cart_list.append(m_id) 
            
                    menu = Menu.objects.get(id=m_id)
                    if "Steak" in menu.name:
                        temp = str_tr.replace("ชื่อ",menu.name)

                    elif "Solo" in menu.name:
                        temp = str_tr.replace("ชื่อ",menu.name.replace('(Solo)', ''))  
                    
                    temp2 = temp.replace("amount",str(amount))
                    str_table = temp2.replace("20",str(int(menu.price)*int(amount)))
                    table.append(str_table)
        # del request.session['mycart']

        # request.session['mycart'] = temp_cart_list # del cart in tohrung
        # print("temp_cart_list",temp_cart_list)
        print("request.session['mycart']",request.session['mycart'])
        item_in_cart = len(request.session.get('mycart'))
        # print("table",table)
        # total += int(menu.price)*int(amount)
        # temp ={"menu_name":"","menu_price":0}
        
        # print(menu)
        # temp["menu_name"] = menu.name
        # temp["menu_price"] = menu.price
        
        # output_list.append(temp)
        # print(output_list)
        
        
        # return HttpResponse({'item_in_cart':item_in_cart,'output_list':output_list}, content_type="application/json")
        return JsonResponse({'item_in_cart':item_in_cart,'table':table}, safe=False)


def add_to_cart(request):
    # force quantity = 1
    if request.is_ajax():
        
        menu_id = request.GET.get('menu_id',False)
        my_dorm = request.GET.get('myDorm',False)
        print(menu_id)
        add_menu_to_cart = Menu.objects.get(id=menu_id)

        str_add_to_cart = str(menu_id)+","+add_menu_to_cart.name
        collect_session(request,"เพิ่มเข้าตะกร้า",str_add_to_cart)

        str_menu = "<tr id='name_set'><td class='uk-width-small'><h4> name </h4></td><td class='uk-width-small'> <h4>x amount  </h4></td><td class='uk-width-small'>  <h4> price บาท</h4></td><td class='uk-width-small uk-text-center'  ><a class='remove_from_cart' name='menu_id'><h4 > <i class='fa fa-trash-o'></i></h4></a></td></tr>"
        temp = str_menu.replace("name",add_menu_to_cart.name)
            
        temp2 = temp.replace("name_set","set"+str(add_menu_to_cart.id))
        temp3 = temp.replace("amount",str(1))
        str_menu = temp3.replace("price",str(int(add_menu_to_cart.price)*1))




        print("test",request.session.get('mycart',[]))
        menu_list = request.session.get('mycart',[])
        print("type",type(menu_list))
        menu_list.append(menu_id)
        request.session['mycart'] = menu_list
    
        item_in_cart = len(request.session.get('mycart'))

        output_list = []
        str_tr = "  <tr><td>฿ 20 </td><td>ชื่อ </td><td>x amount </td></tr>"
        table = []
        # for menu_id in reversed(request.session['mycart']):
        my_item_in_cart = request.session.get('mycart',[])
        temp_cart = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        my_dict = {i:temp_cart.count(i) for i in temp_cart}
        isLookchin = False
        isMooping= False
        total_amount = 0
        total = 0
        print("my_dict",my_dict)
        for m_id,amount in my_dict.items():
            
            menu = Menu.objects.get(id=m_id)
            print("name",menu.name)
            temp = str_tr.replace("ชื่อ",menu.name)
            
            temp2 = temp.replace("amount",str(amount))
            str_table = temp2.replace("20",str(int(menu.price)*int(amount)))
            table.append(str_table)
        
            total += int(menu.price)*int(amount)
            if menu.store.name == "น้องแนนหมูปิ้ง":
                isMooping = True
            elif menu.store.name == "สมใจ ลูกชิ้นทอด":
                isLookchin = True
            elif menu.store.name != "น้องแนนหมูปิ้ง" or menu.store.name !="สมใจ ลูกชิ้นทอด":
                total_amount += amount

        if isLookchin:
            total_amount+=1
        if isMooping:
            total_amount +=1    
        print("ttotal_amount",total_amount)

        price_without_charge = total
        if my_dorm: # if user choose dorm
            if total_amount <=3:
                # delivery_charge = 25.0
                if my_dorm =="หอ B":
                    delivery_charge = 20.0
                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                    delivery_charge = 10.0
                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                    delivery_charge = 7.0    

            elif total_amount >=4:
                # delivery_charge = 30.0
                if my_dorm =="หอ B":
                    delivery_charge = 25.0
                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                    delivery_charge = 15.0
                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                    delivery_charge = 12.0
        else:
            delivery_charge = 0.0
        total+=delivery_charge       

        # temp ={"menu_name":"","menu_price":0}
        
        # print(menu)
        # temp["menu_name"] = menu.name
        # temp["menu_price"] = menu.price
        
        # output_list.append(temp)
        print("total",total)
        return JsonResponse({'total_price':str(total),'total_amount':total_amount,
            'price_without_charge':float(price_without_charge),
            'delivery_charge':float(delivery_charge),
            'table':str_menu,
            },safe=False)

        
        
        # return HttpResponse({'item_in_cart':item_in_cart,'output_list':output_list}, content_type="application/json")
        # return JsonResponse({'item_in_cart':item_in_cart,'table':table}, safe=False)


def st_remove_from_cart(request):
    if request.is_ajax():

        menu_id = request.GET.get('menu_id',False)
        name_set = request.GET.get('name_set',False)
        
        print("menu_id",menu_id)
        my_dorm = request.GET.get('myDorm',False)

        menu_list = request.session.get('mycart',[])
        temp_cart = []
        for i in menu_list:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
        
        # # print("menu_list",menu_list)
        # # del_list = list(menu_id)
        # # print("del_list",del_list)
        # # my_dict = {i:temp_cart.count(i) for i in temp_cart}  
        # print("type",type(menu_id))
        # print ("len",len(menu_id))

        try:
            int(menu_id)
            a = [x for x in temp_cart if x != str(menu_id)]
            print("a",a)
            del request.session['mycart']
            request.session['mycart'] = a

        except Exception as e:
            print("Exception")
            rm = literal_eval(menu_id)
            # menu_id = rm
            # print("menu_id rm",menu_id)
            a = [x for x in temp_cart if x != rm]

            del request.session['mycart']
            request.session['mycart'] = a
       
            


        total=0
        total_amount = 0
        output = []
        my_item_in_cart = request.session.get('mycart',[])
        print("after del my_item_in_cart",my_item_in_cart)
        temp_cart2 = []
        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart2.append(tuple(i))
            else:
                temp_cart2.append(i)

        my_dict = {i:temp_cart2.count(i) for i in temp_cart2}
        for m_id,amount in my_dict.items():
            if isinstance(m_id, tuple):       
                main = Menu.objects.get(id=m_id[0])
                total_amount += amount
                if m_id[1] == '-1':
                    total += int(main.price)*int(amount)
                else:
                    total += (int(main.price)+30.0)*int(amount)


            else:
                menu = Menu.objects.get(id=m_id)
                total += int(menu.price)*int(amount)
                total_amount += amount
            # output.append(temp)
        # 

        # isLookchin = False
        # isMooping = False
        # for m_id,amount in my_dict.items():
        #     temp={"name":"","price":0.0,"amount":0,"menu_id":0}
                
        #     menu = Menu.objects.get(id=m_id)
        #     temp['menu_id'] = m_id
        #     temp['name'] = menu.name
        #     temp['amount'] = amount
        #     temp['price'] = int(menu.price)*int(amount)
        #     total += int(menu.price)*int(amount)
        #     output.append(temp)

        #     if menu.store.name == "น้องแนนหมูปิ้ง":
        #         isMooping = True
        #     elif menu.store.name== "สมใจ ลูกชิ้นทอด":
        #         isLookchin = True
        #     elif menu.store.name != "น้องแนนหมูปิ้ง" or menu.store.name !="สมใจ ลูกชิ้นทอด":
        #         total_amount += amount

        # if isLookchin:
        #     total_amount+=1
        # if isMooping:
        #     total_amount +=1    
        price_without_charge = total
        print("myDorm",my_dorm)
        if my_dorm: # if user choose dorm
            if total_amount <=3:
                delivery_charge = 25.0
                # if my_dorm =="หอ B":
                #     delivery_charge = 20.0
                # elif my_dorm =="หอ C" or my_dorm =="หอ E":
                #     delivery_charge = 10.0
                # elif my_dorm =="หอ F" or my_dorm =="หอ M":
                #     delivery_charge = 7.0    

            elif total_amount >=4:
                delivery_charge = 30.0
                # if my_dorm =="หอ B":
                #     delivery_charge = 25.0
                # elif my_dorm =="หอ C" or my_dorm =="หอ E":
                #     delivery_charge = 15.0
                # elif my_dorm =="หอ F" or my_dorm =="หอ M":
                #     delivery_charge = 12.0
        else:
            delivery_charge = 0.0        

        total+=delivery_charge


            # menu = Menu.objects.get(id=m_id)
            # temp['name'] = m_id
            # temp['name'] = menu.name
            # temp['amount'] = amount
            # temp['price'] = int(menu.price)*int(amount)
            # total += int(menu.price)*int(amount)

            # output.append(temp)

        context = "success"
        print("gg")
        print("totl",total)
        return JsonResponse({'total_price':str(total),'total_amount':total_amount,
            'price_without_charge':float(price_without_charge),
            'id':name_set,'delivery_charge':float(delivery_charge)},safe=False)


def remove_from_cart(request):
    if request.is_ajax():

        menu_id = request.GET.get('menu_id',False)
        print("menu_id",menu_id)
        my_dorm = request.GET.get('myDorm',False)

        menu_list = request.session.get('mycart',[])
        # temp_cart = []
        # for i in menu_list:
        #     if isinstance(i, list):
        #         temp_cart.append(tuple(i))
        #     else:
        #         temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
        # my_dict = {i:temp_cart.count(i) for i in temp_cart}  

        a = [x for x in menu_list if x != str(menu_id)]
        print("a",a)
        del request.session['mycart']
        request.session['mycart'] = a


        total=0
        total_amount = 0
        output = []
        my_item_in_cart = request.session.get('mycart',[])
        my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}

        isLookchin = False
        isMooping = False
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0}
                
            menu = Menu.objects.get(id=m_id)
            temp['menu_id'] = m_id
            temp['name'] = menu.name
            temp['amount'] = amount
            temp['price'] = int(menu.price)*int(amount)
            total += int(menu.price)*int(amount)
            output.append(temp)

            if menu.store.name == "น้องแนนหมูปิ้ง":
                isMooping = True
            elif menu.store.name== "สมใจ ลูกชิ้นทอด":
                isLookchin = True
            elif menu.store.name != "น้องแนนหมูปิ้ง" or menu.store.name !="สมใจ ลูกชิ้นทอด":
                total_amount += amount

        if isLookchin:
            total_amount+=1
        if isMooping:
            total_amount +=1    
        price_without_charge = total
        print("myDorm",my_dorm)
        if my_dorm: # if user choose dorm
            if total_amount <=3:
                if my_dorm =="หอ B":
                    delivery_charge = 20.0
                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                    delivery_charge = 10.0
                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                    delivery_charge = 7.0    

            elif total_amount >=4:
                if my_dorm =="หอ B":
                    delivery_charge = 25.0
                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                    delivery_charge = 15.0
                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                    delivery_charge = 12.0
        else:
            delivery_charge = 0.0        

        total+=delivery_charge
            # menu = Menu.objects.get(id=m_id)
            # temp['name'] = m_id
            # temp['name'] = menu.name
            # temp['amount'] = amount
            # temp['price'] = int(menu.price)*int(amount)
            # total += int(menu.price)*int(amount)

            # output.append(temp)

        context = "success"
        print("gg")
        print("totl",total)
        return JsonResponse({'total_price':str(total),'total_amount':total_amount,
            'price_without_charge':float(price_without_charge),
            'id':menu_id,'delivery_charge':float(delivery_charge)},safe=False)




def until_dawn_canteen(request,store_name):
    gender = ""
    
    try:
        info = Informations.objects.get(user=request.user)
        gender = info.sex
    except Exception as e:
        gender="unknown"
    
    if gender == "female":
        # state 0 1 2
        # print("random 6-8",np.random.randint(0,3))
        state = 1
        pass
    elif gender == "male":
        # state 3 4 5
        # print("random 6-8",np.random.randint(3,6))
        state = 4
    elif gender == "unknown":
        # state 6 7 8
        state = 7 

    actions,num_actions,next_state= recommendation_actions(request,state)
    print("state",state)
    print("actions",actions)
    print("num_actions",num_actions)
    print("next_state",next_state)

    
    
    output_store = []
    menues_list = []
    store = Store.objects.get(name=store_name)
    enter_store = str(store.id)+","+store_name

    collect_session(request,"enter_store",enter_store)
    menues = Menu.objects.filter(store=store)
    print("menuuuuu")
    for menu in menues :
        temp = {'name':"",'image':None}
        if menu.image :
            # menues_list.append(menu.image.url)
            temp['name'] = menu.name
            temp['image'] = menu.image.url
            menues_list.append(temp)
        
    
    reviews = Review.objects.filter(store=store)
    # getreview and love
    
    time_status = 0
    delivery = False
    is_delivery = False
    if "delivery" in store.tags :
        delivery = True

        try :
            time = DeliveryTime.objects.get(store=store)
                # print(calendar.day_name[date.today().weekday()])
            day = date.today().weekday()
            time_now = datetime.datetime.now().time()
            time_status = 0
            if day == 0 :# monday

                if time.monday :
                    time_open = time.monday_open
                    time_close = time.monday_close
                    if time_open is None and time_close is None:
                        time_status = 0

                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 1:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0
                                        
                                        
                            else:
                                if time_now <= time_close :
                                    time_status = 1
                                else:
                                    time_status = 0
                        else:
                            time_status = 0

                else :
                    time_status = 0

                is_delivery = time.monday
                    
            elif day == 1 :# tuesday
                if time.tuesday :
                    time_open = time.tuesday_open
                    time_close = time.tuesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.tuesday

            elif day == 2:  # wednesday
                if time.wednesday :
                    time_open = time.wednesday_open
                    time_close = time.wednesday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open :
                            if time_close < time_open : # ex. close 01.00
                                if date.today().weekday() == 3:
                                    if time_now <= time_close:
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                else:
                                    if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
                                        time_status = 1
                                    else:
                                        time_status = 0 
                                            
                            else:
                                if time_now <= time_close :
                                    time_status = 1

                                else:
                                    time_status = 0
                        else:

                            time_status = 0
                else :
                    time_status = 0
                    
                is_delivery = time.wednesday


            elif day == 3 :# thursday
                if time.thursday :
                    time_open = time.thursday_open
                    time_close = time.thursday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0

                is_delivery = time.thursday
                    
            elif day == 4:# friday
                if time.friday :
                    time_open = time.friday_open
                    time_close = time.friday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.friday
                    
            elif day == 5 :# saturday
                if time.saturday :
                    time_open = time.saturday_open
                    time_close = time.saturday_close
                    if time_open is None and time_close is None:
                        time_status = 0
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.saturday
            elif day == 6:# sunday
                    # print(time.sunday)
                if time.sunday :
                    time_open = time.sunday_open
                    time_close = time.sunday_close
                        # print(time_close)
                        # print(time_open)
                    if time_open is None and time_close is None:
                        time_status = 0
                        # print(None)
                    else :
                        if time_now >= time_open and time_now <= time_close :
                            time_status = 1
                else :
                    time_status = 0
                is_delivery = time.sunday
        except :
            pass
    
    rate = []
    profile_picture = []
    store_loved_color = None
    if request.user.is_authenticated:
        user = request.user
        store = get_object_or_404(Store, id=store.id)
        if store.likes.filter(id=user.id).exists():
            store_loved_color= True
        else:
            store_loved_color = None

    for i in reviews:
        p = Profile.objects.get(user=i.user)
        temp = { 'rating_color': 0,'rating_no_color': 0,'username':""}
        temp['username'] = p.name
        temp['rating_color'] = i.rating
        temp['rating_no_color'] = 5 - temp['rating_color']
        rate.append(temp)
        try :
            profile_picture.append(Profile.objects.get(user=i.user).picture.url)
        except:
            raise
# raise Http404

    out = zip(reviews,rate,profile_picture)

    reviewForm = ReviewForm()
    # store = Store.objects.get(id=store_id)
    # reviews = Review.objects.filter(store=store)
    output = []
    print("earn")
    if request.session.get('mycart',False):
        item_in_cart = len(request.session.get('mycart'))
        my_item_in_cart = request.session.get('mycart',[])
        my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}
        print("my_dict",my_dict)
            
        for m_id,amount in my_dict.items():
            temp={"name":"","price":0.0,"amount":0,"menu_id":0}
                
                
            menu = Menu.objects.get(id=m_id)
            temp['menu_id'] = m_id
            temp['name'] = menu.name
            temp['amount'] = amount
            temp['price'] = int(menu.price)*int(amount)
            output.append(temp)
    else:
        print("no len")
        item_in_cart = None

    if request.method == 'POST':
        if "review" in request.POST:
            try:
                star = request.POST['star']
            except Exception as e:
                star = 0;
        
            
            print ("star: ",star)
            reviewForm = ReviewForm(request.POST, request.FILES)
            if reviewForm.is_valid():
                review = Review.objects.create(user = request.user,
                store = store,
                comment = reviewForm.cleaned_data['comment'],
                rating = star,)
                DisplayHome.objects.create(user=request.user,review=review)
                next_page = "/โรงอาหารโต้รุ่ง/"+store.name
                print("redirect")
                # return shop_decision(requset,store.name,store.id)
                # next_page = "/store/"+store.name+"/"+str(store_id)
                return HttpResponseRedirect(next_page)

    # print((request.session.get('mycart')))
    # print(len(request.session.get('mycart')))
    # item_in_cart = len(request.session.get('mycart'))
    # 'reviews':reviews,'out':out,'store':store,'delivery':delivery,'category':cate,
    #     'store_loved_color':store_loved_color,
    print("is_delivery",is_delivery)
    
    print("time_status",time_status)

    is_delivery =True
    time_status = 1
    print("state",state)
    print("actions",actions)
    print("num_actions",num_actions)
    print("next_state",next_state)



    recommendedList = []
    for a in actions:
        temp = {"menu":None,"is_delivery":True,"time_status":1}
        temp["menu"] = a 
        is_delivery,time_status= check_time_open(a.store.id)
      
        # temp["is_delivery"] = is_delivery
        # temp["time_status"] = time_status
        print("is_delivery",temp["is_delivery"])
        print("time_status", temp["time_status"])

        recommendedList.append(temp) 

    return render(request, 'until_dawn_canteen.html',{'store':store,
                  "menues":reversed(menues) ,"mobile_menues":reversed(menues),'reviewForm':reviewForm,
                  'item_in_cart':item_in_cart,"output":output,
                  'store_loved_color':store_loved_color,
                  'reviews':reviews,
                  'out':out,
                  'menues_list':menues_list,
                  'time_status':time_status,
                  'is_delivery':is_delivery,
                  'recommendedList':recommendedList,
                  'actions':actions,
                  'state':state,
                  'next_state':next_state,
                  'num_actions':num_actions,

                  })
# return render(request, 'night_canteen.html',{'reviewFor,"m':reviewForm,'store_loved_color':store_loved_color,})
@login_required
def st_checkout(request):
    collect_session(request,"enter","steak checkout")
    anythingElseForm = AnythingElseForm()
    output = []
    total=0
    total_amount = 0
    
    
    p = Profile.objects.get(user=request.user)
    delivery_address = p.address
    delivery_phone = p.phone_number
    
    # a = {"orderlist": [], "price": [], "url_pic": [], "amount": []}
    my_item_in_cart = request.session.get('mycart',[])
    # my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}
    
        # item_in_cart = len(request.session.get('mycart'))

    temp_cart = []
    for i in my_item_in_cart:
        if isinstance(i, list):
            temp_cart.append(tuple(i))
        else:
            temp_cart.append(i)
        
        # print("my_item_in_cart",my_item_in_cart)
    my_dict = {i:temp_cart.count(i) for i in temp_cart}
    
    print("my_dict",my_dict)
    count = 0
        
    for m_id,amount in my_dict.items():
        temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[],"name_set":""}
        temp['amount'] = amount
        temp['menu_id'] = m_id

        if isinstance(m_id, tuple):
            temp_set = {"main":"","side":"","sauce":"","price":0.0,}
            

            main = Menu.objects.get(id=m_id[0])
            sauce = Menu.objects.get(id=m_id[2])

            set_price = 0

            if m_id[1]== '-1':
                side_name = "ไม่เลือก"
                set_price = int(main.price)*int(amount)
                    
            else:
                side = Menu.objects.get(id=m_id[1])
                side_name = side.name.replace('(Side)', '')
                set_price = (int(main.price)+30.0)*int(amount)

            
            # side = Menu.objects.get(id=m_id[1])
            

            temp_set["main"] = main.name
            temp_set["side"] = side_name
            temp_set["sauce"] = sauce.name.replace('(Sauce)', '')

            temp['price'] = set_price
            temp['set'] = temp_set
            output.append(temp)
            total_amount += amount
            total += set_price
            temp['name_set'] = "set"+str(count)+str(amount)
                

        else:
            menu = Menu.objects.get(id=m_id)
            temp['name_set'] = "set"+str(count)+str(amount)
            if "Solo" in menu.name:
               temp['name'] = menu.name.replace('(Solo)', '')
            else:
                temp['name'] = menu.name
                
            temp['price'] = int(menu.price)*int(amount)
            total += int(menu.price)*int(amount)
            total_amount += amount
            output.append(temp)
        count += 1
    # isMooping = False
    # isLookchin = False
    
    # for m_id,amount in my_dict.items():
    #     temp={"name":"","price":0.0,"amount":0,"menu_id":0}
        
    #     menu = Menu.objects.get(id=m_id)
    #     temp['menu_id'] = m_id
    #     temp['name'] = menu.name
    #     temp['amount'] = amount
    #     temp['price'] = int(menu.price)*int(amount)
    #     total += int(menu.price)*int(amount)
    #     output.append(temp)
    #     print("name",type(menu.store))
    #     print("sname",type(menu.store.name))
   
    #     if menu.store.name == "น้องแนนหมูปิ้ง":
    #         isMooping = True
    #     elif menu.store.name == "สมใจ ลูกชิ้นทอด":
    #         isLookchin = True
    #     elif menu.store.name != "น้องแนนหมูปิ้ง" or menu.store.name !="สมใจ ลูกชิ้นทอด":
    #         total_amount += amount

    # if isLookchin:
    #     total_amount+=1
    # if isMooping:
    #     total_amount +=1    


    # print("total_amount",total_amount)

    # item_in_cart = len(request.session.get('mycart'))
    delivery_charge = 0.0;
    
    # if total_amount <=3:
    #     delivery_charge = 5.0
    # elif total_amount >=4 and total_amount <=5:
    #     delivery_charge = 10.0
    # elif total_amount >=6 and total_amount <=7:
    #     delivery_charge = 15.0
    # elif total_amount >=8 and total_amount <=9:
    #     delivery_charge = 20.0
    # elif total_amount >=10:
        # delivery_charge = 25



    total+=delivery_charge
   

    return  render(request,'st_checkout.html',{'item_in_cart':total_amount,
               'data':json.dumps(output),
               'output':output,'total':total,'delivery_address':delivery_address,
               'delivery_phone':delivery_phone,'delivery_charge':delivery_charge,
               })

@login_required
def ud_checkout(request):
    collect_session(request,"enter","โต้รุ่ง checkout")
    anythingElseForm = AnythingElseForm()
    output = []
    total=0
    total_amount = 0
    
    
    p = Profile.objects.get(user=request.user)
    delivery_address = p.address
    delivery_phone = p.phone_number
    
    # a = {"orderlist": [], "price": [], "url_pic": [], "amount": []}
    my_item_in_cart = request.session.get('mycart',[])
    my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}
    
    isMooping = False
    isLookchin = False
    
    for m_id,amount in my_dict.items():
        temp={"name":"","price":0.0,"amount":0,"menu_id":0}
        
        menu = Menu.objects.get(id=m_id)
        temp['menu_id'] = m_id
        temp['name'] = menu.name
        temp['amount'] = amount
        temp['price'] = int(menu.price)*int(amount)
        total += int(menu.price)*int(amount)
        output.append(temp)
        print("name",type(menu.store))
        print("sname",type(menu.store.name))
   
        if menu.store.name == "น้องแนนหมูปิ้ง":
            isMooping = True
        elif menu.store.name == "สมใจ ลูกชิ้นทอด":
            isLookchin = True
        elif menu.store.name != "น้องแนนหมูปิ้ง" or menu.store.name !="สมใจ ลูกชิ้นทอด":
            total_amount += amount

    if isLookchin:
        total_amount+=1
    if isMooping:
        total_amount +=1    


    print("total_amount",total_amount)

    # item_in_cart = len(request.session.get('mycart'))
    delivery_charge = 0.0;
    
    # if total_amount <=3:
    #     delivery_charge = 5.0
    # elif total_amount >=4 and total_amount <=5:
    #     delivery_charge = 10.0
    # elif total_amount >=6 and total_amount <=7:
    #     delivery_charge = 15.0
    # elif total_amount >=8 and total_amount <=9:
    #     delivery_charge = 20.0
    # elif total_amount >=10:
        # delivery_charge = 25



    total+=delivery_charge
    gender = ""
    
    try:
        info = Informations.objects.get(user=request.user)
        gender = info.sex
    except Exception as e:
        gender="unknown"
    
    if gender == "female":
        # state 0 1 2
        # print("random 6-8",np.random.randint(0,3))
        state = 2
        pass
    elif gender == "male":
        # state 3 4 5
        # print("random 6-8",np.random.randint(3,6))
        state = 5
    elif gender == "unknown":
        # state 6 7 8
        state = 8 

    actions,num_actions,next_state= recommendation_actions(request,state)
    print("state",state)
    print("actions",actions)
    print("num_actions",num_actions)
    print("next_state",next_state)


    recommendedList = []
    for a in actions:
        temp = {"menu":None,"is_delivery":True,"time_status":1}
        temp["menu"] = a 
        is_delivery,time_status= check_time_open(a.store.id)
      
        # temp["is_delivery"] = is_delivery
        # temp["time_status"] = time_status
        print("is_delivery",temp["is_delivery"])
        print("time_status", temp["time_status"])

        recommendedList.append(temp) 

   

    return  render(request,'ud_checkout.html',{'item_in_cart':total_amount,
               'data':json.dumps(output),
               'output':output,'total':total,'delivery_address':delivery_address,
               'delivery_phone':delivery_phone,'delivery_charge':delivery_charge,
               'num_actions':num_actions,
               'state':state,
               'actions':actions,
               "next_state":next_state,
               "recommendedList":recommendedList,
               })


@login_required
def st_delivery(request):
    
    
    if request.is_ajax():
        address = request.GET.get('address',False)
        phone_number = request.GET.get('phone_number',False)
        total_price = request.GET.get('total_price',False)
        delivery_charge = request.GET.get('delivery_charge',False)
        code_cou = request.GET.get('code_cou',False)
        myAnythingElse = request.GET.get('myAnythingElse',False)
        
   
        print(address)
        # print("payment ",payment)
        menu_list = []
        amount_list = []
        my_item_in_cart = request.session.get('mycart',[])

        temp_cart = []

        for i in my_item_in_cart:
            if isinstance(i, list):
                temp_cart.append(tuple(i))
            else:
                temp_cart.append(i)
            
        my_dict = {i:temp_cart.count(i) for i in temp_cart}

        store_id = 0
        for m_id,amount in my_dict.items():

            if isinstance(m_id, tuple):
                menu_list.append(tuple(m_id))
                amount_list.append(amount)

            else:
                menu = Menu.objects.get(id=m_id)
                store_id = menu.store.id
                menu_list.append(m_id)
                amount_list.append(amount)
         
        print("store_id",store_id)
        s = Store.objects.get(id=24)
        print("menulist",menu_list)
        print("amount_list",amount_list)
        order = Order.objects.create(user=request.user,
            menu=menu_list,
            store=s,
            amount=amount_list,
            address =address,
            total=total_price,
            phone_number=phone_number,
            delivery_charge=delivery_charge,
            coupon=code_cou,
            morethings=myAnythingElse,
            status="รับออเดอร์")
            
                                     
                                     # str_order += "==================\n"
                                     
                                     # print("order_id : ",order.id)
        next_page = "st-select-payment"
        return JsonResponse({'next_page':next_page,'order_id':order.id},safe=False)

@login_required
def ud_delivery(request):
    
    
    if request.is_ajax():
        address = request.GET.get('address',False)
        phone_number = request.GET.get('phone_number',False)
        total_price = request.GET.get('total_price',False)
        delivery_charge = request.GET.get('delivery_charge',False)
        code_cou = request.GET.get('code_cou',False)
        myAnythingElse = request.GET.get('myAnythingElse',False)
        
   
        print(address)
        # print("payment ",payment)
        menu_list = []
        amount_list = []
        my_item_in_cart = request.session.get('mycart',[])
        my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}
        print("my_item_in_cart",my_dict)
        for m_id,amount in my_dict.items():
            print("mid",m_id)
            print("amounr",amount)
           
                
                
            menu = Menu.objects.get(id=m_id)
           
            menu_list.append(menu.id)
            amount_list.append(amount)
    
        s = Store.objects.get(name="โรงอาหารโต้รุ่ง")
        print("menulist",menu_list)
        print("amount_list",amount_list)
        order = Order.objects.create(user=request.user,
            menu=menu_list,
            store=s,
            amount=amount_list,
            address =address,
            total=total_price,
            phone_number=phone_number,
            delivery_charge=delivery_charge,
            coupon=code_cou,
            morethings=myAnythingElse,
            status="รับออเดอร์")
            
                                     
                                     # str_order += "==================\n"
                                     
                                     # print("order_id : ",order.id)
        next_page = "ud-select-payment"
        return JsonResponse({'next_page':next_page,'order_id':order.id},safe=False)

@login_required
def st_payment(request,order_id):
    print("st paymnet")
    
    try:
        slipForm = SlipPaymentForm()
        o = Order.objects.get(id=order_id)
        total = o.total
        
        # store=o.store
        payment_list =[]
        # pay = Payment.objects.filter(store=store)
        
        if request.method == 'POST':
            slipForm = SlipPaymentForm(request.POST,request.FILES)
            if "byCash" in request.POST:
                # print("Earn")
                slipForm.fields['slip_image'].required = False
        
            if slipForm.is_valid():
                str_coupon =""
                print("o.coupon",o.coupon)
                if o.coupon !="":
                    try:
                        cou = GetCoupon.objects.get(coupon__code=o.coupon,user=request.user)
                        DisplayHome.objects.create(user=request.user,coupon=cou.coupon)
                        cou.amount -= 1
                        cou.save()
                        code_c = CodeType.objects.get(coupon=cou.coupon)
                        if code_c.code_type == "แถม":
                            str_coupon += code_c.value
                        else:
                            str_coupon += code_c.coupon.msg +" "+code_c.value
                    except :
                        o.coupon =""
                        o.save()

                # order_update = Order.objects.get(id=order_id)
                o.isSuccess = True
                o.save()

                print("order update",o)
                str_order="#"+str(o.id) +" \n"
                str_order+="=== รายการออร์เดอร์ ===\n"
                payment = ""
                link_slip = ""
                if slipForm.cleaned_data['slip_image'] is None:
                    o.payment_method="จ่ายเงินปลายทาง"
                    o.save()
                    # order.update(payment_method="จ่ายเงินปลายทาง")
                    payment="จ่ายเงินปลายทาง"
                else:
                    o.payment_method="พร้อมเพย์"
                    payment="พร้อมเพย์"
                    o.slip_payment = request.FILES['slip_image']
                    o.save()
                    link_slip = "www.ginimm.com/show-slip-"+str(o.id)
                    
                
                for m,a in zip(o.menu,o.amount):
        
                    print("m",m)
                    print("type m ",type(m))
                    try:
                        int(m)
                        menu =Menu.objects.get(id=m)
             
                        price = int(a) * menu.price
              
                        st_name =str(menu.store.name)
     
                        str_order += str(menu.name)+" "+str(price) + " บาท"+ " x "+ a +"\n"
                    
                    except Exception as e:
                        
                        tuple_menu = literal_eval(m)
                        print("tuple_menu",tuple_menu)
                        print("type tuple_menu",type(tuple_menu))
                        
                        main = Menu.objects.get(id=tuple_menu[0])
                        sauce = Menu.objects.get(id=tuple_menu[2])
                        sauce_name = sauce.name.replace('(Sauce)', '')
                        set_price = 0

                        if tuple_menu[1]== '-1':
                            side_name = "ไม่เลือก"
                            set_price = int(main.price)
                                
                        else:
                            side = Menu.objects.get(id=tuple_menu[1])
                            side_name = side.name.replace('(Side)', '')
                            set_price = (int(main.price)+30.0)

                        str_order +=  str(main.name)+"\n +"+side_name+"\n +"+sauce_name+"\n "+" ราคา "+str(set_price) + " บาท"+ " x "+ a +"\n"

                   
                        
                
                #     menu =Menu.objects.get(id=m)
             
                #     price = int(a) * menu.price
              
                #     st_name =str(menu.store.name)
     
                #     str_order += "ร้าน"+ st_name +": "+ str(menu.name)+" "+str(price) + " บาท"+ " x "+ a +"\n"
                
     
                if o.morethings != "":
                    str_order += "==== สิ่งที่ต้องการเพิ่มเติม ==== "+ "\n"
                    str_order += o.morethings + "\n"
                if str_coupon != "":
                    str_order += "ใช้คูปอง" + str_coupon+ " \n"
                
                p = Profile.objects.get(user=request.user)
                str_order += "===================\n"
                str_order += "ค่าจัดส่ง "+ str(o.delivery_charge)+ " บาท\n"
                str_order += "ราคารวม "+ str(o.total)+ " บาท\n"
                str_order += "เบอร์โทรศัพท์ติดต่อ "+o.phone_number +"\n"
                str_order += "ที่อยู่จัดส่ง "+o.address+"\n"
                str_order += "วิธีการชำระเงิน "+payment+"\n"
                str_order += "ขื่อผู้รับ "+p.name+"\n"
                if link_slip != "":
                    str_order+= "สามารถดูสลิปโอนเงินได้ที่นี่ "+link_slip
                collect_session(request,"สั่งอาหาร",o.id)
             
                # toey
                # line_bot_api.push_message('Uf5880cbaf8c0f778fc9489af4ff34bf5', TextSendMessage(text=str_order))
                # line_bot_api.push_message('U47ea5d1a29927a509fcab4afe475c122', TextSendMessage(text=str_order))
                # # earn
                # line_bot_api.push_message('Ucbb8d9d8af074f86b827b5a55e0b5ded', TextSendMessage(text=str_order))
                # # p'pond
                # line_bot_api.push_message('Uc08d56c0071797e83e5437b3a0be3414', TextSendMessage(text=str_order))
                # # p'matoom
                # line_bot_api.push_message('U63f4871892a259090d7b616dde01d05b', TextSendMessage(text=str_order))

                
                
                # line = LineStore.objects.get(name=store.name)
                # line_bot_api.push_message(line.uid, TextSendMessage(text=strdecode))
                # line_bot_api.push_message('Ucbb8d9d8af074f86b827b5a55e0b5ded', TextSendMessage(text=strdecode))
                
                del request.session['mycart']

                next_page = "/order-success/"+str(order_id)
                return HttpResponseRedirect(next_page)
        return render(request,'st_payment.html',{'slipForm':slipForm,'total':total,})

    except Exception as e:
        raise
        # messages.error(request, e)
        # raise Http404()

@login_required
def ud_payment(request,order_id):
    
    try:
        slipForm = SlipPaymentForm()
        o = Order.objects.get(id=order_id)
        total = o.total
        
        # store=o.store
        payment_list =[]
        # pay = Payment.objects.filter(store=store)
        
        if request.method == 'POST':
            slipForm = SlipPaymentForm(request.POST,request.FILES)
            if "byCash" in request.POST:
                print("Earn")
                slipForm.fields['slip_image'].required = False
        
            if slipForm.is_valid():
                str_coupon =""
                print("o.coupon",o.coupon)
                if o.coupon !="":
                    try:
                        cou = GetCoupon.objects.get(coupon__code=o.coupon,user=request.user)
                        DisplayHome.objects.create(user=request.user,coupon=cou.coupon)
                        cou.amount -= 1
                        cou.save()
                        code_c = CodeType.objects.get(coupon=cou.coupon)
                        if code_c.code_type == "แถม":
                            str_coupon += code_c.value
                        else:
                            str_coupon += code_c.coupon.msg +" "+code_c.value
                    except :
                        o.coupon =""
                        o.save()

                # order_update = Order.objects.get(id=order_id)
                o.isSuccess = True
                o.save()

                print("order update",o)
                str_order="#"+str(o.id) +" \n"
                str_order+="=== รายการออร์เดอร์ ===\n"
                payment = ""
                link_slip = ""
                if slipForm.cleaned_data['slip_image'] is None:
                    o.payment_method="จ่ายเงินปลายทาง"
                    o.save()
                    # order.update(payment_method="จ่ายเงินปลายทาง")
                    payment="จ่ายเงินปลายทาง"
                else:
                    o.payment_method="พร้อมเพย์"
                    payment="พร้อมเพย์"
                    o.slip_payment = request.FILES['slip_image']
                    o.save()
                    link_slip = "www.ginimm.com/show-slip-"+str(o.id)
                
                
                for m,a in zip(o.menu,o.amount):
                    menu =Menu.objects.get(id=m)
             
                    price = int(a) * menu.price
              
                    st_name =str(menu.store.name)
     
                    str_order += "ร้าน"+ st_name +": \n"+ str(menu.name)+" "+str(price) + " บาท"+ " x "+ a +"\n"
                
     
                if o.morethings != "":
                    str_order += "==== สิ่งที่ต้องการเพิ่มเติม ==== "+ "\n"
                    str_order += o.morethings + "\n"
                if str_coupon != "":
                    str_order += "ใช้คูปอง" + str_coupon+ " \n"
                
                p = Profile.objects.get(user=request.user)
                str_order += "===================\n"
                str_order += "ค่าจัดส่ง "+ str(o.delivery_charge)+ " บาท\n"
                str_order += "ราคารวม "+ str(o.total)+ " บาท\n"
                str_order += "เบอร์โทรศัพท์ติดต่อ "+o.phone_number +"\n"
                str_order += "ที่อยู่จัดส่ง "+o.address+"\n"
                str_order += "วิธีการชำระเงิน "+payment+"\n"
                str_order += "ขื่อผู้รับ "+p.name+"\n"
                if link_slip != "":
                    str_order+= "สามารถดูสลิปโอนเงินได้ที่นี่ "+link_slip
                collect_session(request,"สั่งอาหาร",o.id)
             
                # toey
                # line_bot_api.push_message('Uf5880cbaf8c0f778fc9489af4ff34bf5', TextSendMessage(text=str_order))
                # line_bot_api.push_message('U47ea5d1a29927a509fcab4afe475c122', TextSendMessage(text=str_order))
                # # earn
                # line_bot_api.push_message('Ucbb8d9d8af074f86b827b5a55e0b5ded', TextSendMessage(text=str_order))
                
                
                # line = LineStore.objects.get(name=store.name)
                # line_bot_api.push_message(line.uid, TextSendMessage(text=strdecode))
                # line_bot_api.push_message('Ucbb8d9d8af074f86b827b5a55e0b5ded', TextSendMessage(text=strdecode))
                
                del request.session['mycart']

                next_page = "/success/"+str(order_id)
                return HttpResponseRedirect(next_page)
        return render(request,'ud_payment.html',{'slipForm':slipForm,'total':total,})

    except Exception as e:
        raise
        # messages.error(request, e)
        # raise Http404()

def home(request):
    collect_session(request,"enter","home")
    c = Coupon.objects.all()
    for i in c :
        if date.today() > i.date_expire:
            i.delete()

    display_list = DisplayHome.objects.all().order_by('-created_at')[:10]
    print("display_list ",display_list)
    # out= []
    # mobile_out =[]
    rate = []
    profile_picture = []
    reviews_list = []
    desktop = []
    mobile = []
    item_list =[]
    # coupon_list= []
    for item in display_list:
        print(item.review)
        print(item.coupon)
        if item.coupon is None :
            if item.review is None :
                print("item",item)

                # information = Informations.objects.get(id=item.information.id)
                # item_list = {'username':'','profile_picture': None,'message' :'','store':''
                # ,'type':'information','create_at' : None}
                # item_list['profile_picture'] = Profile.objects.get(user=item.user).picture.url
                # item_list['message'] = 'กรอกประวัติความหิว'
                # p = Profile.objects.get(user=item.user)
                # item_list['username'] = p.name
                # item_list['create_at'] = item.information.created_at
            else:
                item_list = {'rating_color': 0 ,'rating_no_color': 0 ,'profile_picture':None,
                    'type':'review','store':'','username':'','create_at' : None,'comment' : '',"store_id":0}
                temp = { 'rating_color': 0,'rating_no_color': 0, }

                item_list['rating_color'] = item.review.rating
                item_list['rating_no_color'] = 5 - item_list['rating_color']
                    # item_list['reiview'] = item.review
                    # item_list['rate'] =temp
                    # item_list['rate'] =temp
                p = Profile.objects.get(user=item.user)
                item_list['store'] = item.review.store.name
                item_list['store_id'] = item.review.store.id
                item_list['username'] = p.name
                item_list['create_at'] = item.created_at
                item_list['comment'] = item.review.comment


                item_list['profile_picture'] = Profile.objects.get(user=item.review.user).picture.url
                print("item_list coupon  ",item_list)
            print("item_list coupon none ",item_list)
        elif item.review is None :
            if item.coupon is None :
                information = Informations.objects.get(id=item.information.id)
                item_list = {'username':'','profile_picture': None,'message' :'','store':''
                ,'type':'information','create_at' : None}
                item_list['profile_picture'] = Profile.objects.get(user=item.user).picture.url
                item_list['message'] = 'กรอกประวัติความหิว'
                p = Profile.objects.get(user=item.user)
                item_list['username'] = p.name
                item_list['create_at'] = item.information.created_at
        
            else:
                coupon = Coupon.objects.get(id=item.coupon.id)
                item_list = {'username':'','profile_picture': None,'coupon_msg' :'','store':''
                ,'type':'coupon','create_at' : None}
                item_list['profile_picture'] = Profile.objects.get(user=item.user).picture.url
                item_list['coupon_msg'] = coupon.msg
                item_list['store'] = coupon.store.name
                p = Profile.objects.get(user=item.user)
                item_list['username'] = p.name
                item_list['create_at'] = item.created_at
                print("item_list review  ",item_list)

            print("item_list review none ",item_list)
        desktop.append(item_list)
        mobile.append(item_list)



    response = set_cookie(request, 'home.html', {'desktop':desktop,'mobile':mobile})
    
    
    return response


@login_required
def addStore(request):
	addForm = StoreForm()
	if request.method == 'POST':
		addForm = StoreForm(request.POST, request.FILES)
		if addForm.is_valid():
			day_from_choice= addForm.cleaned_data['day_open']
			day=""
			day_from_choice = int(day_from_choice)
			print(addForm.cleaned_data['day_open'])
			print(day_from_choice)
			if day_from_choice == 1:
				day = "วันจันทร์"
			elif day_from_choice == 2:
				day = "วันอังคาร"
			elif day_from_choice == 3:
				day = "วันพุธ"
			elif day_from_choice == 4:
				day = "วันพฤหัสบดี"	
			elif day_from_choice == 5:
				day = "วันศุกร์"
			elif day_from_choice == 6:
				day = "วันเสาร์"
			elif day_from_choice == 7:
				day = "วันอาทิตย์"
			elif day_from_choice == 8:
				day = "วันจันทร์ - วันศุกร์"
			elif day_from_choice == 9:
				day = "วันเสาร์ - วันอาทิตย์"				
			elif day_from_choice == 0:
				day = "ทุกวัน"		

			tag=addForm.cleaned_data['tags']
			delivery= addForm.cleaned_data['delivery'],
			if delivery == True:
				tag += ",delivery"
			print(delivery)
			create_store = Store.objects.create(
		           user = request.user,
		           name = addForm.cleaned_data['store_name'],
		           place = addForm.cleaned_data['place'],
		           phone = addForm.cleaned_data['phone'],
		           category = addForm.cleaned_data['category'],
		           day_open =  day,
		           time_open= addForm.cleaned_data['time_open'],
		           time_close= addForm.cleaned_data['time_close'],
		           tags=tag,
		           image =request.FILES['store_image'],
		           )
			collect_session(request,"เพิ่มร้านค้า",create_store.id)
			next_page = "/store/"+str(create_store.id)+"/"+str(create_store.name)
			return HttpResponseRedirect(next_page)

	return render(request, 'addStore.html', {'addStoreForm':addForm,})
    # return redirect('loginapp.add_store')

@login_required
def addMenu(request,pk):
	menuForm = MenuForm()
	try:
		store = Store.objects.get(id=pk)
		if request.method == 'POST':
			menuForm = MenuForm(request.POST, request.FILES)
			if menuForm.is_valid():
				print("is valid")
				create_menu = Menu.objects.create(
					store = store,
		          	name = menuForm.cleaned_data['menu_name'],
		          	price = menuForm.cleaned_data['menu_price'],
		          	image =request.FILES['menu_image'],
		          	created_by= request.user)
				collect_session(request,"เพิ่มเมนู",create_menu.id)
				next_page = "/store/"+str(pk)+"/"+store.name
				return HttpResponseRedirect(next_page)
	except Store.DoesNotExist:
		return HttpResponseRedirect('home')	
	
				# return render() go to some page that tell error not have tihs store 
	return render(request, 'addMenu.html', {'menuForm':menuForm,'store_name':store.name})

def set_cookie(request,template,dicts):
	response = render(request, template, dicts)
	if request.user.is_authenticated:
		print("User has login")
	else :
		if not request.session.session_key:
			request.session.save()
		session_id = request.session.session_key
		if 'name' in request.COOKIES:
			value = request.COOKIES['name']
			# response.delete_cookie('name')
			print("old cookie "+ value)
		else :
			# expire in 10 years
			response.set_cookie('name',session_id,max_age= 315360000)
			print(" new cookie create")

	return response
     
@login_required
def report(request):
	form = SelectMonthForm()
	# collect_session(request,"รีวิวร้านค้า",review.id)
	today =datetime.date.today()
	today_name = today.strftime('%B')
	month_name= today.strftime('%B')
	year = today.strftime('%Y')
	store = StoreByUser.objects.get(user = request.user).store
	reviews_count = Review.objects.filter(store=store).count()
	order_count = Order.objects.filter(store=store).count()
	member_viewer = User_session.objects.filter(action="enter_store",value=store.name).count()
	anonymous_viewer =Anonymous_session.objects.filter(action="enter_store",value=store.name).count()
	viewer = member_viewer+anonymous_viewer
	# service = request.POST['statistic']
	stat, created = Statistic.objects.update_or_create(month="แสดงทั้งหมด",
                defaults={'store':store,'month':"แสดงทั้งหมด",
                'love': store.total_likes,
                'view':viewer,
                'order':order_count,
                'review':reviews_count})

	now = datetime.datetime.now()
	first_day_string = "2018-02-01"
	first_day = datetime.datetime.strptime(first_day_string, "%Y-%m-%d").date()
	differ = datetime.date.today() - first_day

	

	m_viewer =  User_session.objects.filter(action="enter_store",value=store.id,created_at__year=today.year, created_at__month=today.month).count()
	a_viewer = Anonymous_session.objects.filter(action="enter_store",value=store.id,created_at__year=today.year, created_at__month=today.month).count()
	viewed_by_month = m_viewer+a_viewer
	ordered_by_month = Order.objects.filter(store=store,created_at__year=today.year, created_at__month=today.month).count()
	liked_by_month = User_session.objects.filter(action="like",value=store.id,created_at__year=today.year, created_at__month=today.month).count()
	reviewed_by_month = Review.objects.filter(store=store,created_at__year=today.year, created_at__month=today.month).count()
	
	
	stat, created = Statistic.objects.update_or_create(month=month_name,
                defaults={'store':store,'month':month_name,
                'love': liked_by_month,
                'view':viewed_by_month,
                'order':ordered_by_month,
                'review':reviewed_by_month})
	viewer_list_per_day = []
	for i in reversed(range(differ.days)):
		member_viewer_yesterday = 0
		anonymous_viewer_yesterday =0
		viewer_yesterday =0
		# print('',i+1)
		yesterday = datetime.date.today() - datetime.timedelta(days=i+1)
		member_viewer_yesterday =  User_session.objects.filter(action="enter_store",value=store.name,created_at__date=yesterday).count()
		anonymous_viewer_yesterday = Anonymous_session.objects.filter(action="enter_store",value=store.name,created_at__date=yesterday).count()
		# print("member_viewer_yesterday ",member_viewer_yesterday)

		viewer_yesterday= int(anonymous_viewer_yesterday)+int(member_viewer_yesterday)
		viewer_list_per_day.append(viewer_yesterday)

	if request.method == 'POST':
		print("post")

		form = SelectMonthForm(request.POST)
		if form.is_valid():
			print("formvalid")
			statistic = None
			selected =  form.cleaned_data['action'] 
			print ("selected",selected)
			if selected == '0':
				print("0")

				statistic = Statistic.objects.get(store=store,month="แสดงทั้งหมด")
				month_name = "แทดสงทั้งหมดในปี"
				
			elif selected == '1':
				try:
					statistic = Statistic.objects.get(store=store,month="January")
					month_name = "January"
				except Exception as e:
					statistic = None
				
			elif selected == '2':
				try:
					statistic = Statistic.objects.get(store=store,month="February")
					month_name = "February"
				except Exception as e:
					statistic = None
				

			elif selected == '3':
				try:
					statistic = Statistic.objects.get(store=store,month="March")
					month_name = "March"
				except Exception as e:
					statistic = None
				

			elif selected == '4':
				try:
					statistic = Statistic.objects.get(store=store,month="April")
					month_name = "April"
				except Exception as e:
					statistic = None
				
				
			elif selected == '5':
				try:
					statistic = Statistic.objects.get(store=store,month="May")
					month_name = "May"
				except Exception as e:
					statistic = None
				

				
			elif selected == '6':
				try:
					statistic = Statistic.objects.get(store=store,month="June")
					month_name = "June"
				except Exception as e:
					statistic = None
		

			return	render(request, 'report.html',{'form':form,'month':month_name,'year':year,
				'statistic':statistic,
				'viewer':viewer,
				'viewer_list_per_day':json.dumps(viewer_list_per_day),
				'differ_dates':differ.days})

	month_name="แสดงทั้งหมด"
	return render(request, 'report.html',{'form':form,'month':month_name,'year':year,'store':store,
		'reviews_count':reviews_count,'order_count':order_count,'statistic':stat,
		'viewer':viewer,'viewer_list_per_day':json.dumps(viewer_list_per_day),'differ_dates':differ.days})

def about_us(request):
    collect_session(request,"enter","เกี่ยวกับเรา")
    return render(request, 'about_us.html')

def contact(request):
    collect_session(request,"enter","ติดต่อเรา")
    return render(request, 'contact.html')


@login_required
@csrf_exempt
def delivery(request):


	if request.is_ajax():
		address = request.GET.get('address',False)
		phone_number = request.GET.get('phone_number',False)
		total_price = request.GET.get('total_price',False)
		delivery_charge = request.GET.get('delivery_charge',False)
		code_cou = request.GET.get('code_cou',False)
		

		order = request.GET.get('data',False)
		order = json.loads(order)
		print(address)
		# print("payment ",payment)
		menu_list = []
		amount_list = []
		

		for item in order :
			m = Menu.objects.get(store__id=item['store'],name=item['name'])
			menu_list.append(m.id)
			amount_list.append(item['amount'])
			s = Store.objects.get(id=item['store'])
		
		order = Order.objects.create(user=request.user,
			menu=menu_list,
			store=s,
			amount=amount_list,
			address =address,
			total=total_price,
			phone_number=phone_number,
			delivery_charge=delivery_charge,
			coupon=code_cou)
		

		# str_order += "==================\n"

			# print("order_id : ",order.id)

		next_page = "select-payment"
		return JsonResponse({'next_page':next_page,'order_id':order.id},safe=False)

@login_required
def payment(request,pk):

    try:
        slipForm = SlipPaymentForm()
        o = Order.objects.get(id=pk)
        total = o.total
        store=o.store
        payment_list =[]
        pay = Payment.objects.filter(store=store)
        for p in pay:
            payment_list.append({'method':p.pay})
            if request.method == 'POST':
                slipForm = SlipPaymentForm(request.POST,request.FILES)
                slipForm = SlipPaymentForm(request.POST,request.FILES)
            if "byCash" in request.POST:
                print("Earn")
                slipForm.fields['slip_image'].required = False

            if slipForm.is_valid():
                str_coupon =""
                print("o.coupon",o.coupon)
                if o.coupon !="":
                    try:
                        cou = GetCoupon.objects.get(coupon__code=o.coupon,user=request.user)
                        DisplayHome.objects.create(user=request.user,coupon=cou.coupon)
                        cou.amount -= 1
                        cou.save()
                        code_c = CodeType.objects.get(coupon=cou.coupon)
                        if code_c.code_type == "แถม":
                            str_coupon += code_c.value
                        else:
                            str_coupon += code_c.coupon.msg +" "+code_c.value
                    except :
                        o.coupon =""
                        o.save()
                        sys.exc_clear()
                str_order="===== รายการออร์เดอร์ =====\n"
                payment = ""
                link_slip = ""
                if slipForm.cleaned_data['slip_image'] is None:
                    o.payment_method="จ่ายเงินปลายทาง"
                    o.save()
					# order.update(payment_method="จ่ายเงินปลายทาง")
                    payment="จ่ายเงินปลายทาง"
                else:
                    o.payment_method="พร้อมเพย์"
                    payment="พร้อมเพย์"
                    o.slip_payment = request.FILES['slip_image']
                    o.save()
                    link_slip = "www.ginimm.com/show-slip-"+str(o.id)

                for m,a in zip(o.menu,o.amount):
                    menu =Menu.objects.get(id=m)
                    price = int(a) * menu.price
                    str_order += a+" x "+menu.name+" "+str(price) + " บาท\n"

				# if slipForm.cleaned_data['slip_image'] is None:
				# 	payment = "จ่ายเงินปลายทาง"
					 
				# else:
				# 	payment="พร้อมเพย์"
				# 	order.update(payment_method="พร้อมเพย์")
				# 	o.slip_payment = request.FILES['slip_image']
				# 	o.save()
					# tempIsPromtPay="ชำระเงินแ"
				
                if str_coupon != "":
                    str_order += "ใช้คูปอง" + str_coupon+ " \n"
                str_order += "===================\n"
                str_order += "ค่าจัดส่ง "+ str(o.delivery_charge)+ " บาท\n"
                str_order += "ราคารวม "+ str(o.total)+ " บาท\n"
                str_order += "เบอร์โทรศัพท์ติดต่อ "+o.phone_number +"\n"
                str_order += "ที่อยู่จัดส่ง "+o.address+"\n"
                str_order += "วิธีการชำระเงิน "+payment+"\n"
                str_order += "ขื่อผู้รับ "+request.user.username+"\n"
                if link_slip != "":
                    str_order+= "สามารถดูสลิปโอนเงินได้ที่นี่ "+link_slip
                collect_session(request,"สั่งอาหาร",o.id)
               
                line = LineStore.objects.get(name=store.name)
            
				# line_bot_api.push_message(line.uid, TextSendMessage(text=strdecode))
                # line_bot_api.push_message(line.uid, TextSendMessage(text=strdecode))
                # toey
                # line_bot_api.push_message('U47ea5d1a29927a509fcab4afe475c122', TextSendMessage(text=str_order))
                # # earn
                # line_bot_api.push_message('Ucbb8d9d8af074f86b827b5a55e0b5ded', TextSendMessage(text=str_order))
                next_page = "/success/"+str(pk)
                return HttpResponseRedirect(next_page)

        return render(request, 'payment.html', {'slipForm':slipForm,'store':store,'total':total,'payment_list':payment_list})		
    except Exception as e:
        messages.error(request, e)
        raise Http404()
  
@login_required
def showSlip(request,pk):
	
	try:
		# slipForm = SlipPaymentForm()
		order = Order.objects.get(id=pk)
		image = order.slip_payment.url
		
		
	
		return render(request, 'slip.html', {'order':order,'image':image,})		
	
	except Exception as e:
		messages.error(request, e)
		raise Http404()
	
  


def shop_decision(request,store_name,store_id):
    print("shop_decision")
    try:
        print("toroong")
        Tohrung2.objects.get(store__id=store_id)
        next_page = "/โรงอาหารโต้รุ่ง/"+store_name
        return HttpResponseRedirect(next_page)
    except Exception as e:
        if store_name =="SteakHolder":
            next_page = "/steak-holder/"
        else:
            next_page = "/store/"+str(store_id)+"/"+str(store_name)

        
        return HttpResponseRedirect(next_page)



@login_required
def success(request,order_id):
	return render(request,'delivery.html',{'username':request.user.username,'id':order_id}) 

@login_required
def order_success(request,order_id):
    return render(request,'order_success.html',{'username':request.user.username,'id':order_id})     

@login_required
def order(request):
	orders = Order.objects.filter(user = request.user)
	menu = []
	for o in orders:
		menu.append({"name":o.menu.name,"image":o.menu.image.url})

	return render(request, 'order.html',{'menu':menu})
    

# @login_required
def shop(request, store_id,store_name):
	try:
		
		collect_session(request,"enter_store",store_id)

		reviewForm = ReviewForm()
		# print("name:", string)
		store = Store.objects.get(id=store_id)
		time_status = 0
		delivery = False
		if "delivery" in store.tags :
			delivery = True

			try :
				time = DeliveryTime.objects.get(store=store)
				# print(calendar.day_name[date.today().weekday()])
				day = date.today().weekday()
				time_now = datetime.datetime.now().time()
				time_status = 0
				if day == 0 :# monday

					if time.monday :
						time_open = time.monday_open
						time_close = time.monday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open :
								if time_close < time_open : # ex. close 01.00
									if date.today().weekday() == 1:
										if time_now <= time_close:
											time_status = 1
										else:
											time_status = 0	
									else:
										if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
											time_status = 1
										else:
											time_status = 0
											
											
								else:
									if time_now <= time_close :
										time_status = 1
									else:
										time_status = 0
							else:
								time_status = 0

									


					else :
						time_status = 0
					
				elif day == 1 :# tuesday
					if time.tuesday :
						time_open = time.tuesday_open
						time_close = time.tuesday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open and time_now <= time_close :
								time_status = 1
					else :
						time_status = 0

				elif day == 2:	# wednesday
					if time.wednesday :
						time_open = time.monday_open
						time_close = time.monday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open :
								if time_close < time_open : # ex. close 01.00
									if date.today().weekday() == 3:
										if time_now <= time_close:
											time_status = 1
										else:
											time_status = 0	
									else:
										if time_now <= datetime.time.max: # 23.00 < 23.59.999999 
											time_status = 1
										else:
											time_status = 0	
											
								else:
									if time_now <= time_close :
										time_status = 1
									else:
										time_status = 0
							else:
								time_status = 0
					else :
						time_status = 0
					



				elif day == 3 :# thursday
					if time.thursday :
						time_open = time.thursday_open
						time_close = time.thursday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open and time_now <= time_close :
								time_status = 1
					else :
						time_status = 0
					
				elif day == 4:# friday
					if time.friday :
						time_open = time.friday_open
						time_close = time.friday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open and time_now <= time_close :
								time_status = 1
					else :
						time_status = 0
					
				elif day == 5 :# saturday
					if time.saturday :
						time_open = time.saturday_open
						time_close = time.saturday_close
						if time_open is None and time_close is None:
							time_status = 0
						else :
							if time_now >= time_open and time_now <= time_close :
								time_status = 1
					else :
						time_status = 0
					
				elif day == 6:# sunday
					# print(time.sunday)
					if time.sunday :
						time_open = time.sunday_open
						time_close = time.sunday_close
						# print(time_close)
						# print(time_open)
						if time_open is None and time_close is None:
							time_status = 0
							# print(None)
						else :
							if time_now >= time_open and time_now <= time_close :
								time_status = 1
					else :
						time_status = 0
					# print()
			except :
				pass
				

		cate = store.category
		menues2 =  Menu.objects.filter(store=store).order_by('-id')[:]

		reviews = Review.objects.filter(store=store)

		rate = []
		profile_picture = []
		store_loved_color = None
		if request.user.is_authenticated:
			user = request.user
			store = get_object_or_404(Store, id=store_id)
			if store.likes.filter(id=user.id).exists():
				store_loved_color= True
			else:
				store_loved_color = None

		for i in reviews:
			temp = { 'rating_color': 0,'rating_no_color': 0, }
			temp['rating_color'] = i.rating
			temp['rating_no_color'] = 5 - temp['rating_color']
			rate.append(temp)
			
			try :
				profile_picture.append(Profile.objects.get(user=i.user).picture.url)
			except:
				pass


		out = zip(reviews,rate,profile_picture)
		storecontact = []
		store_contact = StoreContact.objects.filter(store=store)
		for sc in store_contact:
			storecontact.append({'type':sc.contact_type,'contact':sc.contact})



		if request.method == 'POST':
			if "review" in request.POST:
				if request.POST['star'] is  None:
					star = 0;
				else:
					star = request.POST['star']
				# print ("star: ",star)
				reviewForm = ReviewForm(request.POST, request.FILES)
				if reviewForm.is_valid():
					review = Review.objects.create(
			            user = request.user,
			            store = store,
			            comment = reviewForm.cleaned_data['comment'],
			            rating = star,)
					collect_session(request,"รีวิวร้านค้า",review.id)
					DisplayHome.objects.create(user=request.user,review=review)
					next_page = "/store/"+store.name+"/"+str(store_id)
					return HttpResponseRedirect(next_page)
			elif "order" in request.POST:
				print("order post")
				output = []
				total=0.0
				price_per_menu = 0;
				a = {"orderlist": [], "price": [], "url_pic": [], "amount": []}
				for m in menues2:
					# temp = {'name': '', 'url_pic' : '', 'amount': 0,"store":store}
					temp={"name":"","price":0.0,"url_pic":None,"amount":0,"store":0}

					# print("id",m.id)
					# if request.POST.get(str(m.id)) is  None:
					# 	next_page = "/store/"+str(pk)
					# 	return HttpResponseRedirect(next_page)
					# 	# pass

					# else:
					p = Profile.objects.get(user=request.user)
					delivery_address = p.address 
					delivery_phone = p.phone_number
			
						
					a = request.POST.get(str(m.id),0)
					name = Menu.objects.get(id=m.id).name
						# print("earrn")
						# print (name,a)
						
					print("A",a)
					if int(a) > 0:
						print("A in if",a)
							# if " " in m.price:
							# 	size,price= m.price.split(" ")

							# else:
							# 	price = m.price
						temp['name'] = m.name
						temp['url_pic'] = m.image.url
						temp['amount'] = a
						temp['store'] = store.id

						temp['price'] = m.price*int(a)
						total += m.price*int(a)
							
							# output.append(temp)
						output.append(temp)
							# Order.objects.create(user=request.user,menu=m)
						print("go to checkout")

				# print("calculat delivery_charge")			
				delivery_charge = 0.0
				# print("total delivery_charge",total)
				if(store.name == "กินอิ่มนอนอุ่น"):
					if(total < 150.0):
						delivery_charge = store.delivery_payment

					else:
						delivery_charge = 0
				
				total+=delivery_charge
				print("total",total)
				return  render(request,'checkout.html',{'username':request.user.username,'data':json.dumps(output),
					'output':output,'total':total,'delivery_address':delivery_address,
					'delivery_phone':delivery_phone,'store':store,'delivery_charge':delivery_charge})

	except Exception as e:
		pass		
	return render(request,'stores.html',{'reviewForm':reviewForm,'username':request.user.username,'menues':reversed(menues2),'mobile_menues':reversed(menues2),
		'reviews':reviews,'out':out,'store':store,'delivery':delivery,
		'category':cate,'store_loved_color':store_loved_color,
		'time_status':time_status,'storecontact':storecontact})


def searchBycate(request,cate):
    stores_list = []
    stores =[]
    store_love_list =[]

    collect_session(request,"search_cate",cate)
    try :
        if cate == "all":
            stores = Store.objects.all()
        else :
            stores = Store.objects.filter(tags__contains=cate)
        print("stores",stores)
        
        page = request.GET.get('page', 1)

        for s in stores :
            if s.name != "โรงอาหารโต้รุ่ง":
               
                print("stores ",s)
                temp = {'id':'','name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0,
                 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
                # print("temp ",temp)
                temp['name'] = s.name
                temp['id'] = s.id
                tags = s.tags.split(',')
                print("tag ",tags)
                for tag in tags :
                    temp['tags'].append(tag)



                try:
                    Tohrung2.objects.get(store=s)
                    temp['menues'].append(s.image.url)
                    temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()


                        # temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()

                except Tohrung2.DoesNotExist as e:
                    temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()
                    print("no_reviews",temp['no_reviews'])
                    print("count",Review.objects.filter(store__id=s.id).count())

                    menues = Menu.objects.filter(store__id=s.id).order_by('created_at')[:4]
                    for menu in menues:
                        temp['menues'].append(menu.image.url)
              
                try:
                    print("try rating")
                    rating_avg = Review.objects.filter(store__id = s.id).aggregate(Avg('rating'))
                    print("rating_avg",rating_avg)
                    temp['rating_color'] = round(rating_avg['rating__avg'])



                except Exception as e:
                    print("except rating")
                    temp['rating_color'] = 0
                    temp['rating_no_color'] = 5 - temp['rating_color']

                    
                temp['love'] = s.total_likes
                        
                if request.user.is_authenticated:
                    user = request.user
                    store = get_object_or_404(Store, id=s.id)
                    if store.likes.filter(id=user.id).exists():
                        temp['store_loved_color'] = True
                    else:
                        temp['store_loved_color'] = None
                
                print("temp",temp)
                stores_list.append(temp)

        print("============================")
        for i in stores_list:
            print (i)

        paginator = Paginator(stores_list,10)
        try:
            stores = paginator.page(page)
        except PageNotAnInteger:
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)

    except Exception as e:
        pass 


    return render(request, 'search_cate.html',{'stores':stores,'category':cate,})





def searchAll(request):
    stores_list = []
    stores =[]
    store_love_list =[]
    cate = request.POST.get("search", "")

    collect_session(request,'search_input',cate)

    page = request.GET.get('page', 1)


    # collect_session(request,'search_input',cate)
    page = request.GET.get('page', 1)

    if request.method == 'POST':
        if request.POST.get('search') is None:
            return  HttpResponseRedirect('home')
        else:
            print("ddd",request.POST.get('search')) 

        
    

    try :
        # stores = Store.objects.filter(tags__contains=cate)
        print("cate",cate)
        stores= Store.objects.annotate(search=SearchVector('tags', 'name')).filter(search__icontains=cate)

        for s in stores :
            
            if s.name != "โรงอาหารโต้รุ่ง":
               
                print("stores ",s)
                temp = {'id':'','name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0,
                 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
                # print("temp ",temp)
                temp['name'] = s.name
                temp['id'] = s.id
                tags = s.tags.split(',')
                print("tag ",tags)
                for tag in tags :
                    temp['tags'].append(tag)



                try:
                    Tohrung2.objects.get(store=s)
                    temp['menues'].append(s.image.url)
                    temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()


                        # temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()

                except Tohrung2.DoesNotExist as e:
                    temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()
                    print("no_reviews",temp['no_reviews'])
                    print("count",Review.objects.filter(store__id=s.id).count())

                    menues = Menu.objects.filter(store__id=s.id).order_by('created_at')[:4]
                    for menu in menues:
                        temp['menues'].append(menu.image.url)
              
                try:
                    print("try rating")
                    rating_avg = Review.objects.filter(store__id = s.id).aggregate(Avg('rating'))
                    print("rating_avg",rating_avg)
                    temp['rating_color'] = round(rating_avg['rating__avg'])



                except Exception as e:
                    print("except rating")
                    temp['rating_color'] = 0
                    temp['rating_no_color'] = 5 - temp['rating_color']

                    
                temp['love'] = s.total_likes
                        
                if request.user.is_authenticated:
                    user = request.user
                    store = get_object_or_404(Store, id=s.id)
                    if store.likes.filter(id=user.id).exists():
                        temp['store_loved_color'] = True
                    else:
                        temp['store_loved_color'] = None
                
                print("temp",temp)
                stores_list.append(temp)

        paginator = Paginator(stores_list, 10)
        try:
            stores = paginator.page(page)
        except PageNotAnInteger:
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)

    except :
        pass


    return render(request, 'search_input.html',{'stores':stores,'category':cate})



def outofstock(request):
    print("earn")
    store = StoreByUser.objects.get(user = request.user).store
    print(store)
    print(store.quote)
    menulist = Menu.objects.filter(store=store).order_by('-id')[:]

  
    return render(request, 'outofstock.html',{'menues':reversed(menulist),'store':store,'mobile_menues':reversed(menulist)})

def collect_session(request,act,val):
 if request.user.is_authenticated:
 	User_session.objects.create(user=request.user,action=act,value=val)
 else :
 	if 'name' in request.COOKIES:
 		name = request.COOKIES['name']
 		Anonymous_session.objects.create(name=name,action=act,value=val)
 		
@login_required
def fill_in(request):
	# form = InformationsForm()
	# # print(form)
	return render(request, 'informations.html')


@login_required
def fill_in_edit(request):
	try:
		if Informations.objects.filter(user=request.user).exists():
			return render(request, 'informations_complete.html') 
		else :
			return render(request, 'informations.html') 
		
	except Exception as e:
		messages.error(request, e)
		raise Http404()

def calculate_age(day,month,year):
	today = date.today()
	year = int(year)
	month = int(month)
	day = int(day)
	print(type(year))
	return today.year - year - ((today.month, today.day) < (month, day))

@login_required
def fill_in_complete(request):

    if request.method == 'POST':
        collect_session(request,"กรอกประวัติความหิว",request.user)
    
        list_meal = request.POST.getlist('meal')
        if not list_meal :
            print("mobile")
            list_meal = request.POST.getlist('meal-mobile')
            list_reason = request.POST.getlist('reason-mobile')
            list_size = request.POST['size-mobile']
            list_social = request.POST.getlist('social-mobile')
            list_fav = request.POST.getlist('fav-mobile')

        else :
            print("desktop")
            list_meal = request.POST.getlist('meal')
            list_reason = request.POST.getlist('reason')
            list_size = request.POST['size']
            list_social = request.POST.getlist('social')
            list_fav = request.POST.getlist('fav')

        gender = request.POST['sex']
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        salary = request.POST['salary']

        try :

            age = calculate_age(day,month,year)

            if 'bf' in list_meal :
                bf = True
            else :
                bf = False
            if 'lunch' in list_meal :
                lunch = True
            else :
                lunch = False   
            if 'dinner' in list_meal :
                dinner = True
            else :
                dinner = False
            if 'late' in list_meal :
                late = True
            else :
                late = False


            if 'taste' in list_reason :
                taste = True
            else :
                taste = False
            if 'price' in list_reason :
                price = True
            else :
                price = False
            if 'service' in list_reason :
                service = True
            else :
                service = False
            if 'clean' in list_reason :
                clean = True
            else :
                clean = False
            if 'at' in list_reason :
                at = True
            else :
                at = False
            if 'location' in list_reason :
                location = True
            else :
                location = False

                
            if 'facebook' in list_social :
                facebook = True
            else :
                facebook = False
            if 'twitter' in list_social :
                twitter = True
            else :
                twitter = False
            if 'instagram' in list_social :
                instagram = True
            else :
                instagram = False
            if 'line' in list_social :
                line = True
            else :
                line = False


            if 'japan' in list_fav :
                japan = True
            else :
                japan = False
            if 'shabu' in list_fav :
                shabu = True
            else :
                shabu = False
            if 'grill' in list_fav :
                grill = True
            else :
                grill = False
            if 'steak' in list_fav :
                steak = True
            else :
                steak = False
            if 'fastfood' in list_fav :
                fastfood = True
            else :
                fastfood = False
            if 'diet' in list_fav :
                diet = True
            else :
                diet = False
            if 'thai' in list_fav :
                thai = True
            else :
                thai = False
            if 'cake' in list_fav :
                cake = True
            else :
                cake = False
            if 'dessert' in list_fav :
                dessert = True
            else :
                dessert = False
            if 'juice' in list_fav :
                juice = True
            else :
                juice = False
            if 'coffee' in list_fav :
                coffee = True
            else :
                coffee = False


            obj, created = Informations.objects.update_or_create(
                user=request.user, defaults={'age': age,'birthdate':date(year=int(year), month=int(month), day=int(day)),
                'sex':gender,'salary':salary,'size':list_size,'breakfast':bf,'lunch':lunch,'dinner':dinner,'late':late,
                'taste':taste,'price':price,'service':service,'clean':clean,'at':at,'location':location,
                'thai':thai,'diet':diet,'shabu':shabu,'grill':grill,'steak':steak,'fastfood':fastfood,'cake':cake,
                'japanese':japan,
                'dessert':dessert,'coffee':coffee,'juice':juice,'facebook':facebook,'twitter':twitter,'instagram':instagram,'line':line},
            )

            if created :
                dis = DisplayHome.objects.update_or_create(user=request.user,
                    defaults={
                    'information':obj,
                    })

                try:
                    c = Coupon.objects.all()
                    for i in c :
                        if date.today() > i.date_expire:
                            i.delete()

                        GetCoupon.objects.create(user=request.user,coupon=i,amount=i.amount)
                except Exception as e:
                    messages.error(request, e)
                    raise Http404()
    
        except Exception as e:
            messages.error(request, e)
            raise Http404()

        
    
    return render(request, 'informations_complete.html')

def checkIsSell(request):
    print("in checkIsSell")
    if request.method == 'POST':
        user = request.user
        menu_id = request.POST.get('menu_id', None)
        isChecked = request.POST.get('isChecked', None)
        menu = get_object_or_404(Menu, id=menu_id)
        if isChecked == 'true':
        	isChecked=True
        elif isChecked == 'false':
        	isChecked=False
         
        print(menu_id)
        print(menu)

        if isChecked:
            Menu.objects.filter(id=menu_id).update(isSell=isChecked)
        else:
            Menu.objects.filter(id=menu_id).update(isSell=isChecked)

    context = 'success'
    return HttpResponse(json.dumps(context), content_type='application/json')

    
def like_button(request):
    print("earn")
    if request.method == 'POST':
        user = request.user
        sid = request.POST.get('pk', None)
        print(sid)
        store = get_object_or_404(Store, id=int(sid))
        print(store)

        if store.likes.filter(id=user.id).exists():
            store.likes.remove(user)
            u = User_session.objects.get(user=request.user,action="like",value=store.id)
            u.delete()

        else:
            store.likes.add(user)
            collect_session(request,"like",store.id)
    context = {'likes_count': store.total_likes}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def use_coupon(request,coupon):
	try :
		print(coupon)
		c = GetCoupon.objects.get(coupon__id=coupon,user=request.user)

		c.amount -= 1
		c.save()

		cou = Coupon.objects.get(id=coupon)
		DisplayHome.objects.create(user=request.user,coupon=cou)

		collect_session(request,'ใช้คูปอง',coupon)
		
		time = datetime.datetime.now()
		add_time = time + datetime.timedelta(0,3600)

		success_coupon = {'name':cou.store.name,'msg':cou.msg,'image':cou.image,'time':add_time}
	
		return render(request, 'use_coupon.html',{'coupon':success_coupon})
	except Exception as e:
		messages.error(request, e)
		raise Http404()

@login_required
def use_code(request):
    if request.is_ajax():
        c = Coupon.objects.all()
    for i in c :
        if date.today() > i.date_expire:
            i.delete()
    try:

        code = request.GET.get('code',False)
        amount = request.GET.get('amount',False)
        my_dorm = request.GET.get('myDorm',False)
        print (code)
        cou = GetCoupon.objects.get(coupon__code=code,user=request.user)
        if cou.amount <= 0 :
            cou.delete()  
        else :
            output = []
            my_item_in_cart = request.session.get('mycart',[])
            my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}

            isLookchin = False
            isMooping = False
            menu = None
            for m_id,amount in my_dict.items():
                
                
                menu = Menu.objects.get(id=m_id)

                break
            print("menu",menu)
            coupon = cou.coupon
            c = CodeType.objects.get(coupon=coupon)
         
            if c.coupon.store.name == 'โรงอาหารโต้รุ่ง' :

                try :
                    Tohrung2.objects.get(store=menu.store)
                    print("โรงอาหารโต้รุ่ง")

                    if c.code_type == 'ส่วนลด':
                        if c.value =="ค่าส่ง":
                            msg="ส่งฟรี"
                            code_type = 0

                            a = int(amount)
                            if a <=3:
                                if my_dorm =="หอ B":
                                    delivery_charge = 20.0
                                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                                    delivery_charge = 10.0
                                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                                    delivery_charge = 7.0    

                            elif a >=4 and a <=6:
                                if my_dorm =="หอ B":
                                    delivery_charge = 25.0
                                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                                    delivery_charge = 15.0
                                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                                    delivery_charge = 12.0
                            
                            value = delivery_charge
                    elif c.code_type == 'แถม' :
                        code_type = 1
                        msg = 'รับฟรี'
                        value = c.value

                    # print("value",value)
                except :
                    raise
                

            else :
                if c.code_type == 'ส่วนลด':
                    code_type = 0
                    msg = coupon.msg
                    value = float(c.value)
                elif c.code_type == 'แถม' :
                    code_type = 1
                    msg = 'รับฟรี'
                    value = c.value

            collect_session(request,'ใช้โค้ด',coupon.id)
    except Exception as e:
        raise
    return JsonResponse({'code':code_type,'value':value,'msg':msg},safe=False)

@login_required
def st_use_code(request):
    if request.is_ajax():
        c = Coupon.objects.all()
    for i in c :
        if date.today() > i.date_expire:
            i.delete()
    try:

        code = request.GET.get('code',False)
        amount = request.GET.get('amount',False)
        my_dorm = request.GET.get('myDorm',False)
        print (code)
        cou = GetCoupon.objects.get(coupon__code=code,user=request.user)
        if cou.amount <= 0 :
            cou.delete()  
        else :
            output = []
            my_item_in_cart = request.session.get('mycart',[])
            temp_cart = []
            for i in my_item_in_cart:
                if isinstance(i, list):
                    temp_cart.append(tuple(i))
                else:
                    temp_cart.append(i)
            
            # print("my_item_in_cart",my_item_in_cart)
            my_dict = {i:temp_cart.count(i) for i in temp_cart}
            # print("my_dict",my_dict)
              # for m_id,amount in my_dict.items():
            #     temp={"name":"","price":0.0,"amount":0,"menu_id":0,'set':[]}
            #     temp['amount'] = amount
            #     if isinstance(m_id, tuple):
            #         temp_set = {"main":"","side":"","sauce":"","price":0.0,}
          
                
            # my_item_in_cart = request.session.get('mycart',[])
            # my_dict = {i:my_item_in_cart.count(i) for i in my_item_in_cart}

            isLookchin = False
            isMooping = False
            menu = None
            for m_id,amount in my_dict.items():
                try:
                    int(m_id)
                    menu = Menu.objects.get(id=m_id)

                except Exception as e:
                    menu = Menu.objects.get(id=m_id[0])
                
                break
                

                
            print("menu",menu)
            coupon = cou.coupon
            c = CodeType.objects.get(coupon=coupon)
         
            if c.coupon.store.name == 'โรงอาหารโต้รุ่ง' :

                try :
                    Tohrung2.objects.get(store=menu.store)
                    print("โรงอาหารโต้รุ่ง")

                    if c.code_type == 'ส่วนลด':
                        if c.value =="ค่าส่ง":
                            msg="ส่งฟรี"
                            code_type = 0

                            a = int(amount)
                            if a <=3:
                                if my_dorm =="หอ B":
                                    delivery_charge = 20.0
                                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                                    delivery_charge = 10.0
                                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                                    delivery_charge = 7.0    

                            elif a >=4 and a <=6:
                                if my_dorm =="หอ B":
                                    delivery_charge = 25.0
                                elif my_dorm =="หอ C" or my_dorm =="หอ E":
                                    delivery_charge = 15.0
                                elif my_dorm =="หอ F" or my_dorm =="หอ M":
                                    delivery_charge = 12.0
                            
                            value = delivery_charge
                    elif c.code_type == 'แถม' :
                        code_type = 1
                        msg = 'รับฟรี'
                        value = c.value

                    # print("value",value)
                except :
                    raise
                
            elif c.coupon.store.name == "SteakHolder" :
                print("แถมมมม")

                if c.code_type == 'ส่วนลด':
                    if c.value =="ค่าส่ง":
                        msg="ส่งฟรี"
                        code_type = 0

                        a = int(amount)
                        if a <=3:
                            delivery_charge = 25.0   

                        elif a >=4 and a <=6:
                            delivery_charge = 30.0
                                
                            
                        value = delivery_charge
                elif c.code_type == 'แถม' :
                    print("แถมมมม2222")
                    code_type = 1
                    msg = 'รับฟรี'
                    value = c.value

            else :
                if c.code_type == 'ส่วนลด':
                    code_type = 0
                    msg = coupon.msg
                    value = float(c.value)
                elif c.code_type == 'แถม' :
                    code_type = 1
                    msg = 'รับฟรี'
                    value = c.value

            collect_session(request,'ใช้โค้ด',coupon.id)
    except Exception as e:
        raise
    return JsonResponse({'code':code_type,'value':value,'msg':msg},safe=False)


@login_required
def edit_delivery_tr(request,id):
	# s = StoreByUser.objects.get(user=request.user)
    s = Store.objects.get(id=id)
    t= DeliveryTime.objects.get(store=s)

	# time = {'m': t.monday_off,'tu':t.tuesday_off,'w': t.wednesday_off,'th': t.thursday_close,
	# 'f':t.friday_off,'sa':t.saturday_off,'su':t.sunday_off}
    time = [t.monday,t.tuesday,t.wednesday,t.thursday_close,t.friday,t.saturday,t.sunday]
    day = ['วันจันทร์','วันอังคาร','วันพุธ','วันพฤหัสบดี','วันศุกร์','วันเสาร์','วันอาทิตย์']
    index =  [0,1,2,3,4,5,6,]
    list_time = zip(time,day,index)
    return render(request, 'delivery_close_tr.html',{'time':list_time,'name':s.name,'store_id':s.id})

def changeDelivery_tr(request):
    if request.method == 'POST':
        user = request.user
        index = request.POST.get('index', None)
        isChecked = request.POST.get('isChecked', None)
        store_id = request.POST.get('store_id', None)
        if isChecked == 'true':
            checked=True
        elif isChecked == 'false':
            checked=False

        print(checked)
        index = int(index)
        # s = StoreByUser.objects.get(user=request.user)
        s = Store.objects.get(id=store_id)
       
		# print(s.store.name)
        if index == 0 :
            DeliveryTime.objects.filter(store=s).update(monday=checked)
        elif index == 1 :
            DeliveryTime.objects.filter(store=s).update(tuesday=checked)
        elif index == 2 :
            DeliveryTime.objects.filter(store=s).update(wednesday=checked)
        elif index == 3 :
            DeliveryTime.objects.filter(store=s).update(thursday=checked)
        elif index == 4 :
            DeliveryTime.objects.filter(store=s).update(friday=checked)
        elif index == 5 :
            DeliveryTime.objects.filter(store=s).update(saturday=checked)
        elif index == 6 :
            print("55555555")
            DeliveryTime.objects.filter(store=s).update(sunday=checked)

        context = 'success'
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def edit_delivery(request):
    s = StoreByUser.objects.get(user=request.user)
    # s = Store.objects.get(id=id)
    t= DeliveryTime.objects.get(store=s.store)

    # time = {'m': t.monday_off,'tu':t.tuesday_off,'w': t.wednesday_off,'th': t.thursday_close,
    # 'f':t.friday_off,'sa':t.saturday_off,'su':t.sunday_off}
    time = [t.monday,t.tuesday,t.wednesday,t.thursday_close,t.friday,t.saturday,t.sunday]
    day = ['วันจันทร์','วันอังคาร','วันพุธ','วันพฤหัสบดี','วันศุกร์','วันเสาร์','วันอาทิตย์']
    index =  [0,1,2,3,4,5,6,]
    list_time = zip(time,day,index)
    return render(request, 'delivery_close.html',{'time':list_time})

def changeDelivery(request):
    if request.method == 'POST':
        user = request.user
        index = request.POST.get('index', None)
        isChecked = request.POST.get('isChecked', None)
        store_id = request.POST.get('store_id', None)
        if isChecked == 'true':
            checked=True
        elif isChecked == 'false':
            checked=False

        print(checked)
        index = int(index)
        s = StoreByUser.objects.get(user=request.user)
        # s = Store.objects.get(id=store_id)
       
        # print(s.store.name)
        if index == 0 :
            DeliveryTime.objects.filter(store=s.store).update(monday=checked)
        elif index == 1 :
            DeliveryTime.objects.filter(store=s.store).update(tuesday=checked)
        elif index == 2 :
            DeliveryTime.objects.filter(store=s.store).update(wednesday=checked)
        elif index == 3 :
            DeliveryTime.objects.filter(store=s.store).update(thursday=checked)
        elif index == 4 :
            DeliveryTime.objects.filter(store=s.store).update(friday=checked)
        elif index == 5 :
            DeliveryTime.objects.filter(store=s.store).update(saturday=checked)
        elif index == 6 :
            print("55555555")
            DeliveryTime.objects.filter(store=s).update(sunday=checked)

        context = 'success'
    return HttpResponse(json.dumps(context), content_type='application/json')
