from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Organizations, Types, Sub_types, Transaction
import time
from threading import Thread
from .nv9biller import Biller
# from uuid import getnode as get_mac
from getmac import get_mac_address as get_mac
import pymongo
import requests
from bson import objectid
from datetime import datetime
from django.utils import timezone

try:
    db = pymongo.MongoClient("conection lik")
except:
    db = None

device = None
charity = None
types = None
sub_types = None

charity_local = None
types_local = None
sub_types_local = None

accepted = False
money = 0
port = 'COM5'
Stop = False
sub_ = None
dev_mac = get_mac()
# dev_mac = hex(mac).replace("0x", "")
print(dev_mac)

tz = timezone.now()
dt = timezone.datetime.now()
print("timezone: ", tz)
print("datetime: ", dt)

def add_device(passw, NAME, mac):
    global db
    devices = db.get_database().devices
    device = {"password": passw, "name": NAME, "mac": mac}
    id = devices.insert_one(device).inserted_id
    # print(id)
    return id


def get_sub_types(ID):
    global sub_types, db,sub_types_local
    #writen first
    # sub_types = db.get_database().sub_types.find({'type_id': ID})

    #witen by me 
    sub_types = db.get_database().charity_subtypes.find({'charity_id': ID})
    sub_types_list = list(sub_types)
    print("Number of subtypes: ", len(sub_types_list))
    if  len(sub_types_list) > 0:
        Sub_types.objects.all().delete()
        for sub in sub_types_list:
            print('sub',sub)
            sub= Sub_types(sub_type_ar = sub['sub_type_ar'],sub_type_en = sub['sub_type_en'],type_id = sub['type_id'],sub_id = sub['_id'])
            sub.save()


def get_types(ID):
    global types, db, types_local
    types = db.get_database().types.find({'charity_id': ID})
    print("types: " , types)

    types_local = list(types)
    if (len(types_local)>0): 
        print("delete all types")
        Types.objects.all().delete()
        Sub_types.objects.all().delete()
    print("local types: ", types_local)

    for type in types_local:
            print(type)
            tp = Types()
            tp.type_ar = type['type_ar']
            tp.type_en = type['type_en']
            tp.charity_id = type['charity_id']
            tp._id = type['_id']
            tp.type_id = type['type_id']
            print(' tp.type_id', tp.type_id)
            tp.save()

            # sub_types = db.get_database().sub_types.find({'type_id': type['_id']})
            # print('sub_types from :',list(sub_types))

            # for sub in list(sub_types):
            #     print(sub)
            #     sp = Sub_types()
            #     sp.sub_type_ar = sub['sub_type_ar']
            #     sp.sub_type_en = sub['sub_type_en']
            #     sp.type_id = sub['type_id']
            #     sp.sub_id = sub['_id']
            #     sp.save()


def get_charity(ID):
    global charity, db
    cha = db.get_database().charity
    charity = cha.find_one({'_id': ID})
    print(charity)
    get_types(charity['_id'])
    #writen by me 
    get_sub_types(charity['_id'])


def find_device(name):
    global device, db
    devices = db.get_database().devices
    device = devices.find_one({"mac": name})
    print(device)
    if (device != None): get_charity(device['charity_id'])
    else:
        orgs = Organizations.objects.first()
        print("orgs device : ", orgs.device_id)
        device = devices.find_one({"_id": orgs.device_id})
        print("device : ", device)

def check_internet():
    url = "http://www.google.com"
    timeout = 3
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False

def add_transaction(type , money, tr_id, dt):
	global db, device
	transactions = db.get_database().transactions
	transaction = {"trans_id": tr_id ,"type":type, "money":money, "datetime":dt, "device_id":device['_id']}
	id = transactions.insert_one(transaction).inserted_id
	return id

def get_donate_type2(id_str , lang):
    t = Types.objects.filter(type_id = id_str)
    print(t)
    if (t.exists()):
        if (lang == "en"): ty = t[0].type_en
        else: ty = t[0].type_ar
    else:
        s = Sub_types.objects.filter(sub_id = id_str)
        print(s)
        if (lang == "en"): ty = s[0].sub_type_en
        else: ty = s[0].sub_type_ar
    
    print("donate type : ", ty)
    return ty

def get_donate_type(id_str , lang):
	ID = objectid.ObjectId(id_str)
	t = list(db.get_database().types.find({'_id': ID}))
	print(t)
	if (len(t) > 0):
		ty = t[0]['type_' + lang]
	else:
		s = list(db.get_database().sub_types.find({'_id': ID}))
		ty = s[0]['sub_type_' + lang]

	print("donate type : ", ty)
	return ty

