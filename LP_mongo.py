__author__ = 'fangkuan'
import pymongo
from pymongo import MongoClient

occupation_list = []


def read_occupation_list():
    for line in open('./data/occupational category.txt'):
        occupation_list.append(line.strip())


def select_determin_user():
    client = MongoClient('localhost', 27017)
    db = client.test
    collection = db.userinfo
    results = collection.find({}, {'id': 1, 'name': 1, 'description': 1})

    userjob = db.userjob
    count = 0
    for user in results:
        ss = user['name']+','+user['description']
        uid = user['id']
        #print ss
        for job in occupation_list:

            if ss.count(job.decode('utf8')) > 1:
                record = {"id": uid, "job": job}
                userjob.insert(record)
        count += 1
        if count % 1000 == 0:
            print count

read_occupation_list()
select_determin_user()