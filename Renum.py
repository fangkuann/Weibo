# coding=utf-8
__author__ = 'fangkuan'
import os
userDic  ={}
prePath = 'd:/weibo.data/user/user/'
infoPath = 'd:/weibo.data/info/info/'
writePath = 'd:/weibo.data/new_user/'

def renum():
    count = 1
    for file in os.listdir(prePath):
        print file
        for line in open(prePath + file):
            items = line.strip().split('，')
            uid1 = items[0]
            if uid1 not in userDic:
                userDic[uid1] = count
                count += 1
            if items[1] != '':
                followers = items[1].split('；')
                for user in followers:
                    if user not in userDic:
                        userDic[user] = count
                        count += 1
            if items[2] != '':
                followees = items[2].split('；')
                for user in followees:
                    if user not in userDic:
                        userDic[user] = count
                        count += 1

    for file in os.listdir(infoPath):
        print file
        for line in open(infoPath + file):
            uid = line.strip().split('，')[0]
            if uid not in userDic:
                userDic[uid] = count
                count += 1

def write_new_file():
    fout = open('./new_user_job.txt','w')
    for line in open('./user_job.txt'):
        uid = line.strip().split('\t')[-1].split('/')[-1]
        job = line.strip().split('\t')[-3]
        new_uid = userDic[uid]
        fout.write(str(new_uid)+'\t'+job+'\n')
    fout.flush()
    fout.close()

    for file in os.listdir(prePath):
        print file
        fout = open(writePath+file, 'w')
        for line in open(prePath + file):
            items = line.strip().split('，')
            uid1 = items[0]
            fout.write(str(userDic[uid1])+';')
            if items[1] != '':
                followers = items[1].split('；')
                new_followers = []
                for user in followers:
                    new_followers.append(str(userDic[user]))
                fout.write(','.join(new_followers))
            fout.write(';')
            if items[2] != '':
                followees = items[2].split('；')
                new_followees = []
                for user in followees:
                    new_followees.append(str(userDic[user]))
                fout.write(','.join((new_followees)))
            fout.write('\n')
renum()
print len(userDic)
write_new_file()