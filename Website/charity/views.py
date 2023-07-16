from audioop import reverse
from bson.objectid import ObjectId
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect,render
from django.contrib import messages
import pymongo
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseRedirect
import json
import os
from django.conf import settings
from requests import get
import json
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
usern =None
user= None
try:
    db = pymongo.MongoClient("conecon link")
    print('connected')
except:
    db = None

def image_link(img_name):
    ip = get('https://api.ipify.org').content.decode('utf8')
    dir_path = os.getcwd()
    # dir_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    dir_path = dir_path.replace('/var/www/html', '')
    img_url = "http://" + ip + dir_path + "/media/" + img_name
    return img_url

#login Page
def charity_login(request):
    global user
    if request.method == 'POST':
        #get user from input 
        username =  request.POST.get('username')
        password =  request.POST.get('password')
        print("the value from input in form",username,password) 
        #search on database is user exit
        user = db.get_database().charity.find_one({'username': username})
        if user:
                print(user['password'])
                passW = user['password'].decode("utf-16")
                charity_name = user['name_ar']
                print('charity_name',charity_name,len(charity_name))
                print(password , ":" , passW)
                if (password == passW):
                    request.session['user'] = username
                    print("session",request.session['user'])
                    print("success")
                    if len(charity_name)>0:
                        return redirect('dashboardOld')
                    else:
                        return redirect('dashboardNew')
                else:
                    messages.add_message(request, messages.INFO, 'password is wrong.')
        else:
            #check if admin
            admin = db.get_database().admin.find_one({'username': username})
            if admin:
                print(admin['password'])
                passW = admin['password'].decode("utf-16")
                print('passW',admin['password'])
                if (password == passW):
                    request.session['user'] = username
                    print("session",request.session['user'])
                    print("success")
                    return redirect('AdminDash')        
                else:
                    messages.add_message(request, messages.INFO, 'password is wrong.')
            else:messages.add_message(request, messages.INFO, 'UserName is wrong.')
        

    return render(request,'index.html')


#Dashboard for new user 
def charity_dashboard_new_user(request):
    global user
    if request.session.has_key("user"):
        userN = user['username']
        if request.method == 'POST':
            print('post')
            name_ar =  request.POST.get('namear')
            name_en =  request.POST.get('nameen')
            city =  request.POST.get('city')
            email =  request.POST.get('email')
            web =  request.POST.get('web')
            phone =  request.POST.get('phone')
            
            try:
                upload_img = request.FILES['img']
                fss = FileSystemStorage()
                file = fss.save(upload_img.name, upload_img)
                file_url = fss.url(file)
                print('logo',file_url)
            except: file_url =''
            myquery = { "username": userN}
            newvalues = { "$set": { "name_ar": name_ar, "name_en": name_en,'logo':file_url,'city':city,'email':email,'web':web,'phone':phone}}
            db.get_database().charity.update_one(myquery, newvalues)
            user = db.get_database().charity.find_one({'username': userN})
            return redirect('zakahTypes')
    else:
        return redirect('login')
          
    context={'username':userN}
    print('usern',context)
    return render(request,'dashboard_new_user.html',context)


#Add ZakahTypes
def ADDZakahTypes(request):
    global user
    print('the ',user)
    if request.session.has_key("user"):
        userN = user['username']
        logo = user['logo']
        charity_id = user['_id']
        print('image',logo)
        types=db.get_database().all_types.find()
        print('the_types',types[0])
        list_type = list(types)
        print('the_types',list_type)
       
        if request.method == 'POST':
            types_list_form=request.POST.getlist('zakah')
            print('type_from_form',types_list_form)
            for type_list in types_list_form:
               type_one_object = type_list
               type_en = type_one_object.split(",")[0]
               type_ar= type_one_object.split(",")[1]
               print('type_one',type_one_object)
               print('type_en',type_en)
               print('type_ar',type_ar)
               check_type_en = db.get_database().types.find_one({'type_en': type_en,'charity_id': charity_id})
               if not check_type_en:
                   Collection = { "type_ar": type_ar, "type_en": type_en,"charity_id":charity_id}
                   db.get_database().types.insert_one(Collection)
            return redirect('dashboardOld')
    else:
        return redirect('login')
    context = {
    'types':list_type,
    'username':userN,
    'logo':logo,
    }
    return render(request,'AddZakahTypes.html',context)


