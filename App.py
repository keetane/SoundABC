# https://qiita.com/papasim824/items/5910fdd462163c4012fc

import streamlit as st
import pandas as pd
pd.set_option('display.max_columns', None)
import random
import glob
import datetime

# ページのタイトル設定
st.set_page_config(
    page_title="Sound ABC",
)

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = "main"
    st.session_state.answers = []

# ゲームの選択@サイドバー
game = st.sidebar.selectbox("ゲームを選ぶ", glob.glob('games/*.csv'), index=4) #引数に入力内容を渡せる
st.sidebar.divider()

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

# 遊べる音の設定
color_dic =  {
    '赤' : 'red',
    '黄' : 'yellow',
    '青' : 'blue',
    '黒' : 'black',
    'オレンジ' : 'orange',
    '緑' : 'green',
    '紫' : 'purple',
    'ピンク' : 'pink',
    '茶' : 'brown',
}
color_j = dict(zip(range(1,len(color_dic)+1), list(color_dic.keys())))
color_j[0] = 'もう一度聞く'
color_e = dict(zip(range(1,len(color_dic)+1), list(color_dic.values())))


# 遊ぶ音の選択
sounds = st.sidebar.multiselect("遊ぶ音", list(color_dic.keys()), default=list(color_dic.keys())) #第一引数：リスト名、第二引数：選択肢、複数選択可
st.sidebar.divider()


# 最初のページ
def main():

    # ゲームタイトル
    st.title("Sound ABC")
    
    # DataFrame定義
    df = pd.read_csv(game, index_col=0, parse_dates=True)

    # 一つ前の色を除いたリストの作成
    new_dict = [x for x in sounds if x != df['Q'].iloc[0]]
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

    # dfを統合
    df = pd.concat([df2, df])
    df.to_csv(game)

    # 音を鳴らす
    st.audio('sound/{}.mp3'.format(color_dic[df['Q'].iloc[0]]))

    def change_page():
        st.session_state.answers.append(st.session_state.answer0)
        st.session_state.page_id = "page1"


    with st.form("f0"):
        st.radio("何色の音？", sounds, key="answer0")
        st.form_submit_button("答える", on_click=change_page)

# 答えのページ
def page1():
    def change_page():
        st.session_state.page_id = "main"

    df = pd.read_csv(game, index_col=0, parse_dates=True)

    # 答えを記載
    df['A'].iloc[0] = st.session_state.answers[-1]

    # 正誤判定
    if df['A'].iloc[0] == df['Q'].iloc[0]:
        df['B'] = 'O'
        st.markdown('# 正解！！')
    else:
        df['B'] = 'X'
        st.markdown('# 残念...' + df['Q'].iloc[0] + 'だよ')

    # Dataframeの保存
    df.to_csv(game)

    st.button("次の問題", on_click=change_page)


# ページ遷移のための判定
if st.session_state.page_id == "main":
    main()
if st.session_state.page_id == "page1":
    page1()