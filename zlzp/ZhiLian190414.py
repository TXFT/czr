# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = Spider_zhilian
@file = ZhiLian190414.py
@author = TianChao
@time = 2019/04/14 09:23
@Description: 根据职位名和城市名爬取智联招聘上的职位信息，保存到CSV中，支持增量爬取
"""
import requests
import json
import math
import re
import pymongo
import csv
import pickle
import hashlib
import os
import datetime
from lxml import etree
from log import logger
import sys

city_names = ['石家庄']
job_names = ['数据分析']
if len(sys.argv) == 3:
    city_names[0] = sys.argv[1]
    job_names[0] = sys.argv[2]
else:
    print('命令行用法: '+ sys.argv[0] +' 待搜索城市 待搜索职位')
output_path = 'Output'

def load_progress(path):
    '''
    反序列化加载已爬取的URL文件
    :param path:
    :return:
    '''
    logger.info("load url file of already spider：%s" % path)
    try:
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
            return tmp
    except:
        logger.info("not found url file of already spider!")
    return set()

def save_progress(data, path):
    '''
    序列化保存已爬取的URL文件
    :param data:要保存的数据
    :param path:文件路径
    :return:
    '''
    try:
        with open(path, 'wb+') as f:
            pickle.dump(data, f)
            logger.info('save url file √!')
    except Exception as e:
        logger.error('save url file ×:',e)
def hash_url(url):
    '''
    对URL进行加密，取加密后中间16位
    :param url:已爬取的URLL
    :return:加密的URL
    '''
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return m.hexdigest()[8:-8]

def get_page_nums(cityname,jobname):
    '''
    获取符合要求的工作页数
    :param cityname: 城市名
    :param jobname: 工作名
    :return: 总数
    '''
    url = r'https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId={}&workExperience=-1&education=-1' \
          r'&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(cityname,jobname)
    logger.info('start get job count...')
    try:
        rec = requests.get(url)
        if rec.status_code==200:
            j = json.loads(rec.text)
            count_nums = j.get('data')['numFound']
            logger.info('get job count nums sucess:%s'%count_nums)
            page_nums = math.ceil(count_nums/60)
            logger.info('page nums:%s' % page_nums)
            return page_nums
    except Exception as e:
        logger.error('get job count nums ×:%s',e)
def get_urls(start,cityname,jobname):
    '''
    获取每页工作详情URL以及部分职位信息
    :param start: 开始的工作条数
    :param cityname: 城市名
    :param jobname: 工作名
    :return: 字典
    '''
    url = r'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId={}&workExperience=-1&education=-1' \
          r'&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(start,cityname,jobname)
    logger.info('spider start:%s',start)
    logger.info('get current page all job urls...')
    url_list=[]
    try:
        rec = requests.get(url)
        if rec.status_code == 200:
            j = json.loads(rec.text)
            results = j.get('data').get('results')
            for job in results:
                empltype = job.get('emplType')  # 职位类型，全职or校园
                if empltype=='全职':
                    url_dict = {}
                    url_dict['positionURL'] = job.get('positionURL') # 职位链接
                    url_dict['createDate'] = job.get('createDate') # 招聘信息创建时间
                    url_dict['updateDate'] = job.get('updateDate') # 招聘信息更新时间
                    url_dict['endDate'] = job.get('endDate') # 招聘信息截止时间
                    positionLabel = job.get('positionLabel')
                    if positionLabel:
                        jobLight = (re.search('"jobLight":\[(.*?|[\u4E00-\u9FA5]+)\]',job.get('positionLabel'))) # 职位亮点
                        url_dict['jobLight'] = jobLight.group(1) if jobLight else None
                    else:
                        url_dict['jobLight'] = None
                    url_list.append(url_dict)
        logger.info('get current page all job urls √:%s' % len(url_list))
        return url_list
    except Exception as e:
        logger.error('get current page all job urls ×:%s', e)
        return None
def get_job_info(url_list,old_url):
    '''
    获取工作详情
    :param url_list: 列表
    :return: 字典
    '''
    if url_list:
        for job in url_list:
            url = job.get('positionURL')
            h_url = hash_url(url)
            if not h_url in old_url:
                logger.info('spider url:%s'%url)
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        s = etree.HTML(response.text)
                        #print(response.text)
                        strScript = s.xpath('/html/body/script[6]/text()')[0]
                        #print(strScript)
                        strScript = strScript.replace('__INITIAL_STATE__=','')#整理该脚本赋值内容
                        #print(strScript)
                        djs=json.loads(strScript)
                        #print(djs['jobNumber'])
                        #print(djs['reportData'])
                        #print(djs['user'])
                        djs_jobInfo=djs['jobInfo']
                        #print(djs_jobInfo) #职位信息-主要-内容很长
                        djs_jobDetail=djs_jobInfo['jobDetail']
                        #print(djs_jobDetail)
#                        for i in djs_jobDetail:
#                            for j in djs_jobDetail[i]:
#                                print(i,j,djs_jobDetail[i][j])
                        djs_detailedCompany=djs_jobDetail['detailedCompany']
                        d_companyName = djs_detailedCompany['companyName'] #公司名称
                        d_url = djs_detailedCompany['url'] #公司链接
                        #djs_detailedPosition=djs_jobDetail['detailedPosition']
                        d_workAddress = djs_jobDetail['detailedPosition']['workAddress']  # 上班地址
                        d_cityDistrict = djs_jobDetail['detailedPosition']['cityDistrict'] #行政区
                        d_publishTime = djs_jobDetail['detailedPosition']['publishTime']  # 发布时间
                        d_education   = djs_jobDetail['detailedPosition']['education']  # 学历
                        d_salary60    = djs_jobDetail['detailedPosition']['salary60']  # 月薪
                        d_workingExp  = djs_jobDetail['detailedPosition']['workingExp']  # 经验
                        d_recruitNumber = djs_jobDetail['detailedPosition']['recruitNumber']  # 招聘人数
                        d_workCity    = djs_jobDetail['detailedPosition']['workCity']  # 城市
                        d_name = djs_jobDetail['detailedPosition']['name']  # 职业名
                        d_industry = djs_jobDetail['detailedCompany']['industry']  # 公司类型
                        d_companySize = djs_jobDetail['detailedCompany']['companySize']  # 公司总人数
#                       d_jobDescPC = djs_jobDetail['detailedPosition']['jobDescPC'].replace('<div>','').replace('</div>','')  # 岗位描述
                        print(d_publishTime, d_cityDistrict, d_companyName, d_salary60, d_name)
#                       # djsDtl=json.loads(djsDtl)
#                       # print(djsDtl)
                        logger.info('get job info success!')
                        old_url.add(h_url)
                        yield dict(d_companyName=d_companyName, d_url=d_url, d_workAddress=d_workAddress, d_cityDistrict = d_cityDistrict,
                                   d_publishTime=d_publishTime, d_education=d_education, d_salary60=d_salary60,
                                   d_workingExp=d_workingExp, d_recruitNumber=d_recruitNumber, d_workCity=d_workCity,
                                   d_name=d_name, d_industry=d_industry, d_companySize=d_companySize)#, d_jobDescPC=d_jobDescPC) #岗位描述不记录了,太长
                except Exception as e:
                    logger.error('get job info ×:',url,e)

headers = ['公司名称','公司链接','上班地址','行政区','发布时间','学历','月薪','经验','招聘人数','城市','职业名','公司类型','公司总人数']
def write_csv_headers(csv_filename):
    with open(csv_filename,'a',newline='',encoding='utf-8-sig') as f:
        f_csv = csv.DictWriter(f,headers)
        f_csv.writeheader()

def save_csv(csv_filename,data):
    with open(csv_filename,'a+',newline='',encoding='utf-8-sig') as f:
        f_csv = csv.DictWriter(f,data.keys())
        f_csv.writerow(data)

def main():
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for jobname in job_names:
        for cityname in city_names:
            logger.info('*'*10+'start spider '+'jobname:'+jobname+'city:'+cityname+'*'*10)
            total_page = get_page_nums(cityname,jobname)
            old_url = load_progress('old_url.txt')
            csv_filename=output_path+'/{0}_{1}.csv'.format(jobname,cityname)
            if not os.path.exists(csv_filename):
                write_csv_headers(csv_filename)
            for i in range(int(total_page)):
                urls = get_urls(i*60, cityname, jobname)
                data = get_job_info(urls, old_url)
                for d in data:
                    save_csv(csv_filename,d)
            save_progress(old_url,'old_url.txt')
            logger.info('*'*10+'jobname:'+jobname+'city:'+cityname+' spider finished!'+'*'*10)
if __name__=='__main__':
    start_time = datetime.datetime.now()
    logger.info('*'*20+"Start running spider!"+'*'*20)
    main()
    end_time = datetime.datetime.now()
    logger.info('*'*20+"spider done! Running time:%s"%(start_time-end_time) + '*'*20)
    print("Running time:%s"%(end_time - start_time))
