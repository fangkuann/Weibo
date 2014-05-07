# coding=utf-8
__author__ = 'fangkuan'
import os
pathpre='d:/weibo.data/user/user/'
socialNet = {}

def readNetwork():
    for file in os.listdir(pathpre):
        print file
        for line in open(pathpre + file, 'r'):
            items = line.strip().split('，')
            uid1 = items[0]
            if uid1 not in socialNet:
                socialNet[uid1] = set([])
            if items[1] != '':
                followers = items[1].split('；')
                for user in followers:
                    socialNet[uid1].add(user)
            if items[2] != '':
                followees = items[2].split('；')
                for user in followees:
                    if user not in socialNet:
                        socialNet[user] = set([uid1])


readNetwork()