# view for index.html
def index(request):
    global dev_mac, charity, device, charity_local, Stop
    Stop = True
    
    if (check_internet()):
        find_device(dev_mac)
        if (device != None):
            Organizations.objects.all().delete()
            ch=Organizations()
            ch.device_id = device['_id']
            ch.charity_id = charity['_id']
            ch.name_ar = charity['name_ar']
            ch.name_en = charity['name_en']
            ch.phone    = charity['phone']
            ch.website  = charity['website']
            #ch.logo     = charity['logo']
            ch.city     = charity['city']
            ch.get_remote_image(charity['logo'])
            ch.save()

    orgs = Organizations.objects.first()
    print(orgs.logo)
    charity_local = orgs
    if ('media' not in charity_local.logo): charity_local.logo = "media/" + str(charity_local.logo)

    context = {
        'title': 'Welcome',
        'charity': charity_local
    }
    return render(request, 'index.html', context)

def zakah_types(request):
    global dev_mac, charity, types, Stop, charity_local, types_local, sub_types_local, sub_
    sub_ = None
    Stop = True
    if (check_internet()): find_device(dev_mac)
 
    # if (check_internet()):
    #     # update 
    #     types_local = list(types)
    #     for type in types_local:
    #         tp = Types()
    #         tp.type_ar = type['type_ar']
    #         tp.type_en = type['type_en']
    #         tp.charity_id = type['charity_id']
    #         tp.type_id = type['_id']
    #         tp.save()
    
    print("tp : " , Types.objects.all())
    types_local = list(Types.objects.all())
    print("tp : " , types_local)

    if request.method == 'POST':
        slug = request.POST['slug']
        if len(slug) > 0:
             print("slug here: " , slug)
             try:
                #_type = db.get_database().types.find({'type_ar': slug})
                #sub_types = list(db.get_database().sub_types.find({'type_id': _type[0]['_id']}))
                #sub_types = list(db.get_database().sub_types.find({'type_id': objectid.ObjectId(slug)}))
                sub_types_local = list(Sub_types.objects.filter(type_id=slug))
                # print(sub_types)
             except:
                _type = None
                sub_types_local = None
                print("_type None")
             if (sub_types_local==None or len(sub_types_local)==0):
                print("zakah_type_Donate")
                # return redirect('/zakah_sub_Donate?slug=' + str(_type[0]['_id']))
                # return redirect('/zakah_sub_Donate/' + str(_type[0]['_id']))
                return zakah_Sub_types(request)

             else:
                print("zakah_Sub_types")
                #return redirect('/zakah_sub_type')
                return zakah_Sub_types(request)
        #else:
        #    print("slug not here")
        #    return redirect('/zakah_sub_Donate')
            #return zakah_sub_Donate(request)

    # json = []
    # for type in local_types:
    #     print(type)
    #     json.append({'id': type['_id'],
    #                  'type_ar': type['type_ar'],
    #                  'type_en': type['type_en']})

    charity_local.logo = "../" + str(charity_local.logo)

    context = {
        "title": "Type",
        "types_of_zakah": types_local,
         'charity': charity_local
    }

    print("types context: ", context)

    return render(request, 'zakah_type.html',context)


# view for zakah_type
def zakah_Sub_types(request):
    global sub_types, Stop, sub_types_local, charity_local, sub_
    sub_ = None
    Stop = True
    sub_types = None

    if request.method == 'POST':
        slug = request.POST['slug']
        print("slg: ", slug)
        if len(slug) >0:
            try:
                
                # if (check_internet()):
                #     sub_types = list(db.get_database().sub_types.find({'type_id': objectid.ObjectId(slug)}))
                #     # update 
                #     sub_types_local = list(sub_types)
                #     for sub in sub_types_local:
                #         sp = Sub_types()
                #         sp.sub_type_ar = sub['type_ar']
                #         sp.sub_type_en = sub['type_en']
                #         sp.type_id = sub['type_id']
                #         sp.sub_id = sub['_id']
                #         sp.save()
                
                sub_types_local = list(Sub_types.objects.filter(type_id = slug))
            except:
                _type = None
                print("_type None")
    
    print("sub:" , sub_types_local )
    i = 0
    # json = []
    # for sub in sub_types:
    #     # print(sub)
    #     i += 1
    #     json.append({'id' : sub['_id'],
    #                  'sub_type_ar': sub['sub_type_ar'],
    #                  'sub_type_en': sub['sub_type_en'],
    #                  'type_id': sub['type_id'] })
    
    if len(sub_types_local) == 0:
        print("Donate")
        request.session['post'] = request.POST
        return HttpResponseRedirect('/zakah_sub_Donate/')
        # return zakah_sub_Donate(request)

    context = {
        "title": "subTypes",
        'sub_types': sub_types_local,
         'charity': charity_local,
    }
    print('sub_types ')
    return render(request, 'zakah_sub_type.html',context)


