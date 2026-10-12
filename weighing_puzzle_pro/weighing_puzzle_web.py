import streamlit as st
import random
import os
from streamlit.components.v1 import declare_component

# ページの基本設定
st.set_page_config(page_title="天秤パズル Pro", layout="centered")

# --- カスタムコンポーネントの設定 ---
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_path = os.path.join(parent_dir, "frontend")
drag_drop_component = declare_component("drag_drop_component", path=build_path)

# --- ゲームロジック ---
def get_next_state(possible_fake_coins, left_coins, right_coins):
    possible_set = set(possible_fake_coins)
    left_set = set(left_coins)
    right_set = set(right_coins)
    balanced_set = possible_set - (left_set | right_set)

    candidates_left = possible_set & left_set
    candidates_right = possible_set & right_set
    candidates_balanced = balanced_set

    results = [
        ("left", candidates_left),
        ("right", candidates_right),
        ("balanced", candidates_balanced)
    ]
    
    max_size = max(len(c) for _, c in results)
    best_options = [res for res in results if len(res[1]) == max_size]
    choice, next_possible = random.choice(best_options)
    return choice, list(next_possible)

# --- セッション状態の初期化 ---
if 'possible_fake_coins' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.possible_fake_coins = list(range(1, 10))
    st.session_state.trials = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.final_result = None
    st.session_state.last_timestamp = 0

# --- UI ---
st.title("⚖️ 天秤パズル Pro")

if not st.session_state.game_started:
    st.write("1〜9のコインの中に、1枚だけ重い偽物があります。天秤を2回だけ使って特定してください。")
    st.info("下のエリアでコインをドラッグして、天秤に乗せてください。")
    if st.button("ゲーム開始"):
        st.session_state.game_started = True
        st.rerun()

elif not st.session_state.game_over:
    st.subheader(f"第 {st.session_state.trials + 1} 回目の測定")
    
    # コンポーネントを呼び出し、JSからの戻り値を受け取る
    # keyに trials を含めることで、計量ごとにコンポーネントをリセット
    component_result = drag_drop_component(key=f"drag_drop_{st.session_state.trials}")

    # JSから新しいデータが送られてきたかチェック
    if component_result and component_result.get("timestamp", 0) > st.session_state.last_timestamp:
        st.session_state.last_timestamp = component_result["timestamp"]
        left_coins = component_result["left"]
        right_coins = component_result["right"]

        # ロジック実行
        result_val, next_p = get_next_state(st.session_state.possible_fake_coins, left_coins, right_coins)
        st.session_state.possible_fake_coins = next_p
        st.session_state.trials += 1
        
        msg = "左が重い" if result_val == "left" else "右が重い" if result_val == "right" else "水平"
        st.session_state.history.append({
            "t": st.session_state.trials, 
            "l": left_coins, 
            "r": right_coins, 
            "res": msg
        })
        
        if st.session_state.trials >= 2:
            st.session_state.game_over = True
        st.rerun()

    # 履歴表示
    if st.session_state.history:
        st.write("---")
        for h in st.session_state.history:
            st.write(f"第{h['t']}回: 左{h['l']} vs 右{h['r']} → **{h['res']}**")

elif not st.session_state.final_result:
    st.subheader("最終回答タイム")
    st.warning("2回の計量が終わりました。偽物のコインを1つ選んでください。")
    
    for h in st.session_state.history:
        st.write(f"計量{h['t']}: 左{h['l']} vs 右{h['r']} → **{h['res']}**")

    guess = st.selectbox("偽物だと思うコインの番号", options=range(1, 10))
    if st.button("最終回答を確定"):
        # 後出しロジック
        if len(st.session_state.possible_fake_coins) > 1:
            other = [c for c in st.session_state.possible_fake_coins if c != guess]
            fake = random.choice(other)
        else:
            fake = st.session_state.possible_fake_coins[0]
        
        st.session_state.final_result = {"guess": guess, "fake": fake}
        st.rerun()

else:
    res = st.session_state.final_result
    if res["guess"] == res["fake"]:
        st.balloons()
        st.success(f"🎉 正解！偽物は {res['fake']} 番でした！")
    else:
        st.error(f"残念！正解は {res['fake']} 番でした。")
    
    if st.button("最初から遊ぶ"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# スタイル調整
st.markdown("""
<style>
    .stButton button { width: 100%; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)
