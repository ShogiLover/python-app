import streamlit as st

# ページの初期設定
st.set_page_config(page_title="意地悪な数当てゲーム", page_icon="🎮")
st.title("🧙‍♂️ 意地悪な数当てゲーム")
st.write("絶対に勝てないかもしれない、ちょっと理不尽な数当てゲームへようこそ。")

# 1. ゲームの状態（セッション状態）の初期化
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "SETUP"  # SETUP, PLAYING, FINAL, GAMEOVER
    st.session_state.min_value = 0
    st.session_state.max_value = 0
    st.session_state.mid_value = 0
    st.session_state.num_of_attempt = 0
    st.session_state.attempt = 1
    st.session_state.history = []  # 過去の判定ログを保存
    st.session_state.result_status = ""  # "WIN" or "LOSE"
    st.session_state.result_text = ""    # 結果のメッセージ
    st.session_state.last_guess = 0      # 最後にユーザーが入力した数値を保存する変数

# 判定結果をポップアップ（モーダルダイアログ）で表示する関数
@st.dialog("🎯 判定結果")
def show_result_popup(message):
    st.write("")
    st.info(message)
    st.write("")
    if st.button("OK", type="primary", use_container_width=True):
        st.rerun()

# ─── ステージ1：設定フェーズ ───
if st.session_state.game_stage == "SETUP":
    st.header("📦 エリアの設定")
    st.write("まずは隠された数字を探す範囲を決めましょう。")
    
    start_num = st.number_input("探すエリアの【始まりの数】", value=1, step=1)
    end_num = st.number_input("探すエリアの【終わりの数】", value=30, step=1)
    
    if st.button("ゲームを開始する", type="primary"):
        if start_num >= end_num:
            st.error("【終わりの数】は、【始まりの数】よりも大きい値にしてください。")
        else:
            st.session_state.min_value = start_num
            st.session_state.max_value = end_num
            st.session_state.mid_value = (start_num + end_num) // 2
            st.session_state.num_of_attempt = (end_num - start_num).bit_length()
            st.session_state.attempt = 1
            st.session_state.history = []
            st.session_state.result_status = ""
            st.session_state.result_text = ""
            st.session_state.last_guess = start_num
            st.session_state.game_stage = "PLAYING"
            st.rerun()

# ─── ステージ2：質問（プレイ）フェーズ ───
elif st.session_state.game_stage == "PLAYING":
    is_search_done = (st.session_state.attempt > st.session_state.num_of_attempt)

    if not is_search_done:
        st.header(f"🕵️‍♂️ 探索中（{st.session_state.attempt} / {st.session_state.num_of_attempt} 回）")
        st.info(f"現在の正解候補の範囲： **{st.session_state.min_value}** から **{st.session_state.max_value}** の間")
        st.caption("※入力した数値に対して、正解がその数「以上」か「未満」か判定します。")

        with st.form("guess_form", clear_on_submit=False):
            user_guess = st.number_input(
                "数値を入力してください：", 
                value=int(st.session_state.min_value), 
                step=1
            )
            submitted = st.form_submit_button("この数で判定！", type="primary")
        
        if submitted:
            st.session_state.last_guess = user_guess

            # 意地悪な条件分岐ロジック
            if user_guess < st.session_state.min_value:
                res_msg = f"正解の数は {user_guess} 以上です。"
            elif user_guess <= st.session_state.mid_value:
                st.session_state.min_value = user_guess
                st.session_state.mid_value = (st.session_state.max_value + st.session_state.min_value) // 2
                res_msg = f"正解の数は {user_guess} 以上です。"
            elif user_guess > st.session_state.max_value:
                res_msg = f"正解の数は {user_guess} 未満です。"
            else:
                st.session_state.max_value = user_guess - 1
                st.session_state.mid_value = (st.session_state.max_value + st.session_state.min_value) // 2
                res_msg = f"正解の数は {user_guess} 未満です。"
            
            log = f"【{st.session_state.attempt}回目: {user_guess}】 判定結果：{res_msg}"
            st.session_state.history.append(log)
            st.session_state.attempt += 1
            
            show_result_popup(res_msg)
            
    else:
        st.header("🏁 探索完了")
        st.success("すべての探索チャンスを使い果たしました。")
        
        if st.button("最終回答へ進む ➡️", type="primary"):
            st.session_state.game_stage = "FINAL"
            st.rerun()

    if st.session_state.history:
        st.write("---")
        st.subheader("📋 これまでの判定履歴")
        for h in reversed(st.session_state.history):
            st.write(h)

# ─── ステージ3：最終回答フェーズ ───
elif st.session_state.game_stage == "FINAL":
    st.header("🚨 最終回答フェーズ")
    st.warning("これが最後のチャンスです。ズバリ正解を言い当ててください。")
    
    with st.form("final_form", clear_on_submit=False):
        final_guess = st.number_input("最後の予想：", value=int(st.session_state.last_guess), step=1)
        final_submitted = st.form_submit_button("これが本当の正解だ！", type="primary")
    
    if final_submitted:
        # 後出しギミックの判定
        if st.session_state.min_value == st.session_state.max_value:
            if final_guess == st.session_state.min_value:
                st.session_state.result_status = "WIN"
                st.session_state.result_text = f"🎉 おめでとうございます！見事に正解の {final_guess} を当てました！"
            else:
                st.session_state.result_status = "LOSE"
                st.session_state.result_text = f"💀 残念、ハズレです！あなたの予想：{final_guess} ｜ 正解：{st.session_state.min_value} でした。"
        else:
            if final_guess == st.session_state.min_value:
                actual_answer = st.session_state.max_value
            else:
                actual_answer = st.session_state.min_value
            st.session_state.result_status = "LOSE"
            st.session_state.result_text = f"💀 残念、ハズレです！あなたの予想：{final_guess} ｜ 正解：{actual_answer} でした。"
            
        st.session_state.game_stage = "GAMEOVER"
        st.rerun()

    if st.session_state.history:
        st.write("---")
        st.subheader("📋 これまでの判定履歴")
        for h in reversed(st.session_state.history):
            st.write(h)

# ─── ステージ4：ゲームオーバー（結果表示とリトライ） ───
elif st.session_state.game_stage == "GAMEOVER":
    st.header("📊 ゲーム結果")
    
    if st.session_state.result_status == "WIN":
        st.balloons()
        st.success(st.session_state.result_text)
    else:
        st.error(st.session_state.result_text)
        
    st.write("---")
    if st.button("もう一度最初から遊ぶ", type="primary"):
        st.session_state.game_stage = "SETUP"
        st.rerun()

    # 💡 【追加】ゲームオーバー画面の最下部にもこれまでの判定履歴を常時表示させる
    if st.session_state.history:
        st.write("---")
        st.subheader("📋 これまでの判定履歴")
        for h in reversed(st.session_state.history):
            st.write(h)
