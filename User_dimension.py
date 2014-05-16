__author__ = 'fangkuan'
import pymongo
from pymongo import MongoClient
import collections
import scipy as sp
from scipy import stats
db_name = 'test'
dest = 'localhost'


client = MongoClient(dest, 27017)
db = client.db_name
userinfo = db.userinfo
relations = db.relations
user_dimension = db.user_dimension
user_high = db.user_high


def breadth(counter):
    total = sum(counter.values())
    pk = []
    for location in counter:
        pk.append(float(location[1]) / total)
    return sp.stats.entropy(pk, base=10)


def cal_high():
    verified_users = userinfo.find({'verified_type': 0}, {"id": 1})
    for user in verified_users:
        uid = user['id']
        followers_info = relations.find({'id': uid})
        if followers_info.count() > 0:
            followers = followers_info[0]['ids']
            for follower in followers:
                refollow_info = relations.find_one({"id": follower})
                if refollow_info.count() > 0:
                    for reuid in refollow_info['ids']:
                        if reuid == uid:
                            user_high.update({"id": follower}, {"$inc": {"high": 1}}, True)


def cal_dimensions():
    user_cursor = userinfo.find({}, {"id": 1, "province": 1, "city": 1, "location": 1})
    for user in user_cursor:
        uid = user["id"]
        province = int(user['province'])
        city = user['city']
        location = user["location"]
        followers = relations.find({"id": uid}, {"id": 1, "ids": 1})
        location_list = []
        if followers.count() > 0:
            for follower in followers:
                for followid in follower['ids']:
                    follower_location = userinfo.find_one({"id": followid}, {"id": 1, "province": 1, "city": 1, "location": 1, 'verified_type': 1})
                    if follower_location:
                        province = int(follower_location['province'])
                        verified = follower_location['verified_type']
                        if 90 > province >= 11 and verified == -1:
                            location_list.append(follower_location['location'])
        position = ""
        friend_location_breadth = -1
        if len(location_list) > 0:
            counter = collections.Counter(location_list)
            position = counter.most_common(1)[0][0]
            friend_location_breadth = breadth(counter)
        if 90 > province >= 11:
            post = {"id": uid, "location": location, "by_self": 1, "friend_location_breadth": friend_location_breadth}
            user_dimension.insert(post)
        else:
            post = {"id": uid, "location": position, "by_self": 0, "friend_location_breadth": friend_location_breadth}
            user_dimension.insert(post)

cal_dimensions()
cal_high()
