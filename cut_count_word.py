# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 21:52:37 2018

@author: cQ
"""

import pandas as pd


import operate_data_db
import jieba
import jieba.analyse

__DB_PATH__ = 'himmr.db'
__DATA_PATH__ = 'himmr_history.txt'

#######################  GET DATA & STORE DATABASE    #######################
'''
import pick_origin_data

# get data
list_info = pick_origin_data.main(data_path=__DATA_PATH__)

# save to database
operate_data_db.save_to_path(list_info=list_info, db_path=__DB_PATH__)
'''


################################# word count #################################

def jieba_count(result):
    df_tfidf = pd.DataFrame()
    df_textrank = pd.DataFrame()
    df_freq = pd.DataFrame()
    
    
    for index, r in enumerate(result):
        print('COUNT WORD:'+ r.title)
        sentence = r.content
        wordlist_tfidf = jieba.analyse.extract_tags(sentence, 
                                                    topK=500, 
                                                    withWeight=True,
                                                    allowPOS=('ns', 'n', 'vn', 'v', 'a', 'ad', 'an'))
    
        wordlist_textrank = jieba.analyse.textrank(sentence, 
                                                   topK=500, 
                                                   withWeight=True,
                                                   allowPOS=('ns', 'n', 'vn', 'v', 'a', 'ad', 'an'))
    
        wordlist_freq = jieba.analyse.extract_tags(sentence, 
                                                   topK=500, 
                                                   withWeight=False,
                                                   allowPOS=('ns', 'n', 'vn', 'v', 'a', 'ad', 'an'))
    
        df_temp_tfidf = pd.DataFrame(wordlist_tfidf)
        df_temp_textrank = pd.DataFrame(wordlist_textrank)
        df_temp_freq = pd.DataFrame(wordlist_freq)
        df_temp_freq[1] = 1
        
        if not index:
            df_tfidf = df_temp_tfidf
            df_textrank = df_temp_textrank
            df_freq = df_temp_freq
            
        if index < len(result):
            df_tfidf = pd.merge(df_tfidf, df_temp_tfidf, left_on=0, right_on=0, how='outer')
            df_textrank = pd.merge(df_textrank, df_temp_textrank, left_on=0, right_on=0, how='outer')
            df_freq = pd.merge(df_freq, df_temp_freq, left_on=0, right_on=0, how='outer')    
    
    # drop null
    df_tfidf.fillna(value=0, axis=1, inplace=True)
    df_textrank.fillna(value=0, axis=1, inplace=True)
    df_freq.fillna(value=0, axis=1, inplace=True)
    
    # create new dataframe
    df_tfidf_count = pd.DataFrame()
    df_textrank_count = pd.DataFrame()
    df_freq_count = pd.DataFrame()
    
    # set new dataframe's columns
    df_tfidf_count['word'] = df_tfidf[0]
    df_textrank_count['word'] = df_textrank[0]
    df_freq_count['word'] = df_freq[0]
    
    df_tfidf_count['weight'] = df_tfidf.sum(axis=1)
    df_textrank_count['weight'] = df_textrank.sum(axis=1)
    df_freq_count['weight'] = df_freq.sum(axis=1)
    
    # sort by weight
    df_tfidf_count.sort_values(by=['weight'], inplace=True, ascending=False)
    df_textrank_count.sort_values(by=['weight'], inplace=True, ascending=False)
    df_freq_count.sort_values(by=['weight'], inplace=True, ascending=False)
    
    return df_tfidf_count, df_textrank_count, df_freq_count

    # origin jieba cut
    # seg_list = jieba.cut(result[0].content, cut_all=False)
    # print("Default Mode: " + "/".join(seg_list))  # 精确模式
  

def filter_useless_word(df_word):
    list_useless = ['性别', '生日', '出生年月', '院校', '学校',
                    '就读', '学历', '方向', '专业', '学科',
                    '工作', '职业', '坐标', '居住地', '所在地',
                    '位置', '家乡', '籍贯', '星座', '身高', '兴趣爱好']
    
    return df_word[~df_word['word'].isin(list_useless)]


def main(db_path):
    # get db query handler
    session = operate_data_db.load_from_path(db_path=db_path)
    result = session.query(operate_data_db.Person).all()   # 引用类时要有模块名, demo size:[:10]

    return jieba_count(result)


if __name__ == '__main__':
    df_word_tfidf, df_word_textrank, df_word_freq = main(db_path=__DB_PATH__)
    
    df_word_tfidf = filter_useless_word(df_word_tfidf)
    df_word_textrank = filter_useless_word(df_word_textrank) 
    df_word_freq = filter_useless_word(df_word_freq) 
    
    


