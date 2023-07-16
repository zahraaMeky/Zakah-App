from uuid import getnode as get_mac
import pymongo
from bson import objectid
from datetime import datetime

db = pymongo.MongoClient("conectio link")

device = None
charity = None
types   = None
sub_types = None

def add_device(passw , NAME, mac, charity_id_str=""):
	global db
	if (charity_id_str != ""): charity_id = objectid.ObjectId(charity_id_str)
	else: charity_id = ""

	devices = db.get_database().devices
	device = {"password":passw, "name":NAME, "mac": mac, "charity_id": charity_id, "start_date": datetime.now(), "last_maintenance": datetime.now(), "status": "0" }
	id = devices.insert_one(device).inserted_id
	#print(id)
	return id

def get_sub_types(ID):
	global sub_types, db
	sub_types = db.get_database().sub_types.find({'type_id': ID})

def get_types(ID):
	global types, db
	types = db.get_database().types.find({'charity_id': ID})

def get_charity(ID):
	global charity, db
	cha = db.get_database().charity
	charity = cha.find_one({'_id': ID})
	get_types(charity['_id'])

def find_device(name):
	global device, db
	devices = db.get_database().devices
	device = devices.find_one({"mac":name})
	#print(device)
	if (device != None): get_charity(device['charity_id'])
	else:
		add_device("1234" , "zakah", name, "")
		find_device(name)


mac = get_mac()
dev_mac = hex(mac).replace("0x", "")
print(dev_mac)

# add_device('111' , 'z', dev_mac)

find_device(dev_mac)
print("Decive: ", device)
print("Charity: ", charity)

print("Types: ")
types_count = 0
for type in types:
	types_count += 1
	print(type)
	get_sub_types(type['_id'])
	for sub in sub_types:
		print(sub)
	
print(types_count)

print("Charity Name : " , charity['name_ar'])

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

get_donate_type("61446eca9158dd0c75d73bcc" , 'en')






