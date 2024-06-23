# 以下を「app.py」に書き込み
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import os
# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

chat = ChatOpenAI(model="gpt-4o")

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
            SystemMessage(
                content="あなたはプラスチック製造の技術職です。"
                        + "初心者から質問されますので、質問内容を整えて専門的な概念に翻訳して回答してください。"
                        + "専門用語は正確に出力してください。専門用語に複数候補がある場合は、全て出力してください。"
                        + "回答内容は例に則って出力してください。"
                        + "例：金型内に成形材料が充填されていなかったようで不完全な形の成形品ができました。なぜでしょうか？"
                        + "例の回答：「ショートショット」と呼ばれる不良が発生した可能性があります。"
                )
        ]

# LLMとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = HumanMessage(
        content=st.session_state["user_input"]
    )

    messages.append(user_message)
    response = chat(messages)
    messages.append(response)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("プラスチック Ｑ＆Ａ")
st.write("gpt-4oを使ったチャットボット　― ＱＡ例の追加による出力(ＱＡ書籍未使用) ―")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "user"
        if message.type == "ai":
            speaker="gpt-4o"

        st.write(speaker + ": " + message.content)
