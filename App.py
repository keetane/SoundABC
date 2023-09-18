import streamlit as st
from playsound import playsound as ps
import pandas as pd
pd.set_option('display.max_columns', None)
import random
import glob
import datetime

# ゲームタイトル
st.title("Sound ABC")

# ゲームの選択@サイドバー
game = st.sidebar.selectbox("ゲームを選ぶ", glob.glob('games/*.csv'), index=4) #引数に入力内容を渡せる
df = pd.read_csv(game, index_col=0, parse_dates=True)
st.sidebar.divider()

st.dataframe(df.iloc[::-1])

# 遊べる音の設定
color_dic =  {
    '赤' : 'red',
    '黄' : 'yellow',
    '青' : 'blue',
    '黒' : 'black',
    'オレンジ' : 'orange',
    '紫' : 'purple',
    'ピンク' : 'pink',
    '緑' : 'green',
    '茶' : 'brown',
}
color_j = dict(zip(range(1,len(color_dic)+1), list(color_dic.keys())))
color_j[0] = 'もう一度聞く'
color_e = dict(zip(range(1,len(color_dic)+1), list(color_dic.values())))

# 新しいゲームの作成@サイドバー
st.sidebar.markdown('### 新しいゲームを作る')
new_game = st.sidebar.text_input('ゲームの名前は？')
new_button = st.sidebar.button('ゲームを作る')
if new_button:
    col = ['datetime'] + ['Today'] + ['session'] + ['Q'] + ['A'] + ['B']
    new = pd.DataFrame(columns=col)

    # 色をランダムに一つ選択して代入
    first =  random.choice(list(color_dic.keys()))
    new['Q'] = [first]

    # 日付を代入してDatetimeIndexに変更
    new['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new['datetime'] = pd.to_datetime(new['datetime'])
    new.set_index('datetime', inplace=True)
    new.to_csv('games/' + new_game + '.csv')
    st.sidebar.write(new_game + 'を作りました')
st.sidebar.divider()


# 遊ぶ音の選択
sounds = st.multiselect("遊ぶ音", list(color_dic.keys()), default=list(color_dic.keys())) #第一引数：リスト名、第二引数：選択肢、複数選択可

# 一つ前の色を除いたリストの作成
new_dict = [x for x in sounds if x != df['Q'].iloc[-1]]

# 一つ前の色を除いたリストの作成から色を一つ選択
second =  random.choice(list(new_dict))

# カラムの作成
col = ['Today'] + ['session'] + ['Q'] + ['A'] + ['B'] + ['datetime']
df2 = pd.DataFrame(columns=col)
# Rowの作成
df2['Q'] = [second]
# 時間をセット
df2['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df2['datetime'] = pd.to_datetime(df2['datetime'])
df2.set_index('datetime', inplace=True)

# 音を鳴らす
st.audio('sound/{}.mp3'.format(color_dic[df2['Q'].iloc[0]]))



# ここからおかしい
# 答える
answer = st.selectbox('こたえは', (sounds))
button = st.button('せいかいをみる')

if button:
    df2['A'].iloc[0] = answer
    if df2['Q'].iloc[0] == df2['A'].iloc[0] :
            df2['B'].iloc[0] = 'O'
            st.write('せいかい！')
    else :
       df2['B'].iloc[0] = 'X'
       st.write('ざんねん！' + second + 'です。')

st.dataframe(df2)
st.write(second)
st.write(new_dict)