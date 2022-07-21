import streamlit as st

from janome.tokenizer import Tokenizer
import pandas as pd
#import collections
#from wordcloud import WordCloud

file = 'pages/Hermann_Hesse.txt' 
f = open(file, 'r', encoding="utf-8")
text = f.read()

def text_split(text):
    # textをmarkovifyで読み取れるように前処理を行う関数です。
    
    # 引数：text
    # 引数の型：str
    
    # 戻り値：splitted_text_str
    # 引数の型：str
    
    # 今回は複数の文字列を一回で置換できるようにします。
    # maketransで置換する文字列の置き換え表を作成して、
    # str_tableという変数に入れる
    
    str_table = str.maketrans({
        # markovifyで読み取れるよう該当する文字の置換。
        # https://github.com/jsvine/markovify/issues/84
        # アンケートデータ内に「。」がついているものとついていないものがあります。
        # 表記を統一するため一旦、「。」を削除し、
        # 「'\n'」を「。」で置換する。文末が「。」で終わるように統一します。
        
        # 例：句点「。」がついているものと、ついていないものがあります。
        # 喉 越しが良いから。\n　自分に合っている\n
        # 。を削除　↓
        # 喉越しが良いから\n　自分に合っている\n
        #　\nを。で置換
        # 喉越しが良いから。　自分に合っている。
        
        #文字列の置き換え表　
        #変換前 : 変換後
        '。': '',   
        '\n': '。',
        '\r': '',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"':'”',
        "'":"’",
    })
    # 文字列をstr_tableの情報を用いて置換します。
    text = text.translate(str_table)
    
    # textを単語分割（文章を形態素で分ける）
    # wakati=Trueで分かち書き（単語分割）モードにできるのでこれを利用して、
    # 戻り値、文字列 (str) のリストを返します。
    # 例：['分かち書き', 'モード', 'が', 'つき', 'まし', 'た', '！']
    
    t = Tokenizer()
    tokens = t.tokenize(text, wakati=True)
    
    # splitted_text_listを用意します。
    splitted_text_list = []
    # 分かち書きされているtokensを一つずつ処理していき
    # 「。」や感嘆符でなければ、文字の後にスペース、
    # 「。」や感嘆符であれば、「'\n'」に置換
    # splitted_text_listに連結。
    # リストの要素を連結し、一つの文字列にして返します。
    for i in tokens:
        if i != '。' and i != '！' and i != '？':
            i += ' '
        elif i == '。' or i == '！' or i == '？':
            i = '\n'
        splitted_text_list.append(i)
        splitted_text_str = "".join(splitted_text_list)
            
    return splitted_text_str

import markovify
splitted_text_str = text_split(text)
text_model = markovify.NewlineText(splitted_text_str, state_size=3)

for i in range(5):
    st.write(text_model.make_sentence(tries=1000))
    st.write("---------------------------------")


st.caption("---------------------------------")


txt = st.text_area('Text to analyze', '''
     It was the best of times, it was the worst of times, it was
     the age of wisdom, it was the age of foolishness, it was
     the epoch of belief, it was the epoch of incredulity, it
     was the season of Light, it was the season of Darkness, it
     was the spring of hope, it was the winter of despair, (...)
     ''', height=50)
st.write('Sentiment:', text_split(txt))

if txt != None:
    splitted_txt_str = text_split(txt)
    txt_model = markovify.NewlineText(splitted_txt_str, state_size=3)
    for i in range(5):
        st.write(txt_model.make_sentence(tries=1000))
        st.write("---------------------------------")
