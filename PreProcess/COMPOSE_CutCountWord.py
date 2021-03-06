# -*- coding: utf-8 -*-

from PreProcess import COLLECT_SaveLoadDB

import pandas as pd
import jieba
import jieba.analyse

__DB_PATH__ = '../data/himmr.db'
__DATA_PATH__ = '../data/himmr_history.txt'

#######################  GET DATA & STORE DATABASE    #######################
'''
from PreProcess import CONNECT_GetHtmlData

# get data
list_info = CONNECT_GetHtmlData.main(data_path=__DATA_PATH__)

# save to database
COLLECT_SaveLoadDB.save_to_path(list_info=list_info, db_path=__DB_PATH__)
'''

################################# word count #################################

def jieba_count(result):
    df_tfidf = pd.DataFrame()
    df_textrank = pd.DataFrame()
    df_freq = pd.DataFrame()
    
    
    for r in result:
        print('COUNT WORD:'+ r.title)
        sentence = r.content
        wordlist_tfidf = jieba.analyse.extract_tags(sentence, 
                                                    topK=500, 
                                                    withWeight=True,
                                                    allowPOS=('n', 's', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vd', 'vn', 'a', 'ad', 'an'))

        # allowPOS=('ns', 'n', 'vn', 'v', 'a', 'ad', 'an')
    
        wordlist_textrank = jieba.analyse.textrank(sentence, 
                                                   topK=500, 
                                                   withWeight=True,
                                                   allowPOS=('n', 's', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vd', 'vn', 'a', 'ad', 'an'))
    
        wordlist_freq = jieba.analyse.extract_tags(sentence, 
                                                   topK=500, 
                                                   withWeight=False,
                                                   allowPOS=('n', 's', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vd', 'vn', 'a', 'ad', 'an'))
        
        if df_tfidf.empty:
            df_tfidf = pd.DataFrame(wordlist_tfidf)
            df_textrank = pd.DataFrame(wordlist_textrank)
            df_freq = pd.DataFrame(wordlist_freq)
            df_freq[1] = 1
        else:
            df_temp_tfidf = pd.DataFrame(wordlist_tfidf)
            df_temp_textrank = pd.DataFrame(wordlist_textrank)
            df_temp_freq = pd.DataFrame(wordlist_freq)
            df_temp_freq[1] = 1
            
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
    list_useless_a = ['性别', '生日', '出生年月', '院校', '学校',
                      '就读', '学历', '大学', '方向', '专业', '学科',
                      '工作', '职业', '坐标', '居住地', '所在地',
                      '位置', '家乡', '籍贯', '星座', '身高', '兴趣爱好']
    list_useless_b = ['心目', '觉得', '时候', '没有', '自我介绍', 
                      '作为', '评价', '最好', '嘉宾', '充满', 
                      '事情', '不会', '基本', '地方', '发现', 
                      '可能', '妹子', '开始', '找到', '成为',
                      '重要', '能够', '姑娘', '还有', '愿意',
                      '对方', '期待', '好友', '喜欢', '有点',
                      '人生', '相当', '遇到', '大家', '身边',
                      '经历', '信息', '问题', '女生', '男生', 
                      '希望', '女神', '希望', '家庭', '性格',
                      '起来', '事物', '东西', '来自', '妹纸',
                      '应该', '方面', '拥有', '有着', '属于',
                      '女孩', '要求', '小喇叭', '复旦大学']
    list_useless = list_useless_a + list_useless_b
    
    return df_word[~df_word['word'].isin(list_useless)]


def main(db_path):
    # get db query handler
    session = COLLECT_SaveLoadDB.load_from_path(db_path=db_path)
    result = session.query(COLLECT_SaveLoadDB.Person).all()   # 引用类时要有模块名, demo size:[:10]

    df_word_tfidf, df_word_textrank, df_word_freq = jieba_count(result)
    
    df_word_tfidf = filter_useless_word(df_word_tfidf)
    df_word_textrank = filter_useless_word(df_word_textrank) 
    df_word_freq = filter_useless_word(df_word_freq) 
    
    return df_word_tfidf, df_word_textrank, df_word_freq


if __name__ == '__main__':
    df_word_tfidf, df_word_textrank, df_word_freq = main(db_path=__DB_PATH__)
    
    
    