#Dashboard for old user 
def charity_dashboard_old_user(request):
    global user, db
    print('the ',user)
    today = datetime.datetime.now()
    this_year = today.year
    last_ten_years = this_year - 11
    print('year',this_year,'last_ten_years',last_ten_years)
    YEAR_CHOICES = []
    for r in range(this_year, last_ten_years, -1):
        YEAR_CHOICES.append((r))
    print('YEAR_CHOICES',YEAR_CHOICES)
    Oman_Cities = ["مسقط","مطرح","بوشر","السيب","العامرات","قريات","الخابورة","صحم"
    ,"صحار","لوى","شناص","السويق","بركاء","الرستاق","العوابي","المصنعة","وادى المعاول","نخل",
    "سمائل","بدبد","نزوي","الحمراء","بهلاء","إزكي","عبري","البريمي","صور","خصب"
    ]
    sum = 0
    sumRound = 0
    Donate_Num = 0
    OneDay_tarns_Num = []
    Onemonth_tarns_Num = []
    Oneyear_tarns_Num = []
    context = {}
    donation_by_type = []
  
    # if (user): 
    if request.session.has_key("user"):
            print('request.session.has_key("user")')
            userN = user['username']
            logo = user['logo']
            charity_id = user['_id']
            print("charity_id",charity_id)
            charity_name = user['name_ar']
            charity_city = user['city']
            charit_types=db.get_database().types.find({'charity_id': charity_id})
            charit_types_list =list(charit_types)
            charity_device =db.get_database().devices.find({'charity_id': charity_id})
            charity_device_list =list(charity_device)
            print('charity_device_list',charity_device_list)
            #find device_id related to charity_id
            Donate_Num = 0
            devs_list = []
            if (len(charity_device_list)>0):
                for Dev_ID in charity_device_list:
                    device_ID = Dev_ID['_id']
                    Dev_ID['id'] = device_ID
                    devs_list.append(Dev_ID)
                    print("device_ID",device_ID)
                    #find transaction related to device_ID
                    Device_trans_list = list(db.get_database().transactions.find({'device_id': device_ID}))
                    # donate_num = 0
                    # #find total amount of donate
                    # for amount in Device_trans_list:
                    #     device_money = int(amount['money'])
                    #     type = amount['type']
                    #     if (device_money>0):
                    #         print('device_money',device_money)
                    #         sum = sum + device_money
                    #         donate_num += 1
                    #         type_found = False
                    #         for item in donation_by_type:
                    #             if item['type'] == type:
                    #                 item['money'] += device_money
                    #                 type_found = True
                    #                 break
                    #         if not type_found:
                    #             findstype = list(db.get_database().charity_subtypes.find({'_id': type}))
                    #             for stype in findstype:
                    #                 print('findtype',stype['sub_type_ar'])
                    #                 donation_by_type.append({'type': stype['sub_type_ar'], 'money': '{:.3f}'.format(device_money)})
                           
                    # Donate_Num += donate_num
                    # sumRound = '{:.3f}'.format(sum)
                    # print("sum",sumRound)
                    # print('charit_types: ',charit_types_list)
                    # print('charity_device_list: ',charity_device_list)
                    # print('Device_trans_list: ',Device_trans_list)
                    # print('Donate_Num: ',Donate_Num)
                  

                    # #CAll oneDay_Statistics Function 
                    # OneDay_tarns_Num.append(oneDay_Statistics(device_ID))
                    # print('one_DayStatistics_list',OneDay_tarns_Num)
                    # #CAll oneMonth_Statistics Function 
                    # Onemonth_tarns_Num.append(oneMonth_Statistics(device_ID))
                    # print('one_monthStatistics_list',Onemonth_tarns_Num)
                    # #CAll oneYear_Statistics Function 
                    # Oneyear_tarns_Num.append(oneYear_Statistics(device_ID))
                    # print('one_yearStatistics_list',Oneyear_tarns_Num)

                OneDay_tarns_Num = oneDay_Statistics_all(charity_device_list)
                Onemonth_tarns_Num = oneMonth_Statistics_all(charity_device_list)
                Oneyear_tarns_Num = oneYear_Statistics_all(charity_device_list)
                donation_by_typeName, donation_Count, total_sum = findStatisticsDetails4AllDev(charity_device_list)
                # find_types = findStatisticsDetails4AllDev(charity_device_list)
                # print('find_types',find_types)
             
                    
                if request.method == "GET":
                    try:
                        myDates=  request.GET.get('myJSONData')
                        month = request.GET.get('month')
                        year_from_user = request.GET.get('year')
                    
                        if myDates:
                            print('myDates outside fun',myDates)
                            #convert json to list
                            data  = json.loads(myDates)
                            date_1 = data[0]
                            date_2 = data[1]
                            print("type",type(date_1),date_1,"date_2",date_2)
                            print("data",data,type(data))
                            print(data)
                            converDate_1 = datetime.datetime.strptime(date_1, "%Y-%m-%d")                       
                            converDate_2 = datetime.datetime.strptime(date_2, "%Y-%m-%d")
                            filter_num, filter_sum = find_Statistics_2Dates_AllDev(converDate_1,converDate_2,charity_device_list)
                            return JsonResponse({'filter_num':filter_num,'filter_sum':filter_sum})
                            # Device_2Dates = find_Statistics_2Dates_AllDev(converDate_1,converDate_2,charity_device_list)
                            # print('Device_2Dates',Device_2Dates)
                            # print('converDate_1',converDate_1,type(converDate_1))
                            # print('converDate_2',converDate_2,type(converDate_2))
                            # print('device_ID for year and month',device_ID,type(device_ID))
                            # Device_2Dates = list(db.get_database().transactions.find(
                            # {"datetime": {"$gte":converDate_1, "$lt":converDate_2},
                            # 'device_id': ObjectId(device_ID)}
                            # ))
                            # print('Device_2Dates',Device_2Dates)
                            # filter_num = len(Device_2Dates)
                            # print('Device_2Dates',Device_2Dates)
                            # print('filter_num between 2 dates',filter_num)
                            # sum =0
                            # for amounts in Device_2Dates:
                            #     device2day_money = amounts['money']
                            #     print('device_money',device2day_money)
                            #     sum = sum + device2day_money
                            # filter_sum = '{:.3f}'.format(sum)
                            # print('filter_sum 2 cal date',filter_sum)
                            # return JsonResponse({'filter_num':filter_num,'filter_sum':filter_sum})
                        #if month from user
                        if month and year_from_user:
                            print('month year before fun')
                            filter_num, filter_sum = find_Statistics_monthYear_AllDev(month,year_from_user,charity_device_list)
                            return JsonResponse({'filter_num':filter_num,'filter_sum':filter_sum})
                            # print('year_from_user',month,year_from_user)
                            # if month == '12':
                            #     start_Month_Yearstring = year_from_user + "-" + month  + "-01"  + " 00:00:00"
                            #     #year-01-01
                            #     end_Month_Yearstring = year_from_user + "-01-01"   + " 00:00:00"
                            #     print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
                            #     print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
                            # else:
                            #     start_Month_Yearstring = year_from_user + "-" +month  + "-01"  + " 00:00:00"
                            #     #year-01-01
                            #     end_Month_Yearstring = year_from_user + "-"+str(int(month)+1) + "-01"   + " 00:00:00"

                            # print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
                            # print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
                            # start_Month_Year_gth = parse_datetime(start_Month_Yearstring)
                            # end_Month_Year_lth = parse_datetime(end_Month_Yearstring)    
                            # print('start_Month_Year_gth',start_Month_Year_gth,type(start_Month_Year_gth))
                            # print('end_Month_Year_lth',end_Month_Year_lth,type(end_Month_Year_lth))
                            # Device_Month_Year = list(db.get_database().transactions.find(
                            #     {"datetime": {"$gte":start_Month_Year_gth, "$lt":end_Month_Year_lth},
                            #     'device_id': device_ID}
                            # ))
                            # Device_Month_Year_num = len(Device_Month_Year)
                            # print('Device_Month_Year_num',Device_Month_Year_num)
                           
                            # Month_Year_sum =0
                            # for Month_Year_amounts in Device_Month_Year:
                            #     deviceMonth_year_money = Month_Year_amounts['money']
                            #     print('deviceMonth_year_money',deviceMonth_year_money)
                            #     Month_Year_sum = Month_Year_sum + deviceMonth_year_money
                            # sum_Month_year_Round = '{:.3f}'.format(Month_Year_sum)
                            # return JsonResponse({'filter_num':Device_Month_Year_num,'filter_sum':sum_Month_year_Round})
                        # elif month:
                        #     print("month",type(month),month)
                        #     if month == '12':
                        #         #year-12-01
                        #         start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                        #         #year-01-01
                        #         end_string = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                                
                        #     else:
                        #         #year-12-01
                        #         start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                        #         #year-01-01
                        #         end_string = str(this_year)+ "-" + str(int(month)+1) + "-01"   + " 00:00:00"
                        #     print('start_string',start_string,type(start_string))
                        #     print('end_string',end_string,type(end_string))
                        #     start_month_gth = parse_datetime(start_string)
                        #     end_month_lth = parse_datetime(end_string)
                        #     print('start_month_gth',start_month_gth,type(start_month_gth))
                        #     print('end_month_lth',end_month_lth,type(end_month_lth))
                        #         #dataBase
                        #     Device_month = list(db.get_database().transactions.find(
                        #         {"datetime": {"$gte":start_month_gth, "$lt":end_month_lth},
                        #         'device_id': device_ID}
                        #     ))
                        #     Device_month_num = len(Device_month)
                        #     print('Device_month_num',Device_month_num)
                           
                        #     month_sum =0
                        #     for month_amounts in Device_month:
                        #         devicemonth_money = month_amounts['money']
                        #         print('devicemonth_money',devicemonth_money)
                        #         month_sum = month_sum + devicemonth_money
                        #     sum_Month_Round = '{:.3f}'.format(month_sum)
                        #     return JsonResponse({'filter_num':Device_month_num,'filter_sum':sum_Month_Round})
                        #     #if year from user
                        # elif year_from_user:
                        #         print("year_from_user",type(year_from_user),year_from_user)
                        #         start_Yearstring = year_from_user + "-01"  + "-01"   + " 00:00:00"
                        #         #year-01-01
                        #         end_Yearstring = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                        #         print('start_Yearstring',start_Yearstring,type(start_Yearstring))
                        #         print('end_Yearstring',end_Yearstring,type(end_Yearstring))
                        #         start_Year_gth = parse_datetime(start_Yearstring)
                        #         end_Year_lth = parse_datetime(end_Yearstring)
                        #         print('start_Year_gth',start_Year_gth,type(start_Year_gth))
                        #         print('end_Year_lth',end_Year_lth,type(end_Year_lth))
                        #         Device_Year = list(db.get_database().transactions.find(
                        #         {"datetime": {"$gte":start_Year_gth, "$lt":end_Year_lth},
                        #         'device_id': device_ID}
                        #         ))
                        #         Device_Year_num = len(Device_Year)
                        #         print('Device_Year_num',Device_Year_num)
                           
                        #         Year_sum =0
                        #         for Year_amounts in Device_Year:
                        #             deviceyear_money = Year_amounts['money']
                        #             print('deviceyear_money',deviceyear_money)
                        #             year_sum = Year_sum + deviceyear_money
                        #         sum_year_Round = '{:.3f}'.format(year_sum)
                        #         return JsonResponse({'filter_num':Device_Year_num,'filter_sum':sum_year_Round})
                        
                        
                                
                    except Exception as e:
                        print(e)
    else:
            return redirect('login')
    print('donation_by_type: ',donation_by_type)        
    context = {
        'username':userN,
        'logo':logo,
        'charity_id':charity_id,
        'charity_name':charity_name,
        'charity_city':charity_city,
        'charit_types_list':charit_types_list,
        'charity_device_list':devs_list,
        'sum':total_sum,
        'Donate_Num':donation_Count,
        'OneDay_tarns_Num':OneDay_tarns_Num,
        'Onemonth_tarns_Num':Onemonth_tarns_Num,
        'Oneyear_tarns_Num':Oneyear_tarns_Num,
        'YEAR_CHOICES':YEAR_CHOICES,
        'Oman_Cities':Oman_Cities,
        'donation_by_type': donation_by_typeName
       
        }

    return render(request,'dashboard_old_user.html',context)


#Display Device from charity side
def display_device_4charity(request):
    sum = 0
    money =0
    round =0
    num_of_trans =0
    check_name = 0
    all_dev_4Char = []
    global user, db
    print('the ',user)
    if request.session.has_key("user"):
        print('request.session.has_key("user")')
        charity_id = user['_id']
        #if update 
        if request.method == "GET":
            devid= request.GET.get('devid')
            newdevname= request.GET.get('NewdevName')
            print('newdevname',newdevname)
            city= request.GET.get('city')
            address= request.GET.get('address')
            print('devid from button',devid)
            # if newdevname:
            #     Name_IsExit= db.get_database().devices.find({'name': newdevname})
            #     if Name_IsExit:
            #         for n in Name_IsExit:
            #             print("n['_id']",n['_id'])
            #             if n['_id'] != devid:
            #                 print('dev found')
            #                 check_name = 1
                # if Name_IsExit:
                #     checkId= Name_IsExit['name']
                #     print('checkId',checkId)
                #     # if checkId !=devid:
                #     print('dev found')
                #     check_name = 1
                        # else:
                            # print('else')
            myquery = { "_id": ObjectId(devid)}
            if  newdevname:
                Name_IsExit= db.get_database().devices.find({'name': newdevname})
                print('Name_IsExit',Name_IsExit)
                if Name_IsExit:
                    newvalues =  {"$set": {'name': newdevname}}
                    db.get_database().devices.update_one(myquery,newvalues)
                    check_name = 1
            if  city:
                newvalues =  {"$set": {'city':city}}
                db.get_database().devices.update_one(myquery,newvalues)
                check_name = 1
            if  address:
                newvalues =  {"$set": {"address": address}}
                db.get_database().devices.update_one(myquery,newvalues)
                check_name = 1
           
            # check_name = 0
        #Display Device 
        All_dev = list(db.get_database().devices.find({'charity_id': charity_id}))
        for dev in  All_dev:
            devId = dev['_id']
            name =dev['name']
            password =dev['password']
            mac =dev['mac']
            status =dev['status']
            charity_id =dev['charity_id']
            start_date =dev['start_date']
            last_maintenance =dev['last_maintenance']
            next_maintenance = dev.get('next_maintenance', "")
            # next_maintenance =dev['next_maintenance']
            print('next_maintenance',next_maintenance)
            Device_serial =dev['Device_serial']
            if 'city' in dev:
                city = dev['city']
                print("Present, city =",city)
            else:
                city = ""
                print("Not present city")
            if 'address' in dev:
                address = dev['address']
                print("Present, address =",address)
            else:
                address = ""
                print("Not present city")
            
           
            trans4Dev = list(db.get_database().transactions.find({'device_id': devId}))
            # num_of_trans = len(trans4Dev)
            sum = 0
            round =0
            num_of_trans =0
            print("check sum",sum,round,num_of_trans)
            for trans in trans4Dev:
                money = int(trans['money'])
                sum = sum + money
                round ='{:.3f}'.format(sum)
                num_of_trans+=1
                # translist.append({'num_of_trans':num_of_trans,'sum':round})
            all_dev_4Char.append({'devId':str(devId),'name':name,'password':password,'mac':mac,
            'status':status,'charity_id':str(charity_id),'start_date':start_date,
            'last_maintenance':last_maintenance,'next_maintenance':next_maintenance,'Device_serial':Device_serial,'city':city,'address':address,
            'num_of_trans':num_of_trans,'sum':round,'check_name':check_name})
            
            # totalList = all_dev_4Char + translist
        print('all_dev_4Char',all_dev_4Char)
        return JsonResponse({'all_dev_4Char':all_dev_4Char})
                     
    else:
        return redirect('login')



