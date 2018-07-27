# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 21:27:36 2018

@author: cQ
"""

from bs4 import BeautifulSoup
import requests

__DATA_PATH__ = 'himmr_history.txt'


# create list of person info with raw data and title, extract from webpages
def create_raw_dict(data_path):
    # read original html file
    with open(data_path,"r") as f:
        html_str = f.read() 


    # create a beautifulsoup object
    soup = BeautifulSoup(html_str, "lxml")

    # find h4 tag, which contains guest information 
    list_h4 = soup.find_all('h4')

    # establist a list stored title and url of guest information
    list_info_origin = []
    
    for lh4 in list_h4:
        if 'hrefs' in str(lh4):
            if lh4.string:
                list_info_origin.append(dict(url=lh4['hrefs'], title=lh4.string.strip()))
            elif lh4.span.next_sibling:
                list_info_origin.append(dict(url=lh4['hrefs'], title=lh4.span.next_sibling.strip()))

    # filter friendmaking pages 
    list_info_filtered=[]
    
    for linfo in list_info_origin:
        if '陌上' in linfo['title']:
            list_info_filtered.append(linfo)
            
    return list_info_filtered
        
    
# a subfunciton used for droping the advertise contents in html
def subfunc_recognize_ad(list_p_span):
    if list_p_span.string:
        if ('How' in str(list_p_span)) \
        or ('打造' in str(list_p_span)) \
        or ('点击' in str(list_p_span)) \
        or ('发帖规则' in str(list_p_span)) \
        or ('二维码' in str(list_p_span)) \
        or ('付费' in str(list_p_span)) \
        or ('转发' in str(list_p_span)) \
        or ('赞赏' in str(list_p_span)):
            return True
        return False
    return True


# gather each page's personal information into a dict
def subfunc_sort_info(list_p_span, list_info_filtered):
    dict_personal_info = dict(sex=['性别'],
                              birth=['生日', '出生年月'],
                              school=['院校', '学校', '就读', '学历'],
                              subject=['方向', '专业', '学科'],
                              job=['工作', '职业'],
                              location=['坐标', '居住地', '所在地', '位置'],
                              hometown=['家乡', '籍贯'],
                              sign=['星座'],
                              height=['身高'])
    
    # drop blankspace
    str_p_span = ''.join(list_p_span.string.split())
    
    # for each info, when it's not empty then pass
    # 解析带有冒号的语句并归入各条目中，若条目中已有内容则跳过
    for key, value in dict_personal_info.items():
        if list_info_filtered['personal_info'][key] == '':
            for v in value:
                if (v in str_p_span) and ('：' in str_p_span):
                    list_info_filtered['personal_info'][key] = str_p_span[str_p_span.find('：')+1:]


# expand the dict, add related content and personal info
def fullfill_list_data(list_info):
    for lif in list_info:
        lif['content_line']=[]
        lif['content_all']=''
        lif['personal_info']=dict(sex='', birth='', school='', subject='', job='', location='', hometown='', sign='', height='')
        
        re = requests.get(url=lif['url'])   # get html from target url
        
        soupx = BeautifulSoup(re.text,'lxml')   # form a BeautifulSoup object
        
        # Since both span and p may contain personal info, 
        # try extract both of them and drop duplicates
        for list_span in soupx.find_all('span'):
            if list_span.string:
                if subfunc_recognize_ad(list_span):
                    continue
                lif['content_line'].append(''.join(list_span.string.split()))
                lif['content_all'] += ''.join(list_span.string.split())
                subfunc_sort_info(list_span, lif)
        
        for list_p in soupx.find_all('p'):
            if list_p.string:
                if subfunc_recognize_ad(list_p):
                    continue
                lif['content_line'].append(''.join(list_p.string.split()))
                lif['content_all'] += ''.join(list_p.string.split())
                subfunc_sort_info(list_p, lif)
    
    return list_info


def main(data_path):
    list_info_raw = create_raw_dict(data_path)
    # list_info_raw = list_info_raw[:10] # demo's mini size
    list_info_formatted = fullfill_list_data(list_info_raw)
    
    return list_info_formatted
    

if __name__ == '__main__':
    main(data_path=__DATA_PATH__)