# coding=utf-8
__author__ = 'fangkuan'
import os
jobs = []
pre = 'http://weibo.com/'
pathpre='d:/weibo.data/info/info/'
uidset = set([])
def readJobs():
    global jobs
    for line in open('../CvAnalysis/data/job_merge.txt', 'r'):
        jobs += line.strip().split('\t')



def filter_weibo_user():
    fout = open('./user_job.txt','w')
    for file in os.listdir(pathpre):
        print file
        for line in open(pathpre + file ,'r'):
            items = line.split('，')
            ss = items[1] + items[11]
            ss = ss.lower()
            if items[0] in uidset:
                continue
            uidset.add(items[0])
            for job in jobs:
                if ss.find(job) != -1:
                    #print ss,'\t',job,'\t',items[8],'\t',pre+items[0]
                    fout.write(ss+'\t'+job+'\t'+items[8]+'\t'+pre+items[0]+'\n')

readJobs()
filter_weibo_user()