#Edit charity Profile
def charity_profile(request):
    global user
    print('the ',user)
    if request.session.has_key("user"):
        print('request.session.has_key("user")')
        userN = user['username']
        logo = user['logo']
        charity_id = user['_id']
        charity_name_ar = user['name_ar']
        charity_name_en= user['name_en']
        charity_city = user['city']
        charity_email= user['email']
        charity_web= user['website']
        charity_phone= user['phone']
        charity_password= user['password'].decode("utf_16")
        if request.method == 'POST':
            print('post')
            name_ar =  request.POST.get('namear')
            name_en =  request.POST.get('nameen')
            passW   =  request.POST.get('pass').encode("utf_16")
            city    =  request.POST.get('city')
            email   =  request.POST.get('email')
            web     =  request.POST.get('web')
            phone   =  request.POST.get('phone')
            print("passW",passW,name_ar,userN)
            file_url = None
            # try:# try take upload image take it 
            try:
                upload_img = request.FILES['img']
                print("upload_img",upload_img)
                fss = FileSystemStorage()
                fullname = os.path.join(settings.MEDIA_ROOT,str(upload_img))
                print("fullname",fullname)
                if os.path.exists(fullname):
                    os.remove(fullname)
                    print("image exits")
                file = fss.save(upload_img.name, upload_img)
                file_url = fss.url(file)
                print('logo',file_url)
            except: file_url ='' 
            myquery = { "username": userN,"_id":charity_id}
            newvalues = { "$set": {"password":passW,"name_en":name_en,"name_ar": name_ar,"city":city,"website":web,"phone":phone,"email":email}}
            try:
                img_url = image_link(str(upload_img))
                print(img_url)
                if (img_url): 
                    newvalues['$set']['logo'] = img_url#if user upload image take it 
            except:pass
            print("new data: ",newvalues)
            db.get_database().charity.update_one(myquery,newvalues)
            print('update')
            user = db.get_database().charity.find_one({'username':userN})
            return redirect('dashboardOld')
    else:
            return redirect('login')
    context = {
        'username':userN,
        'logo':logo,
        'charity_name_en':charity_name_en,
        'charity_name_ar':charity_name_ar,
        'charity_city':charity_city,
        'charity_password':charity_password,
        'charity_email':charity_email,
        'charity_web':charity_web,
        'charity_phone':charity_phone
        }

    return render(request,'charity_profile.html',context)

#delete item from types collection
def delete_zakah_type(request):
    global user
    print('the',user)
    if request.session.has_key("user"): 
        charity_id = user['_id']
        if request.method == 'GET':  
            type_name = request.GET.get('type_name')  
            print('type_name for charity 2 delete',type_name)
            find_Type_ID=list(db.get_database().types.find({"type_en":type_name}))
            for type_id in find_Type_ID:
                   type_id = type_id['type_id']
            print('type_id for charity 2 delete',type_id)
            subtypequery = { "charity_id": charity_id,"type_id":type_id}
            deletsub = db.get_database().charity_subtypes.delete_many(subtypequery)
            print("deletsub: " , deletsub.deleted_count)
            myquery = { "charity_id": charity_id,"type_en":type_name}
            print(myquery)
            print(type(charity_id))
            res = db.get_database().types.delete_one(myquery)
            print("res: " , res.deleted_count)
            db.get_database().types.find({'charity_id': charity_id})
            return redirect('dashboardOld')
    else:
        return redirect('login')


#delete item from types collection
def ADD_zakah_type(request):
    global user
    choose_types = []
    if request.session.has_key("user"):  
        charity_id = user['_id']
        charit_types=db.get_database().types.find({'charity_id': charity_id})
        charit_types_list = list(charit_types)
        All_types=db.get_database().all_types.find()
        All_types_list = list(All_types)
        print("All_types",All_types_list)
        print("charit_types_list",charit_types_list)
        #add all types in all_types table except types in types table in list
        for _types in All_types_list:
            Found = False
            for char_type in charit_types_list:
                if char_type ['type_en'].strip() == _types ['name_en'].strip() :
                    Found = True
                    print(Found)
            if(not Found ):
                choose_types.append({'type_id':str(_types['_id']),'name_en':_types['name_en'],'name_ar':_types['name_ar']})

        if request.method == "GET":
            checkbox_types = request.GET.get('myCheckboxes')
            print("checkbox_types",checkbox_types)
            if (checkbox_types):
                L = checkbox_types.strip("][").replace("\"", "").split(",")
                print(L)
                for type_list in L:
                    type_en = type_list.split(":")[0]
                    type_ar= type_list.split(":")[1]
                    type_id= type_list.split(":")[2]
                    print('type_en',type_en)
                    print('type_ar',type_ar)
                    check_type_en = db.get_database().types.find_one({'type_en': type_en,'charity_id': charity_id})
                    if not check_type_en:
                        Collection = {'type_id':type_id,"type_ar": type_ar, "type_en": type_en,"charity_id":charity_id}
                        db.get_database().types.insert_one(Collection)
                        return redirect('dashboardOld')

        print("choose_types",choose_types)
        return JsonResponse({'choose_types':choose_types})
    else:
        return redirect('login')