def encode_money(value):
    money_value = value / 1000.0
    return money_value


def biller_main():
    global accepted, money, port, Stop
    print("Start Biller")
    try:
        biller = Biller(port)
        print('-------------------')
        print('Cash Validator program')
        print('SN: {:08X}'.format(biller.serial))
        print('--------------------')

        print('Enable Validator...')
        biller.channels_set(biller.CH_ALL)
        biller.display_enable()
        biller.enable()

        money = 0

        print('insert some money (Ctrl+C to quit)')
        while True:
            try:
                events = biller.poll()

                if (Stop):
                    biller.display_disable()
                    biller.disable()
                    Stop = False
                    break
                if (len(events) == 0): continue
                # print(len(events))
                accepted = False
                for event in events:
                    if (event.code == 0xEE):
                        money += encode_money(event.channel.value)
                        accepted = True

                if (accepted):
                    print("Accepted")
                    print("Money : ", money)
                    # break
                # else:
                #    print("Rejected!")

                time.sleep(0.5)

            except KeyboardInterrupt:
                break

        print('Disabling biller...')
        biller.disable()
        biller.display_disable()
        biller.channels_set(None)
    except: pass



# donate view for zakah sub type
def zakah_sub_Donate(request):
    global money, sub_, db, Stop, charity_local
    money_ = 0

    if request.method == 'POST':
        try:
            print('request.POST',request.POST)
            slug = request.POST['slug']
            print("slug zakah_sub_Donate : " , slug)
            sub_ = slug
            #_donate_type = db.get_database().sub_types.find({'sub_type_ar':slug})
            #print("donate_type: ", _donate_type, "   , " , len(_donate_type))
            #if (len(_donate_type) == 0):
            #    print("noooo")
            #    _donate_type =  dict(db.get_database().types.find({'type_ar': slug}))
            #    print("donate_type: ", _donate_type)
            #sub_ = str(_donate_type['_id'])
            print("sub: ", sub_)
        except:
            try:
                if (sub_==None):
                    print("get post")
                    post = request.session.get('post')
                    print("post: ", post)
                    slug = post['slug']
                    print("post slug : ", slug)
                    if (len(slug) > 10): sub_ = slug
                    print("post sub_: ", sub_)
            except:
                pass
        print("money")

        try:
            money = request.POST['amount']
        except:pass
        try:
            finish = request.POST['finish']
            if (len(finish) > 0):
                if (money == 0):
                    messages.warning(request, 'Please Enter money')
                    messages.warning(request, 'من فضلك ادخل مبلغ')
                else:
                    money_ = money
                    money = 0
                    Stop = True

                    print(f'the amount money{money_}')
                    id = None
                    if(check_internet()): 
                        tr = Transaction.objects.all()
                        if (tr.exists()):
                            for t in tr:
                                add_transaction(objectid.ObjectId(t.type), t.money, t.trans_id, t.datetime)
                        Transaction.objects.all().delete()

                        trans_id = datetime.now().strftime("%Y%m%d%H%M%S")
                        add_transaction(objectid.ObjectId(sub_), money_, trans_id, datetime.now())
                        id = trans_id
                    else:
                        trans = Transaction()
                        trans.type = sub_
                        trans.money = money_
                        trans.trans_id = datetime.now().strftime("%Y%m%d%H%M%S")
                        trans.device_id = charity_local.device_id
                        trans.datetime  = datetime.now()
                        trans.save()
                        id = trans.trans_id
                    return zakah_thanks(request, money_, sub_, id, datetime.now())

        except: pass

        #if (money > 0):
        #    money_ = money
        #    money = 0
        #    Stop = True
        #    print(f'the amount money{money_}')
        #    add_transaction(sub_, money_)
        #    return zakah_thanks(request, money_, sub_)

    context = {
        "title": "Donate",
         'charity': charity_local
    }

    print("Before Thread")
    Stop = False
    Thread(target=biller_main, args=()).start()
    print("After Thread")
    return render(request, 'donate_money.html', context)


def zakah_thanks(request, donate_money, type, id, donate_datetime):
    global charity, Stop, charity_local
    Stop = True
    print(f'the amount money{donate_money}')
    
    donate_type = get_donate_type2(str(type), 'en')

    dt = donate_datetime.strftime('%Y-%m-%d %I:%M:%S %p')

    context = {
        "title": "Thanks",
        'logo': charity_local.logo,
        'name': charity_local.name_en,
        'money': donate_money,
        'type' : donate_type,
        'tr_id' : str(id),
        'phone' : charity_local.phone,
        'web': charity_local.website,
        'datetime' : dt
    }
    print(context)
    return render(request, 'zakah_thanks.html', context)

def get_money(request):
    global money
    return JsonResponse({"money": str(money)})
