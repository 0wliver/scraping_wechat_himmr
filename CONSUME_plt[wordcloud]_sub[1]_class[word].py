# -*- coding: utf-8 -*-

from PreProcess import COMPOSE_CutCountWord

import wordcloud


__DB_PATH__ = './data/himmr.db'
__DATA_PATH__ = './data/himmr_history.txt'
__FONT_PATH__ = 'C:/Windows/Fonts/msyh.ttc'


df_word_tfidf, df_word_textrank, df_word_freq = COMPOSE_CutCountWord.main(db_path=__DB_PATH__)

df_word_tfidf = df_word_tfidf.iloc[0:500,:]
df_word_textrank = df_word_textrank.iloc[0:500,:]
df_word_freq = df_word_freq.iloc[0:500,:]


df_word_tfidf.set_index(keys=df_word_tfidf['word'], inplace=True)
df_word_textrank.set_index(keys=df_word_textrank['word'], inplace=True)
df_word_freq.set_index(keys=df_word_freq['word'], inplace=True)

dict_word_tfidf = df_word_tfidf.to_dict()['weight']
dict_word_textrank = df_word_textrank.to_dict()['weight']
dict_word_freq = df_word_freq.to_dict()['weight']

wc_tfidf = wordcloud.WordCloud(width=1600,
                         height=900,
                         max_font_size=320,
                         min_font_size=30,
                         font_path=__FONT_PATH__,
                         collocations=False,
                         background_color='white')
# colormap='BuGn' https://matplotlib.org/examples/color/colormaps_reference.html
# stopwords=stop_word: Ignored if using generate_from_frequencies.

# can also use .generate(mytext) to count frequncy in auto
w_tfidf = wc_tfidf.generate_from_frequencies(dict_word_tfidf) # .fit_words(dict_word_freq_500)
wc_tfidf.to_file('w_tfidf.png')


wc_textrank = wordcloud.WordCloud(width=1600,
                         height=900,
                         max_font_size=320,
                         min_font_size=30,
                         font_path=__FONT_PATH__,
                         collocations=False,
                         background_color='white',
                         colormap='plasma')
w_textrank = wc_textrank.generate_from_frequencies(dict_word_textrank)
wc_textrank.to_file('w_textrank.png')

wc_freq = wordcloud.WordCloud(width=1600,
                         height=900,
                         max_font_size=320,
                         min_font_size=30,
                         font_path=__FONT_PATH__,
                         collocations=False)
w_freq = wc_freq.generate_from_frequencies(dict_word_freq)
wc_freq.to_file('w_freq.png')

# plt.imshow(w_tfidf, interpolation='bilinear')
# plt.axis("off")
# plt.imshow(w_textrank, interpolation='bilinear')
# plt.axis("off")
# plt.imshow(w_freq, interpolation='bilinear')
# plt.axis("off")