#Daily Statistics
def oneDay_Statistics_all(Devs_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    #Get Statistics for one day
    oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-" + str(dt.day) + " 00:00:00" 
    oneDay_GreaterThan_convertDate = parse_datetime(oneDay_GreaterThan)
    oneDay_LessThan = str(dt.year) + "-" +  str(dt.month) + "-" + str(dt.day) + " 23:59:59" 
   
    oneDay_LessThan_convertDate = parse_datetime(oneDay_LessThan)
    print('oneDay_GreaterThan',oneDay_GreaterThan)
    print('oneDay_LessThan',oneDay_LessThan)
    print('typeof',type(oneDay_GreaterThan_convertDate))
    # print("Dev_Id: " , Dev_Id)
    sumRound = 0
    OneDay_tarns_Num = 0
    for Dev_Id in Devs_Id:
        Device_OneDaytrans = list(db.get_database().transactions.find(
            {"datetime": {"$gte": oneDay_GreaterThan_convertDate, "$lte": oneDay_LessThan_convertDate},
            'device_id': Dev_Id['_id']}
            ))
        # OneDay_tarns_Num = len(Device_OneDaytrans)
        dev_day_num = 0
        for amount in Device_OneDaytrans:
            _money = int(amount['money'])
            if (_money>0):
                print('device_money',_money)
                sum = sum + _money
                dev_day_num += 1
        # sumRound = '{:.3f}'.format(sum)
        # print("sum",sumRound)
        OneDay_tarns_Num += dev_day_num
        print('Device_OneDaytrans: ',Device_OneDaytrans)
    
    sumRound = '{:.3f}'.format(sum)
    returnValue = [OneDay_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)  


#Monthly Statistics
def oneMonth_Statistics_all(Devs_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    check_month = dt.month
    print('check_month',check_month)
    #if month equal 12 increase year and make month  equal 1
    if check_month == 12:
         #Get Statistics for one day
        onemonth_GreaterThan = str(dt.year) + "-"  +  str(dt.month) + "-" + str(dt.day)  + " 00:00:00"
        oneMonth_LessThan = str(dt.year+1) + "-01-01" + " 00:00:00"
    else:
        onemonth_GreaterThan = str(dt.year) + "-"  +  str(dt.month) + "-" + str(dt.day)  + " 00:00:00"
        oneMonth_LessThan = str(dt.year) + "-" + str(dt.month+1) + "-" + str(dt.day) + " 00:00:00"

    # oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-01 00:00:00" 
    oneMonth_GreaterThan_convertDate = parse_datetime(onemonth_GreaterThan)
    # oneDay_LessThan = str(dt.year) + "-" +  str(dt.month-1) + "-01 00:00:00"
    onMonth_LessThan_convertDate = parse_datetime(oneMonth_LessThan)
    print('onemonth_GreaterThan',onemonth_GreaterThan)
    print('oneMonth_LessThan',oneMonth_LessThan)
    print('typeof',type(oneMonth_GreaterThan_convertDate),type(onMonth_LessThan_convertDate))
    
    sum = 0
    OneMonth_tarns_Num = 0
    for Dev_Id in Devs_Id:
        Device_OneMonthtrans = list(db.get_database().transactions.find(
            {"datetime": {"$gte": oneMonth_GreaterThan_convertDate, "$lt": onMonth_LessThan_convertDate},
            'device_id': Dev_Id['_id']}
            ))
        
        dev_month_num = 0
        for amount in Device_OneMonthtrans:
            _money = int(amount['money'])
            if (_money>0):
                print('device_money',_money)
                sum = sum + _money
                dev_month_num += 1
        OneMonth_tarns_Num += dev_month_num

    sumRound = '{:.3f}'.format(sum)
    print("sum",sumRound)
    print('Device_OneMonthtrans: ',Device_OneMonthtrans)
    returnValue = [OneMonth_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)   


#Yearly Statistics 
def oneYear_Statistics_all(Devs_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    check_month = dt.month
    print('check_month',check_month)
    oneYear_GreaterThan = str(dt.year) + "-01-01" + " 00:00:00"
    oneYear_LessThan = str(dt.year) + "-12-31" + " 23:59:59"

    # oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-01 00:00:00" 
    oneYear_GreaterThan_convertDate = parse_datetime(oneYear_GreaterThan)
    # oneDay_LessThan = str(dt.year) + "-" +  str(dt.month-1) + "-01 00:00:00"
    onYear_LessThan_convertDate = parse_datetime(oneYear_LessThan)
    print('oneYear_GreaterThan',oneYear_GreaterThan)
    print('oneYear_LessThan',oneYear_LessThan)
    print('typeof',type(oneYear_GreaterThan_convertDate),type(onYear_LessThan_convertDate))

    sum = 0
    OneYear_tarns_Num = 0
    for Dev_Id in Devs_Id:
        Device_OneYeartrans = list(db.get_database().transactions.find(
            {"datetime": {"$gte": oneYear_GreaterThan_convertDate, "$lte": onYear_LessThan_convertDate},
            'device_id': Dev_Id['_id']}
            ))
        
        dev_year_num = 0
        for amount in Device_OneYeartrans:
            _money = int(amount['money'])
            if (_money>0):
                print('device_money',_money)
                sum = sum + _money
                dev_year_num += 1
        OneYear_tarns_Num += dev_year_num

    sumRound = '{:.3f}'.format(sum)
    print("sum",sumRound)
    print('Device_OneYeartrans: ',Device_OneYeartrans)
    returnValue = [OneYear_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)  


#Daily Statistics
def oneDay_Statistics(Dev_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    #Get Statistics for one day
    oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-" + str(dt.day) + " 00:00:00" 
    oneDay_GreaterThan_convertDate = parse_datetime(oneDay_GreaterThan)
    oneDay_LessThan = str(dt.year) + "-" +  str(dt.month) + "-" + str(dt.day) + " 23:59:59" 
   
    oneDay_LessThan_convertDate = parse_datetime(oneDay_LessThan)
    print('oneDay_GreaterThan',oneDay_GreaterThan)
    print('oneDay_LessThan',oneDay_LessThan)
    print('typeof',type(oneDay_GreaterThan_convertDate))
    print("Dev_Id: " ,type(Dev_Id),Dev_Id)
    Device_OneDaytrans = list(db.get_database().transactions.find(
        {"datetime": {"$gte": oneDay_GreaterThan_convertDate, "$lte": oneDay_LessThan_convertDate},
        'device_id': ObjectId(Dev_Id)}
        ))
    # OneDay_tarns_Num = len(Device_OneDaytrans)
    for amount in Device_OneDaytrans:
        _money = amount['money']
        print('device_money',_money)
        sum = sum + int(_money)
    sumRound = '{:.3f}'.format(sum)
    print("sum",sumRound)
    print('Device_OneDaytrans: ',Device_OneDaytrans)
    OneDay_tarns_Num = len(Device_OneDaytrans)
    returnValue = [OneDay_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)   

#Monthly Statistics
def oneMonth_Statistics(Dev_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    check_month = dt.month
    print('check_month',check_month)
    #if month equal 12 increase year and make month  equal 1
    if check_month == 12:
         #Get Statistics for one day
        onemonth_GreaterThan = str(dt.year) + "-"  +  str(dt.month) + "-" + str(dt.day)  + " 00:00:00"
        oneMonth_LessThan = str(dt.year+1) + "-01-01" + " 00:00:00"
    else:
        onemonth_GreaterThan = str(dt.year) + "-"  +  str(dt.month) + "-" + str(dt.day)  + " 00:00:00"
        oneMonth_LessThan = str(dt.year) + "-" + str(dt.month+1) + "-" + str(dt.day) + " 00:00:00"

    # oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-01 00:00:00" 
    oneMonth_GreaterThan_convertDate = parse_datetime(onemonth_GreaterThan)
    # oneDay_LessThan = str(dt.year) + "-" +  str(dt.month-1) + "-01 00:00:00"
    onMonth_LessThan_convertDate = parse_datetime(oneMonth_LessThan)
    print('onemonth_GreaterThan',onemonth_GreaterThan)
    print('oneMonth_LessThan',oneMonth_LessThan)
    print('typeof',type(oneMonth_GreaterThan_convertDate),type(onMonth_LessThan_convertDate))
    Device_OneMonthtrans = list(db.get_database().transactions.find(
        {"datetime": {"$gte": oneMonth_GreaterThan_convertDate, "$lt": onMonth_LessThan_convertDate},
        'device_id': ObjectId(Dev_Id)}
        ))
    OneMonth_tarns_Num = len(Device_OneMonthtrans)
    for amount in Device_OneMonthtrans:
        _money = amount['money']
        print('device_money',_money)
        sum = sum + int(_money)
    sumRound = '{:.3f}'.format(sum)
    print("sum",sumRound)
    print('Device_OneMonthtrans: ',Device_OneMonthtrans)
    returnValue = [OneMonth_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)   


#Yearly Statistics 
def oneYear_Statistics(Dev_Id):
    sum = 0
    #Get today Date
    dt = datetime.datetime.now()
    check_month = dt.month
    print('check_month',check_month)
    oneYear_GreaterThan = str(dt.year) + "-01-01" + " 00:00:00"
    oneYear_LessThan = str(dt.year) + "-12-31" + " 23:59:59"

    # oneDay_GreaterThan = str(dt.year) + "-" +  str(dt.month) + "-01 00:00:00" 
    oneYear_GreaterThan_convertDate = parse_datetime(oneYear_GreaterThan)
    # oneDay_LessThan = str(dt.year) + "-" +  str(dt.month-1) + "-01 00:00:00"
    onYear_LessThan_convertDate = parse_datetime(oneYear_LessThan)
    print('oneYear_GreaterThan',oneYear_GreaterThan)
    print('oneYear_LessThan',oneYear_LessThan)
    print('typeof',type(oneYear_GreaterThan_convertDate),type(onYear_LessThan_convertDate))
    Device_OneYeartrans = list(db.get_database().transactions.find(
        {"datetime": {"$gte": oneYear_GreaterThan_convertDate, "$lte": onYear_LessThan_convertDate},
        'device_id': ObjectId(Dev_Id)}
        ))
    OneYear_tarns_Num = len(Device_OneYeartrans)
    for amount in Device_OneYeartrans:
        _money = amount['money']
        print('device_money',_money)
        sum = sum + int(_money)
    sumRound = '{:.3f}'.format(sum)
    print("sum",sumRound)
    print('Device_OneYeartrans: ',Device_OneYeartrans)
    returnValue = [OneYear_tarns_Num,"عدد المعاملات",sumRound,"مجموع التبرعات"]
    print('returnValue: ',returnValue)
    return(returnValue)  


    

#AdminDashboard 
def AdminDashboard(request):
    if request.session.has_key("user"): 
        userAdmin = request.session['user']
        loop = [0,1]
        Decode_All_Details_charity = []
        All_Details_charity=list(db.get_database().charity.find())
        All_zakah_types=list(db.get_database().all_types.find())
        #for loop to get encode password and decode it then store in new list 
        for enc_char in All_Details_charity:
            if enc_char["password"]:
                enc_char["password"]= enc_char["password"].decode("utf_16")
                Decode_All_Details_charity.append(enc_char)
                print(' Decode_All_Details_charity',enc_char["password"])
        print(' Decode_All_Details_charity',Decode_All_Details_charity)
        All_Details_Device=list(db.get_database().devices.find())
        P_dev = []
        U_dev = []
        for dev in All_Details_Device:
            char_id = dev['charity_id']
            print('char_id',char_id)
            if (char_id!=''): 
                print("found")
                charity_found=list(db.get_database().charity.find({'_id': char_id}))
                print("charity_found",charity_found)
                try:
                    dev['charity_name'] = charity_found[0]['name_ar']
                    P_dev.append(dev)  
                except:pass
        
            else: 
                print("not found")
                U_dev.append(dev)

        print('P_dev',P_dev)
        print('U_dev',U_dev)
    else:
        return redirect('login')
    context = {
        'All_Details_charity':Decode_All_Details_charity,
        'All_zakah_types':All_zakah_types,
        'P_dev':P_dev,
        'U_dev': U_dev,
        'loop':loop ,
        'userAdmin':userAdmin,
         
    }

    return render(request,'AdminDasshboard.html',context)

def add_Charity(request):
    msg = 'done'
    if request.session.has_key("user"): 
        if request.method == "GET":
            charData= request.GET.get('myJSONData')
            #conver json to list
            data  = json.loads(charData)
            ch_user = data[0]
            ch_pass = data[1]
            print('charData',charData)
            print('ch_user :',ch_user)
            print('ch_pass :',ch_pass)
            encode_pass = ch_pass.encode("utf_16")
            print('encode_pass',encode_pass)
            check_char_user = db.get_database().charity.find_one({'username': ch_user})
            if not check_char_user:
                        Collection = {"username": ch_user, "password": encode_pass,"name_en":"","name_ar":"","city":"","website":"","phone":"","logo":"","email":""}
                        db.get_database().charity.insert_one(Collection)
                        return redirect('AdminDash')
    else:
        return redirect('login')
    return HttpResponse(msg)

#update charity info      
def Edit_charity(request):
    msg = 'done'
    if request.session.has_key("user"): 
        if request.method == "GET":
            charData= request.GET.get('myJSONData')
            #conver json to list
            data  = json.loads(charData)
            ch_user = data[0]
            ch_pass = data[1].encode("utf_16")
            ch_olduser = data[2]
            ch_oldenName = data[3]
            ch_oldarName = data[4]
            print('ch_user:ch_pass',ch_user,ch_pass,ch_olduser)
            myquery = { "username": ch_olduser }
            newvalues =  {"$set": {"username": ch_user, "password":ch_pass,"name_ar":ch_oldarName,"name_en":ch_oldenName}}
            db.get_database().charity.update_one(myquery,newvalues)
    else:
        return redirect('login')
    return HttpResponse(msg)



#delete item from types collection
def delete_charity(request):
    if request.session.has_key("user"): 
        if request.method == 'GET':  
            char_username = request.GET.get('char_username')  
            print('char_username',char_username)
            myquery = {"username":char_username}
            print(myquery)
            db.get_database().charity.delete_one(myquery)
            print("delete_one")
            return redirect('AdminDash')
    else:
        return redirect('login')

#Add Device
def add_Dev(request):
    if request.session.has_key("user"): 
        if request.method == "GET":
            DevData= request.GET.get('myJSONData')
            #conver json to list
            data  = json.loads(DevData)
            dev_user = data[0]
            dev_pass = data[1]
            dev_mac = data[2]
            print('DevData',DevData)
            print('dev_user :',dev_user)
            print('dev_pass :',dev_pass)
            print('dev_pass :',dev_mac)
            check_dev_user = db.get_database().devices.find_one({'name': dev_user})
            if not check_dev_user:
                        Collection = {"name": dev_user,"password": dev_pass,"mac": dev_mac,"status":'0',"charity_id":"","start_date":"","last_maintenance":"","city":""}
                        db.get_database().devices.insert_one(Collection)
    else:
        return redirect('login')
                        
    return HttpResponse('done')

#delete item from types collection
def delete_Device(request):
    if request.session.has_key("user"): 
        if request.method == 'GET':  
            device_name = request.GET.get('dev_name')  
            print('char_username',device_name)
            myquery = {"name":device_name}
            print(myquery)
            db.get_database().devices.delete_one(myquery)
            print("delete_one")
            return HttpResponse(device_name)
    else:
        return redirect('login')

#assign charity to device      
def assign_Device(request):
    if request.session.has_key("user"): 
        msg = 'done'
        if request.method == "GET":
            DevData= request.GET.get('myJSONData')
                #conver json to list
            data  = json.loads(DevData)
            charity_Name = data[0]
            dev_status = data[1]
            dev_startDate= data[2]
            device_name = data[3]
            dev_maintDate = data[4]
            dev_NextmaintDate = data[5]
            print('DevData',DevData,device_name)
            print('device_name',device_name)
            print('charity_Name from  assign_Device:',charity_Name)
            print('dev_status :',dev_status)
            print('dev_startDate :',dev_startDate)
            find_charity_id = list(db.get_database().charity.find({'name_ar': charity_Name}))
            for c in find_charity_id:
                _charID = c['_id']
                print('_charID',_charID)
                print('find_charity_id',find_charity_id)
                print('device_name',device_name)
                myquery = { "name": device_name }
                newvalues =  {"$set": {"status": dev_status, "charity_id":_charID,"start_date":dev_startDate,"last_maintenance":dev_maintDate,"next_maintenance":dev_NextmaintDate}}
                db.get_database().devices.update_one(myquery, newvalues)
            return HttpResponse(msg)
    else:
        return redirect('login')
#Display Zakah
def displayZakah(request):
    msg = "done"
    all_types = []
    ReturnResponse = []
    if request.session.has_key("user"): 
        if request.method == "GET":
            try:
                zakah_en = request.GET.get('zakah_en')
                zakah_ar = request.GET.get('zakah_ar')
                arr = request.GET.get('zakahtype')
                # data  = json.loads(arr)
                print('zakah_en',zakah_en,'zakah_ar',zakah_ar,'arr',arr)
                print('arr',arr)
                if zakah_en and  zakah_ar:
                    check_type=db.get_database().all_types.find_one({'name_en': zakah_en})
                    if not check_type:
                        Collection = {"name_en": zakah_en, "name_ar": zakah_ar}
                        lastid  = db.get_database().all_types.insert_one(Collection)
                        print('lastid',lastid.inserted_id)
                    else:print("zakah_type exits")
                All_zakah_types=list(db.get_database().all_types.find())
                print('All_zakah_types',All_zakah_types)
                for all in All_zakah_types:
                    z_name_ar = all['name_ar']
                    z_name_en = all['name_en']
                    zakah_id = all['_id']
                    print('zakah_id',type(zakah_id))
                    all_types.append({'id': str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar})
                    print('all_types',all_types)
                ReturnResponse = all_types       
            except:pass
    else:return redirect('login')   
    return JsonResponse({"all_types":ReturnResponse})
#delete zakah type
def delete_zakah(request):
    if request.session.has_key("user"): 
        if request.method == 'GET':  
            zakah_name = request.GET.get('zakah_name_en')  
            print('zakah_name to delete',zakah_name)
            myquery = {"name_en":zakah_name}
            print(myquery)
            db.get_database().all_types.delete_one(myquery)
            print("delete_zakah")
            return HttpResponse(zakah_name)
    else:
        return redirect('login')
    

#delete subzakah type
def delete_subzakah4admin(request):
    if request.session.has_key("user"): 
        userAdmin = request.session['user']
        if request.method == 'POST':  
            id = request.POST.get('subid')  
            name = request.POST.get('name')  
            print('zakah_name to delete',id,name)
            myquery = {"_id":ObjectId(id)}
            print(myquery)
            result = db.get_database().sub_types.delete_one(myquery)
            if result.deleted_count == 1:
                print("delete_zakah")
                zakah_subtypes=[]
                entype=list(db.get_database().all_types.find({"_id": ObjectId(name)}))
                for type in entype:
                    name_ar =type['name_ar']
                print('name_arname_ar',name_ar)
                subtypes=list(db.get_database().sub_types.find({'type_id': name}))
                for sub in subtypes:
                            z_name_ar = sub['sub_type_ar']
                            z_name_en = sub['sub_type_en']
                            zakah_id = sub['_id']
                            zakah_type_id= sub['type_id']
                            zakah_subtypes.append({'id': str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar,'type_id':zakah_type_id})
                print('subtype',subtypes)
                context = {
                        'userAdmin':userAdmin,
                        'zakahname':name_ar,
                        'subtypes':zakah_subtypes,
                        'enZakahName':name
                    }
                return render(request,'SubZakah4Admin.html',context)

    else:
        return redirect('login')


#Add Subzakah
def AddSubZakah(request):
    if request.session.has_key("user"): 
        if request.method == "GET":
            try:
                zakah_suben = request.GET.get('zakah_suben')
                zakah_subar = request.GET.get('zakah_subar')
                zakahid = request.GET.get('zakahid')
            except:pass
            if zakah_suben and zakah_subar:
                check_subtype=db.get_database().sub_types.find_one({"type_id": zakahid,"sub_type_en": zakah_suben})
                if not check_subtype:
                        Collection = {"type_id":zakahid,"sub_type_ar": zakah_subar, "sub_type_en": zakah_suben}
                        lastid  = db.get_database().sub_types.insert_one(Collection)
                        last_ins_id = lastid.inserted_id
                        print('last_ins_id',last_ins_id)
                        if str(last_ins_id) !="":
                            print('last_ins_id add')
                            return HttpResponse('add')
                else: 
                    print('exit')
                    return HttpResponse('exit')
        # return HttpResponse("Invalid request")

           
                

def subzakah4admin(request):
    if request.session.has_key("user"): 
        userAdmin = request.session['user']
        if request.method == "POST":
            name_ar =''
            name = request.POST.get('zakahId')
            print('subzakah4admin',name)
            zakah_subtypes=[]
            entype=list(db.get_database().all_types.find({"_id": ObjectId(name)}))
            for type in entype:
                name_ar =type['name_ar']
            print('name_arname_ar',name_ar)
            subtypes=list(db.get_database().sub_types.find({'type_id': name}))
            for sub in subtypes:
                        z_name_ar = sub['sub_type_ar']
                        z_name_en = sub['sub_type_en']
                        zakah_id = sub['_id']
                        zakah_type_id= sub['type_id']
                        zakah_subtypes.append({'id': str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar,'type_id':zakah_type_id})
            print('subtype',subtypes)
            context = {
                    'userAdmin':userAdmin,
                    'zakahname':name_ar,
                    'subtypes':zakah_subtypes,
                    'enZakahName':name
                }
            return render(request,'SubZakah4Admin.html',context)







#Edit zakah type
def edit_Zakah(request):
    Edit_all_types =[]
    if request.session.has_key("user"): 
        msg = 'done'
        if request.method == "GET":
            zakahData= request.GET.get('myJSONData')
                #conver json to list
            data  = json.loads(zakahData)
            Zakah_id =  ObjectId(data[0])
            zakah_Name_en = data[1]
            zakah_Name_ar = data[2]
            print('data',data)
            print('zakah_Name_en :',zakah_Name_en)
            print('zakah_Name_ar :',zakah_Name_ar)
            myquery = { "_id": Zakah_id}
            if myquery:print("myquery found")
            newvalues =  {"$set": {"name_en": zakah_Name_en, "name_ar":zakah_Name_ar}}
            db.get_database().all_types.update_one(myquery, newvalues)
            All_zakah_types=list(db.get_database().all_types.find())
            for all in All_zakah_types:
                z_name_ar = all['name_ar']
                z_name_en = all['name_en']
                zakah_id = all['_id']
                print('zakah_id',zakah_id)
                Edit_all_types.append({'id':str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar})
                print('Edit_all_types',Edit_all_types)
            return JsonResponse({'Edit_all_types':Edit_all_types})
    else:
        return redirect('login')

#logout 
def logout(request):
    if request.session.has_key("user"):
        del request.session['user']
        print("del request.session['user']")
    return redirect('login')
    

def AddZakahFromCharitySide(request):
    global user
    if request.session.has_key("user"):  
        charity_id = user['_id']
        if request.method == "GET":
            try:
                zakah_en = request.GET.get('zakah_en')
                zakah_ar = request.GET.get('zakah_ar')
                print('AddZakahFromCharitySide zakah_en',zakah_en,'zakah_ar',zakah_ar)
            except:pass
        print('request.session.has_key("user")')
        charity_id = user['_id']
        print('charity_id',charity_id)
        check_type_in_all_types = db.get_database().all_types.find_one({'name_en': zakah_en})
        if not check_type_in_all_types:
            check_type_in_types = db.get_database().types.find_one({'type_en': zakah_ar,'charity_id': charity_id})
            if not check_type_in_types:
                Collection4all_types = { "name_ar": zakah_ar, "name_en": zakah_en}
                lastid = db.get_database().all_types.insert_one(Collection4all_types)
                fetchlastid = lastid.inserted_id
                print('lastid',fetchlastid)
                if fetchlastid !="":
                    Collection4a_types = {'type_id':fetchlastid,"type_ar": zakah_ar, "type_en": zakah_en,"charity_id":charity_id}
                    db.get_database().types.insert_one(Collection4a_types)
            return HttpResponse(0)
        else:return HttpResponse(1)
   
def edit_subzakah(request):
    if request.session.has_key("user"): 
        userAdmin = request.session['user']
        if request.method == "POST":
            try:
                subar = request.POST.get('subzar')
                suben = request.POST.get('subzen')
                val2edit = request.POST.get('val2edit')
                value = val2edit.split(",")
                print('subar',subar,'suben',suben,'val2edit',val2edit,'value',value,value[0],value[1],value[2])
            except:pass 
            if  subar!="" and  suben!="" :
                check_subtype = db.get_database().sub_types.find_one({"type_id": value[2], "sub_type_en": suben})
                if not check_subtype: 
                   myquery = {"_id":ObjectId(value[0])}
                   newvalues =  {"$set": {"sub_type_ar": subar, "sub_type_en":suben}}
                   result = db.get_database().sub_types.update_one(myquery, newvalues)
                   if result.modified_count == 1:
                    zakah_subtypes=[]
                    entype=list(db.get_database().all_types.find({"_id": ObjectId(value[1])}))
                    for type in entype:
                        name_ar =type['name_ar']
                        name_en =type['name_en']
                    print('name_arname_ar',name_ar)
                    subtypes=list(db.get_database().sub_types.find({'type_id': value[1]}))
                    for sub in subtypes:
                                z_name_ar = sub['sub_type_ar']
                                z_name_en = sub['sub_type_en']
                                zakah_id = sub['_id']
                                zakah_type_id= sub['type_id']
                                zakah_subtypes.append({'id': str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar,'type_id':zakah_type_id})
                    print('subtype',subtypes)
                    context = {
                            'userAdmin':userAdmin,
                            'zakahname':name_ar,
                            'subtypes':zakah_subtypes,
                            'enZakahName':name_en
                        }
                    return render(request,'SubZakah4Admin.html',context)

                else: 
                    print('subzakahexit')
                    return HttpResponse('exit')
            else:
                print('empty')
                return HttpResponse('empty')
        
        
def addSubzahah4SpecialType(request):
    if request.session.has_key("user"): 
        userAdmin = request.session['user']
        if request.method == "POST":
            zakah_subtypes= []
            try:  
                subar = request.POST.get('subar4type')
                suben = request.POST.get('suben4type')
                zakahID = request.POST.get('zakahnameinurl')
                print('zakahtype',zakahID)
            except:pass 
            if zakahID !="":
                FetchZakah = list(db.get_database().all_types.find({'_id':ObjectId(zakahID)}))
                if FetchZakah is not None:
                    for zakah in FetchZakah:
                        name_ar =zakah['name_ar']
                        name_en =zakah['name_en']
                        # zakah_id = zakah["_id"]
                    if  subar!="" and  suben!="" :
                        check_subtype = db.get_database().sub_types.find_one({"type_id":str(zakahID), "sub_type_en": suben})  
                        print('check_subtype',check_subtype)                      
                        if not check_subtype: 
                                Collection = {"type_id":str(zakahID),"sub_type_ar": subar, "sub_type_en":suben}
                                result = db.get_database().sub_types.insert_one(Collection)
                                if result.inserted_id is not None:
                                    subtypes=list(db.get_database().sub_types.find({"type_id":str(zakahID)}))
                                    for sub in subtypes:
                                                z_name_ar = sub['sub_type_ar']
                                                z_name_en = sub['sub_type_en']
                                                zakah_id = sub['_id']
                                                zakah_type_id= sub['type_id']
                                                zakah_subtypes.append({'id': str(zakah_id),'name_en':z_name_en,'name_ar':z_name_ar,'type_id':zakah_type_id})
                                    print('subtype',subtypes)
                                    context = {
                                            'userAdmin':userAdmin,
                                            'zakahname':name_ar,
                                            'subtypes':zakah_subtypes,
                                            'enZakahName':name_en
                                        }
                                    return render(request,'SubZakah4Admin.html',context)
                        else: 
                                print('subzakahexit')
                                return HttpResponse('exit')
                    else:
                        print('empty')
                        return HttpResponse('empty')


#Charity subzakah
def addSubzakah4charity(request):
    global user
    choose_subtypes = []
    if request.session.has_key("user"):  
        charity_id = user['_id']
        if request.method == "GET":
            zakahName = request.GET.get('zakahName')
            print('zakahName',zakahName)
            if(zakahName):
                fetch_type_en = list(db.get_database().types.find({'type_en': zakahName}))
                for zakah in fetch_type_en:
                    type_id = zakah["type_id"]
                    print("type_id",str(type_id))
            charit_sub_types=db.get_database().charity_subtypes.find({'charity_id': charity_id,'type_id':str(type_id)})
            charit_subtypes_list = list(charit_sub_types)
            All_sub_types=db.get_database().sub_types.find({'type_id': str(type_id)})
            All_subtypes_list = list(All_sub_types)
            print("All_types_list",All_subtypes_list)
            print("charit_types_list",charit_subtypes_list)
            #add all types in all_types table except types in types table in list
            for s_types in All_subtypes_list:
                Found = False
                for char_subtype in charit_subtypes_list:
                    if char_subtype ['sub_type_en'].strip() == s_types ['sub_type_en'].strip() :
                        Found = True
                        print(Found)
                if(not Found ):
                    choose_subtypes.append({'sub_type_en':s_types['sub_type_en'],'sub_type_ar':s_types['sub_type_ar']})

        if request.method == "GET":
            # zakahName = request.GET.get('zakahName')
            checkbox_types = request.GET.get('myCheckboxes')
            # print("checkbox_types",checkbox_types,'zakahName',zakahName)
            # if(zakahName):
            #     fetch_type_en = list(db.get_database().types.find({'type_en': zakahName}))
            #     for zakah in fetch_type_en:
            #         type_id = zakah["_id"]
            if (checkbox_types):
                L = checkbox_types.strip("][").replace("\"", "").split(",")
                print(L)
                for type_list in L:
                    type_en = type_list.split(":")[0]
                    type_ar= type_list.split(":")[1]
                    print('type_en',type_en)
                    print('type_ar',type_ar)
                    check_type_en = db.get_database().charity_subtypes.find_one({'sub_type_en': type_en,'charity_id': charity_id})
                    if not check_type_en:
                        Collection = {"type_id":str(type_id),"sub_type_ar": type_ar, "sub_type_en": type_en,"charity_id":charity_id}
                        db.get_database().charity_subtypes.insert_one(Collection)
                        return redirect('dashboardOld')

        print("choose_subtypes",choose_subtypes)
        return JsonResponse({'choose_subtypes':choose_subtypes})
    else:
        return redirect('login')
             


def addOtherSubZakah4charity(request):
    if request.session.has_key("user"):  
        charity_id = user['_id']
        if request.method == "POST":
            try:  
                subar = request.POST.get('othersub4charar')
                suben = request.POST.get('othersub4charen')
                zakahName = request.POST.get('zakName')
                print('zakahtype',zakahName)
            except:pass
            if(zakahName):
                fetch_type_en = list(db.get_database().types.find({'type_en': zakahName}))
                for zakah in fetch_type_en:
                    type_id = zakah["type_id"]
                if  subar!="" and  suben!="" :
                    check_subtype = db.get_database().charity_subtypes.find_one({'sub_type_en': suben,'charity_id': charity_id})
                    print('check_subtype',check_subtype)                      
                    if not check_subtype: 
                        Collection = {"type_id":str(type_id),"sub_type_ar": subar, "sub_type_en": suben,"charity_id":charity_id}
                        db.get_database().charity_subtypes.insert_one(Collection)
                        return HttpResponse('add')
                    else: 
                            print('subzakahexit')
                            return HttpResponse('exit')
                else:
                    print('empty')
                    return HttpResponse('empty')
    else:
        return redirect('login')



def viewsubzakah4charity(request):
    if request.session.has_key("user"):  
        charity_id = user['_id']
        zakah_subtypes4char = []
        arzakakName = ""  # Initialize with a default value
        context = {}  # Define context variable before if statement
        name = request.POST.get('name') or request.GET.get('name')
        if name:
            print('name',name)
            fetchtype_id=list(db.get_database().types.find({'type_en': name,'charity_id':charity_id}))
            for type in fetchtype_id:
                type_id =type['type_id']
                arzakakName =type['type_ar']  # Update the variable inside the block
                print('type_id',type_id)
                subtypes=list(db.get_database().charity_subtypes.find({'type_id':type_id,'charity_id':charity_id}))
                for sub in subtypes:
                    zakah_subtypes4char.append({'id': str(sub['_id']),'type_id': sub['type_id'],'sub_type_en':sub['sub_type_en'],'sub_type_ar':sub['sub_type_ar']})
                print('subtype',subtypes)
            print('zakah_subtypes4char',zakah_subtypes4char)

            context = {
                    'subtypes':zakah_subtypes4char,
                    'enZakahName':name,
                    'arzakakName':arzakakName
            }

            return render(request,'subZakah4Charity.html',context)




def delete_subzakah(request):
    if request.session.has_key("user"):  
        charity_id = user['_id']
        zakah_subtypes4char = []
        arzakakName = ""  # Initialize with a default value
        context = {}  # Define context variable before if statement
        if request.method == 'POST':  
            id = request.POST.get('subid')  
            name = request.POST.get('name')  
            print('zakah_name to delete',id,name)
            myquery = {"_id":ObjectId(id),'charity_id':charity_id}
            print(myquery)
            db.get_database().charity_subtypes.delete_one(myquery)
            print("delete_zakah")
            if name:
                print('name',name)
                fetchtype_id=list(db.get_database().types.find({'type_en': name,'charity_id':charity_id}))
                for type in fetchtype_id:
                    type_id =type['type_id']
                    arzakakName =type['type_ar']  # Update the variable inside the block
                    print('type_id',type_id)
                    subtypes=list(db.get_database().charity_subtypes.find({'type_id':type_id,'charity_id':charity_id}))
                    for sub in subtypes:
                        zakah_subtypes4char.append({'id': str(sub['_id']),'type_id': sub['type_id'],'sub_type_en':sub['sub_type_en'],'sub_type_ar':sub['sub_type_ar']})
                    print('subtype',subtypes)
                print('zakah_subtypes4char',zakah_subtypes4char)

                context = {
                        'subtypes':zakah_subtypes4char,
                        'enZakahName':name,
                        'arzakakName':arzakakName
                }

                return render(request,'subZakah4Charity.html',context)
    else:
        return redirect('login')
    


def edit_subzakah4type4charity(request):
    if request.session.has_key("user"):  
        charity_id = user['_id']
        zakah_subtypes4char = []
        arzakakName = ""  # Initialize with a default value
        context = {}  # Define context variable before if statement
        if request.method == "POST":
            try:
                subar = request.POST.get('editsubzar4ch')
                suben = request.POST.get('editsubzen4ch')
                val2edit = request.POST.get('val2edit4char')
                value = val2edit.split(",")
                print('subar',subar,'suben',suben,'val2edit',val2edit,'value',value,value[0],value[1],value[2])
            except:pass 
            if  subar!="" and  suben!="" :
                check_subtype = db.get_database().charity_subtypes.find_one({"type_id": value[2], "sub_type_en": suben,"charity_id":charity_id})
                if not check_subtype: 
                    myquery = {"_id":ObjectId(value[0])}
                    newvalues =  {"$set": {"type_id": value[2],"sub_type_ar": subar, "sub_type_en":suben,"charity_id":charity_id}}
                    result = db.get_database().charity_subtypes.update_one(myquery, newvalues)
                    if result.acknowledged:
                        print('name',value[1])
                        fetchtype_id=list(db.get_database().types.find({'type_en': value[1],'charity_id':charity_id}))
                        for type in fetchtype_id:
                            type_id =type['type_id']
                            arzakakName =type['type_ar']  # Update the variable inside the block
                            print('type_id',type_id)
                            subtypes=list(db.get_database().charity_subtypes.find({'type_id':type_id,'charity_id':charity_id}))
                            for sub in subtypes:
                                zakah_subtypes4char.append({'id': str(sub['_id']),'type_id': sub['type_id'],'sub_type_en':sub['sub_type_en'],'sub_type_ar':sub['sub_type_ar']})
                            print('subtype',subtypes)
                        print('zakah_subtypes4char',zakah_subtypes4char)

                        context = {
                                'subtypes':zakah_subtypes4char,
                                'enZakahName':value[1],
                                'arzakakName':arzakakName
                        }

                        return render(request,'subZakah4Charity.html',context)
                    return redirect ('subzakah4charity', name=value[1])
                else: 
                    print('subzakahexit')
                    return HttpResponse('exit')
            else:
                print('empty')
                return HttpResponse('empty')


def add_subzakah4type4charity(request):
    if request.session.has_key("user"):  
        charity_id = user['_id']
        if request.method == "POST":
            try:  
                subar = request.POST.get('subar4type4charity')
                suben = request.POST.get('suben4type4charity')
                zakahtype = request.POST.get('zakahnameurl')
                print('zakahtype',zakahtype)
            except:pass
            if zakahtype !="":
                fetch_type_en = list(db.get_database().types.find({'type_en': zakahtype}))
                for zakah in fetch_type_en:
                    type_id = zakah["type_id"]
                if  subar!="" and  suben!="" :
                    check_subtype = db.get_database().charity_subtypes.find_one({'sub_type_en': suben,'charity_id': charity_id})
                    print('check_subtype',check_subtype)                      
                    if not check_subtype: 
                        Collection = {"type_id":str(type_id),"sub_type_ar": subar, "sub_type_en": suben,"charity_id":charity_id}
                        db.get_database().charity_subtypes.insert_one(Collection)
                        return HttpResponse('add')
                    else: 
                            print('subzakahexit')
                            return HttpResponse('exit')
                else:
                    print('empty')
                    return HttpResponse('empty')
                

def findStatisticsDetails(device_ID):
    donation_by_typeName = []
    donation_Count=0
    donation_by_type = defaultdict(float)
    total_sum = 0

    Device_trans_list = list(db.get_database().transactions.find({'device_id': ObjectId(device_ID)}))
    print('findStatisticsDetails Device_trans_list', Device_trans_list)

    for dev in Device_trans_list:
        device_money = float(dev['money'])
        donation_type = dev['type']

        if device_money > 0:
            print('device_money', device_money)
            total_sum += device_money
            donation_by_type[donation_type] += device_money

    # Convert defaultdict to a list of dictionaries
    donation_by_type = [{'type': k, 'money': v} for k, v in donation_by_type.items()]
    for findtype in donation_by_type:
        type=findtype ['type']
        money = findtype ['money']
        findstype = list(db.get_database().charity_subtypes.find({'_id': type}))
        for stype in findstype:
            print('findtype',stype['sub_type_ar'])
            donation_by_typeName.append({'type': stype['sub_type_ar'], 'money': '{:.1f}'.format(money)})
    donation_Count = len(Device_trans_list)

    return donation_by_typeName, donation_Count, total_sum


@csrf_exempt
def statistics4OneDevice(request):
    if request.session.has_key("user"):  
        if user is not None:
            userN = user['username']
            logo = user['logo']
            charity_name = user['name_ar']
            # charity_id = user['_id']
            print('statistics4OneDevice')
            today = datetime.datetime.now()
            device_name = ''
            Day = Month = Year = donation_by_typeName = None
            donation_Count = total_sum = None
            filter_num=None
            this_year = today.year
            last_ten_years = this_year - 11
            print('year',this_year,'last_ten_years',last_ten_years)
            YEAR_CHOICES = []
            for r in range(this_year, last_ten_years, -1):
                YEAR_CHOICES.append((r))
            
            if request.method == 'GET':
                Device_ID = request.GET.get('Device_ID')
                print('Device_ID statistics4OneDevice', Device_ID)
                request.session['Device_ID'] = Device_ID
                fetchDevice = list(db.get_database().devices.find({'_id': ObjectId(Device_ID)}))
                print('len(fetchDevice)', len(fetchDevice))
                for dev in fetchDevice:
                    device_name = dev['name']
                print("statistics4OneDevice", Device_ID, device_name)
                
                Day = oneDay_Statistics(Device_ID)
                Month = oneMonth_Statistics(Device_ID)
                Year = oneYear_Statistics(Device_ID)
                print("Day from oneDay_Statistics", Day, "Month from oneDay_Statistics", Month)
                donation_by_typeName, donation_Count, total_sum = findStatisticsDetails(Device_ID)
          
                context = {
                    'OneDay_tarns_Num': Day,
                    'Onemonth_tarns_Num': Month,
                    'Oneyear_tarns_Num': Year,
                    'donation_by_type': donation_by_typeName,
                    'donation_Count': donation_Count,
                    'total_sum': total_sum,
                    'device_name': device_name,
                    'Device_ID':Device_ID,
                    'YEAR_CHOICES':YEAR_CHOICES,
                    'charity_name':charity_name,
                    'logo':logo,
                }
                print('context', context)
                
                return render(request, 'OneDeviceStatistics.html', context)
            if request.method == "POST":
                Device_ID =  request.POST.get('devID')
                start_Date = request.POST.get('sDate')
                end_Date = request.POST.get('eDate')
                year = request.POST.get('year')
                month = request.POST.get('month')
                print('year & month',year,month)
                if Device_ID :
                    if  start_Date and end_Date:
                        result = SearchBetween2Dates4OneDev(Device_ID, start_Date, end_Date)
                    if  month and year:
                        result = SearchBetweenMonthYear4OneDev(Device_ID, month, year)
                    print('result',result)
                    if result is not None:
                            filter_num, filter_sum = result
                            print('s4devDate start_Date', start_Date, type(start_Date))
                            print('filter_num,filter_sum', filter_num, filter_sum)
                            data = {'filter_num': filter_num,'filter_sum':filter_sum}
                            print('data',data)
                            return JsonResponse(data)
        return redirect('login')

    
def SearchBetween2Dates4OneDev(dev_id,date1,date2):
    converDate_1 = datetime.datetime.strptime(date1, "%Y-%m-%d")                       
    converDate_2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    print('SearchBetween2Dates4OneDev converDate_1',converDate_1,type(converDate_1))
    Device_2Dates = list(db.get_database().transactions.find(
                            {"datetime": {"$gte":converDate_1, "$lt":converDate_2},
                            'device_id': ObjectId(dev_id)}
                            ))   
    filter_num = len(Device_2Dates)
    print('SearchBetween2Dates4OneDev Device_2Dates',Device_2Dates)
    print('filter_num between 2 dates',filter_num)
    sum =0
    for amounts in Device_2Dates:
        device2day_money = int(amounts['money'])
        print('device_money',device2day_money)
        sum = sum + device2day_money
        filter_sum = '{:.3f}'.format(sum)
        print('filter_sum 2 cal date',filter_sum)
        return filter_num,filter_sum

def SearchBetweenMonthYear4OneDev(dev_id,month,year):
        print('SearchBetweenMonthYear4OneDev',month,year)
        today = datetime.datetime.now()
        this_year = today.year
       #if month from user
        if month and year:
            if month == '12':
                start_Month_Yearstring = year + "-" + month  + "-01"  + " 00:00:00"
                #year-01-01
                end_Month_Yearstring = year + "-01-01"   + " 00:00:00"
                print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
                print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
            else:
                start_Month_Yearstring = year + "-" +month  + "-01"  + " 00:00:00"
                #year-01-01
                end_Month_Yearstring = year + "-"+str(int(month)+1) + "-01"   + " 00:00:00"

            print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
            print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
            start_Month_Year_gth = parse_datetime(start_Month_Yearstring)
            end_Month_Year_lth = parse_datetime(end_Month_Yearstring)    
            print('start_Month_Year_gth',start_Month_Year_gth,type(start_Month_Year_gth))
            print('end_Month_Year_lth',end_Month_Year_lth,type(end_Month_Year_lth))
            Device_Month_Year = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_Month_Year_gth, "$lt":end_Month_Year_lth},
                'device_id': ObjectId(dev_id)}
            ))
            Device_Month_Year_num = len(Device_Month_Year)
            print('Device_Month_Year_num',Device_Month_Year_num)
            
            Month_Year_sum =0
            for Month_Year_amounts in Device_Month_Year:
                deviceMonth_year_money = int(Month_Year_amounts['money'])
                print('deviceMonth_year_money',deviceMonth_year_money)
                Month_Year_sum = Month_Year_sum + deviceMonth_year_money
            sum_Month_year_Round = '{:.3f}'.format(Month_Year_sum)
            filter_num = Device_Month_Year_num
            filter_sum = sum_Month_year_Round
            print('filter_num from month and year',filter_num,filter_sum)
            return filter_num,filter_sum
            # return JsonResponse({'filter_num':Device_Month_Year_num,'filter_sum':sum_Month_year_Round})
        elif month:
            print("month",type(month),month)
            if month == '12':
                #year-12-01
                start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                #year-01-01
                end_string = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                
            else:
                #year-12-01
                start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                #year-01-01
                end_string = str(this_year)+ "-" + str(int(month)+1) + "-01"   + " 00:00:00"
            print('start_string',start_string,type(start_string))
            print('end_string',end_string,type(end_string))
            start_month_gth = parse_datetime(start_string)
            end_month_lth = parse_datetime(end_string)
            print('start_month_gth',start_month_gth,type(start_month_gth))
            print('end_month_lth',end_month_lth,type(end_month_lth))
                #dataBase
            Device_month = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_month_gth, "$lt":end_month_lth},
                'device_id':  ObjectId(dev_id)}
            ))
            Device_month_num = len(Device_month)
            print('Device_month_num',Device_month_num)
            
            month_sum =0
            for month_amounts in Device_month:
                devicemonth_money = int(month_amounts['money'])
                print('devicemonth_money',devicemonth_money)
                month_sum = month_sum + devicemonth_money
            sum_Month_Round = '{:.3f}'.format(month_sum)
            filter_num = Device_month_num
            filter_sum = sum_Month_Round
            print('filter_num from month and year',filter_num,filter_sum)
            return filter_num,filter_sum
            # return JsonResponse({'filter_num':Device_month_num,'filter_sum':sum_Month_Round})
            #if year from user
        elif year:
                print("year_from_user",type(year),year)
                start_Yearstring = year + "-01"  + "-01"   + " 00:00:00"
                #year-01-01
                end_Yearstring = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                print('start_Yearstring',start_Yearstring,type(start_Yearstring))
                print('end_Yearstring',end_Yearstring,type(end_Yearstring))
                start_Year_gth = parse_datetime(start_Yearstring)
                end_Year_lth = parse_datetime(end_Yearstring)
                print('start_Year_gth',start_Year_gth,type(start_Year_gth))
                print('end_Year_lth',end_Year_lth,type(end_Year_lth))
                Device_Year = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_Year_gth, "$lt":end_Year_lth},
                'device_id':  ObjectId(dev_id)}
                ))
                Device_Year_num = len(Device_Year)
                print('Device_Year_num',Device_Year_num)
            
                Year_sum =0
                for Year_amounts in Device_Year:
                    deviceyear_money = int(Year_amounts['money'])
                    print('deviceyear_money',deviceyear_money)
                    year_sum = Year_sum + deviceyear_money
                sum_year_Round = '{:.3f}'.format(year_sum)
                filter_num = Device_Year_num 
                filter_sum = sum_year_Round
                print('filter_num from month and year',filter_num,filter_sum)
                return filter_num,filter_sum

                # return JsonResponse({'filter_num':Device_Year_num,'filter_sum':sum_year_Round})




