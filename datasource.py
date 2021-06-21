import ssl
import pymongo


client = pymongo.MongoClient("mongodb+srv://solutionsforeverything:halosfe00201@cluster0.luuxz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client['user_details']
collection = db['users']
collection1 = db['msg_from_users']

def addUser(uname , email ,passd):
    res = collection.find({"mail": email})
    if res.count() >= 1:
        return True
    else:
        collection.insert_one({"uname" : uname , "pass" : passd , "mail" : email, "college" : "--","gender" :"No gender selected"})
        return False



def addgooglesignin(email , uname , college , photo , passd):
      collection.insert_one({"uname" : uname , "mail" : email, "college" : college,"gender" :"No gender selected",'photo':photo , "pass" : passd})


def checkUser(email):
    res = collection.find({"mail" : email})

    if res.count() == 1 :
        return True
    else:
        return False

def checkLoginUser(email , passd):
    res = collection.find({"mail" : email , "pass" : passd})

    temp = []

    for result in res:
        temp.append(result)

    if res.count() >= 1 :
        return True , temp[0]['uname']
    else:
        return False , ""


def sentUserMsg(name , sub , msg , to):

    collection1.insert_one({"name" : name , "sub" : sub , "msg" : msg ,"to" : to})

def updatePassword(email , password):
    collection.update_one({"mail":email},{"$set":{"pass":password}})

def updateProfile(email , uname , college ,gender):
    collection.update_one({"mail":email},{"$set":{'uname': uname ,'college' : college ,'gender':gender}})

def getProfileDetails(email):
    res = collection.find({"mail" : email})

    temp = []

    for result in res:
        temp.append(result)
    try:
        if temp[0]['photo'] == None:
            temp[0]['photo'] = 'https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png'
    except:
        return temp[0]['uname'], temp[0]['college'], temp[0]['gender'],'https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png'

    return temp[0]['uname'],temp[0]['college'] ,temp[0]['gender'], temp[0]['photo']


def updatePhoto(email , photo):
    collection.update_one({"mail":email},{"$set":{"photo":photo}})