# scraping_wechat_himmr
# 微信征友平台HIMMR 嘉宾关键词分析

## 平台简介
HIMMR是2015年1月创立的，全国唯一一个只针对清华，北大，复旦，上海交大和海外顶尖高校在校生和校友的精品交友平台。
团队介绍：
月亮姐姐，清华本科，北大硕士；乐乐天使，清华本科，上海交大硕士。其余团队成员均来自于清北复交及海外名校。
平台定期发布清北复交及海外名校在校生和校友。
平台成立至今已发布400余位国内四大高校嘉宾和100多位海外名校嘉宾，脱单率始终维持在30%以上，
公众号平台总阅读量超过1000万，评论数超过13000+条，转发量超过32000次。

## 语言及工具
Python / Anaconda

## 主要工作

Connect
========
使用腾讯TBS Studio调试工具抓取小程序上的嘉宾信息页，并记录
http://bbs.mb.qq.com/thread-1416936-1-1.html
https://blog.csdn.net/yishengyouni95/article/details/80719281

Correct
========
* Requests包爬取网页内容
* BeautifulSoup4解析HTML，提取个人情况和所有网页文字信息
http://www.python-requests.org/en/master/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Collect
========
* 数据库使用sqlite3
* 使用SQLAlchemy建立、存储、查询数据
http://www.sqlalchemy.org/

Compose
========
* 使用jieba分词完成分词和统计分析
	* TF-IDF 算法
	* TextRank 算法
	* 词汇出现频率统计
https://github.com/fxsjy/jieba/

Consume
========
* 使用wordcloud生成词云
* 生成的demo图片为w_freq.png, w_textrank.png, w_tfidf.png
https://github.com/amueller/word_cloud

Control
========
* （可能的）后续工作：采用机器学习方法对嘉宾情况进行分类预测