def findStatisticsDetails4AllDev(device_list):
    donation_by_typeName = []
    donation_Count=0
    donation_by_type = defaultdict(float)
    total_sum = 0
    print('device_list',device_list)
    for dev in device_list:
        device_ID=dev['_id']
        Device_trans_list = list(db.get_database().transactions.find({'device_id': ObjectId(device_ID)}))
        print('findStatisticsDetails Device_trans_list', Device_trans_list)

        for dev in Device_trans_list:
            device_money = float(dev['money'])
            donation_type = dev['type']

            if device_money > 0:
                print('device_money', device_money)
                total_sum += device_money
                donation_by_type[donation_type] += device_money

        # Convert defaultdict to a list of dictionaries
        donation_by_type_list = [{'type': k, 'money': v} for k, v in donation_by_type.items()]
        for findtype in donation_by_type_list:
            type=findtype ['type']
            money = findtype ['money']
            findstype = list(db.get_database().charity_subtypes.find({'_id': type}))
            for stype in findstype:
                print('findtype',stype['sub_type_ar'])
                donation_by_typeName.append({'type': stype['sub_type_ar'], 'money': '{:.1f}'.format(money)})
        donation_Count = len(Device_trans_list)
    print('donation_by_typeName for all dev',donation_by_typeName)

    return donation_by_typeName, donation_Count, total_sum


