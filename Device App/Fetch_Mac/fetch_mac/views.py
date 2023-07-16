from django.http import request
from django.shortcuts import render
from getmac import get_mac_address as gma
from django.contrib import messages

import pymongo
try:
    db = pymongo.MongoClient("connection link")
    print('connected')
except:
    db = None
def generateSerial():
    serial = "Z"
    devSerial =""
    AllDev=list(db.get_database().devices.find())
    num = 0
    if len(AllDev) == 0:
            num = 1
            devSerial =serial + "000" + str(num)
            print('devSerial',devSerial)
    else:
            sadd = str(num)
            num = len(AllDev)+1
            if (num%10==num):
                sadd = "000" + str(num)
            if (num%100==num):
                sadd = "00" + str(num)
            if (num%1000==num):
                sadd = "0" + str(num)
            else:
                sadd = str(num)
        
            devSerial =serial + sadd

            print('devSerial',devSerial)
    return(devSerial)

def get_mac(request):
    chec_mac = []
    devSerial =""
    charityuser=""
    devName=""
    mac_address = gma()
    if mac_address:
        chec_mac = db.get_database().devices.find_one({'mac': mac_address})
        if not chec_mac:
            devexit=0
            devSerial =  generateSerial()
            if request.method == 'POST':  
                print("device not exit")
                Device_name =  request.POST.get('DevName') 
                Device_password =  request.POST.get('DevPass') 
                charity_user =  request.POST.get('chname') 
                charity_password=  request.POST.get('chpass') 
                if not charity_user:
                 status = 0
                 charity_id = ""
                else:
                    find_charity_id=list(db.get_database().charity.find({'username': charity_user}))
                    if len(find_charity_id)>0:
                        encode_pass = charity_password.encode("utf_16")
                        for char in find_charity_id:
                            charity_id = char["_id"]
                            charity_pass = char["password"]
                            if charity_pass == encode_pass:
                                status =1
                                print('yes charity_pass == encode_pass: ',charity_pass)
                                print("postinfo",Device_name,Device_password)
                                Collection = {"Device_serial": devSerial,"name": Device_name, "password": Device_password,"mac":mac_address,"status":status,"charity_id":charity_id,"start_date":"","last_maintenance":""}
                                db.get_database().devices.insert_one(Collection)
                                print("device added")
                                messages.success(request,"device added")
                            else: 
                                print('No charity_pass == encode_pass: ',charity_pass)
                                messages.error(request,"Wrong Password")
                            print('charity_id',charity_id,type(charity_id))
                    else:
                        messages.error(request,"Wrong Charity User")
                    
                # print("postinfo",Device_name,Device_password)
                # Collection = {"Device_serial": devSerial,"name": Device_name, "password": Device_password,"mac":mac_address,"status":status,"charity_id":charity_id,"start_date":"","last_maintenance":""}
                # db.get_database().devices.insert_one(Collection)
                # print("device added")
                # messages.success(request,"device added")
        else:
            devexit =1
            getMac = db.get_database().devices.find({'mac': mac_address})
            for Dev in list(getMac):
                print('list(chec_mac)',list(chec_mac))
                devSerial = Dev['Device_serial']
                devName = Dev['name']
                charity_id = Dev['charity_id']
                find_charity_Name=list(db.get_database().charity.find({'_id': charity_id}))
                for charN in find_charity_Name:
                    charityuser = charN["username"]
                print('devSerial from db',devSerial,"charityuser",charityuser)
            print("device exit")
            messages.error(request,"Device Exit")
    context = {
        'mac_address':mac_address,
        'devSerial':devSerial,
        'charityuser':charityuser,
        'devexit':devexit,
        'devName':devName
    }
    return render(request,'index.html',context)

    # print("mac_address",mac_address)
    
    # if request.method == 'POST':  
    #     if not chec_mac:
    #         print("device not exit")
    #         Device_name =  request.POST.get('DevName') 
    #         Device_password =  request.POST.get('DevPass') 
    #         print("postinfo",Device_name,Device_password)
    #         Collection = {"Device_serial": devSerial,"name": Device_name, "password": Device_password,"mac":mac_address,"status":"0","charity_id":"","start_date":"","last_maintenance":""}
    #         db.get_database().devices.insert_one(Collection)
    #         print("device added")
    #         messages.success(request,"device added")
    #     else:
    #         print("device exit")
    #         messages.error(request,"Device Exit")
    # context = {
    #     'mac_address':mac_address,
    #     'devSerial':devSerial
    # }
    # return render(request,'index.html',context)

