import ssl
import pymongo


client = pymongo.MongoClient("mongodb+srv://solutionsforeverything:halosfe00201@cluster0.ssywa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client['blogs']
collection = db['blog_details']
collection1 = db['project_details']
collection2 = db['proj_list']
collection3 = db['blog_list']


def add(name , image , desc):
    collection.insert_one({"name" : name , "image" : image , "desc" : desc})

def getdetails(name):

        res = collection.find({"name": name})

        temp = []

        for result in res:
            temp.append(result)

        return temp[0]['image'], temp[0]['desc']


def addProject(name , image , desc ,url):
    collection1.insert_one({"name" : name , "image" : image , "desc" : desc , "url" : url})

# def getProjDetails(name):
#
#         res = collection1.find({"name": name})
#
#         temp = []
#
#         for result in res:
#             temp.append(result)
#
#         return temp[0]['image'], temp[0]['desc']

def search(search):
    if search == 'xyxz':
        res =  collection1.find()
    else:
        res = collection1.find({ "$or": [ { "name": { "$regex" : search+'.*', "$options" : 'i' }} , {"desc": { "$regex" : search+'.*', "$options" : 'i' } }] } )

    temp = []

    for result in res:
        temp.append(result)
    return temp

def adduserprojects(email , pname , pdesc , purl):
    collection2.insert_one({"email": email, "name": pname, "desc": pdesc, "url": purl})

def addBlogList(name , desc , email):
    collection3.insert_one({"email" : email , "name" : name , "desc" : desc})