def find_Statistics_2Dates_AllDev(date1,date2,device_list):
    print('find_Statistics_2Dates_AllDev',device_list)
    for dev in device_list:
        device_ID=dev['_id']
        Device_2Dates = list(db.get_database().transactions.find(
        {"datetime": {"$gte":date1, "$lt":date2},
        'device_id': ObjectId(device_ID)}
        ))
        print('Device_2Dates',Device_2Dates)
        filter_num = len(Device_2Dates)
        print('Device_2Dates',Device_2Dates)
        print('filter_num between 2 dates',filter_num)
        sum =0
        for amounts in Device_2Dates:
            device2day_money = int(amounts['money'])
            print('device_money',device2day_money)
            sum = sum + device2day_money
        filter_sum = '{:.3f}'.format(sum)
        print('filter_sum 2 cal date',filter_sum)
        return filter_num,filter_sum
    
def find_Statistics_monthYear_AllDev(month,year,device_list):
    print('year_from_user',month,year)
    today = datetime.datetime.now()
    this_year = today.year
    for dev in device_list:
        device_ID=dev['_id']
       #if month from user
        if month and year:
            print('month and year from fun',month,year)
            if month == '12':
                start_Month_Yearstring = year + "-" + month  + "-01"  + " 00:00:00"
                #year-01-01
                end_Month_Yearstring = year + "-01-01"   + " 00:00:00"
                print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
                print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
            else:
                start_Month_Yearstring = year + "-" +month  + "-01"  + " 00:00:00"
                #year-01-01
                end_Month_Yearstring = year + "-"+str(int(month)+1) + "-01"   + " 00:00:00"

            print('start_Month_Yearstring',start_Month_Yearstring,type(start_Month_Yearstring))
            print('end_Month_Yearstring',end_Month_Yearstring,type(end_Month_Yearstring))
            start_Month_Year_gth = parse_datetime(start_Month_Yearstring)
            end_Month_Year_lth = parse_datetime(end_Month_Yearstring)    
            print('start_Month_Year_gth',start_Month_Year_gth,type(start_Month_Year_gth))
            print('end_Month_Year_lth',end_Month_Year_lth,type(end_Month_Year_lth))
            Device_Month_Year = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_Month_Year_gth, "$lt":end_Month_Year_lth},
                'device_id': ObjectId(device_ID)}
            ))
            Device_Month_Year_num = len(Device_Month_Year)
            print('Device_Month_Year_num',Device_Month_Year_num)
            
            Month_Year_sum =0
            for Month_Year_amounts in Device_Month_Year:
                deviceMonth_year_money = int(Month_Year_amounts['money'])
                print('deviceMonth_year_money',deviceMonth_year_money)
                Month_Year_sum = Month_Year_sum + deviceMonth_year_money
            sum_Month_year_Round = '{:.3f}'.format(Month_Year_sum)
            filter_num = Device_Month_Year_num
            filter_sum = sum_Month_year_Round
            print('filter_num from month and year',filter_num,filter_sum)
            return filter_num,filter_sum
            # return JsonResponse({'filter_num':Device_Month_Year_num,'filter_sum':sum_Month_year_Round})
        elif month:
            print("month",type(month),month)
            if month == '12':
                #year-12-01
                start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                #year-01-01
                end_string = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                
            else:
                #year-12-01
                start_string = str(this_year) + "-"  +  month + "-01"   + " 00:00:00"
                #year-01-01
                end_string = str(this_year)+ "-" + str(int(month)+1) + "-01"   + " 00:00:00"
            print('start_string',start_string,type(start_string))
            print('end_string',end_string,type(end_string))
            start_month_gth = parse_datetime(start_string)
            end_month_lth = parse_datetime(end_string)
            print('start_month_gth',start_month_gth,type(start_month_gth))
            print('end_month_lth',end_month_lth,type(end_month_lth))
                #dataBase
            Device_month = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_month_gth, "$lt":end_month_lth},
                'device_id':  ObjectId(device_ID)}
            ))
            Device_month_num = len(Device_month)
            print('Device_month_num',Device_month_num)
            
            month_sum =0
            for month_amounts in Device_month:
                devicemonth_money = int(month_amounts['money'])
                print('devicemonth_money',devicemonth_money)
                month_sum = month_sum + devicemonth_money
            sum_Month_Round = '{:.3f}'.format(month_sum)
            filter_num = Device_month_num
            filter_sum = sum_Month_Round
            print('filter_num from month and year',filter_num,filter_sum)
            return filter_num,filter_sum
            # return JsonResponse({'filter_num':Device_month_num,'filter_sum':sum_Month_Round})
            #if year from user
        elif year:
                print("year_from_user",type(year),year)
                start_Yearstring = year + "-01"  + "-01"   + " 00:00:00"
                #year-01-01
                end_Yearstring = str(int(this_year)+1) + "-01-01"   + " 00:00:00"
                print('start_Yearstring',start_Yearstring,type(start_Yearstring))
                print('end_Yearstring',end_Yearstring,type(end_Yearstring))
                start_Year_gth = parse_datetime(start_Yearstring)
                end_Year_lth = parse_datetime(end_Yearstring)
                print('start_Year_gth',start_Year_gth,type(start_Year_gth))
                print('end_Year_lth',end_Year_lth,type(end_Year_lth))
                Device_Year = list(db.get_database().transactions.find(
                {"datetime": {"$gte":start_Year_gth, "$lt":end_Year_lth},
                'device_id':  ObjectId(device_ID)}
                ))
                Device_Year_num = len(Device_Year)
                print('Device_Year_num',Device_Year_num)
            
                Year_sum =0
                for Year_amounts in Device_Year:
                    deviceyear_money = int(Year_amounts['money'])
                    print('deviceyear_money',deviceyear_money)
                    year_sum = Year_sum + deviceyear_money
                sum_year_Round = '{:.3f}'.format(year_sum)
                filter_num = Device_Year_num 
                filter_sum = sum_year_Round
                print('filter_num from month and year',filter_num,filter_sum)
                return filter_num,filter_sum
       
      
