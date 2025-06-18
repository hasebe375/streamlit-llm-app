import os
from dotenv import load_dotenv

# .env から OPENAI_API_KEY を読み込む
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY が見つかりません。\n"
        ".env を作成して\nOPENAI_API_KEY=あなたのキー\nを記入してください。"
    )

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# =============================
# Streamlit アプリ
# =============================
st.title("サンプルアプリ: 子育て相談アプリ")

st.write("##### 動作モード1: 教育に関する相談")
st.write("入力フォームに教育に関する質問を入力することで、専門家に相談したような回答を得ることができます。")
st.write("##### 動作モード2: 子供の健康に関する相談")
st.write("入力フォームに子供の健康に関する質問を入力することで、専門家に相談したような回答を得ることができます。")

mode = st.radio(
    "動作モードを選択してください。",
    ["教育に関する相談", "子供の健康に関する相談"],
)

st.divider()

label = "教育に関する質問を入力してください。" if mode == "教育に関する相談" \
        else "子供の健康に関する質問を入力してください。"
question = st.text_input(label=label)

if st.button("実行"):
    if not question:
        st.error("質問を入力してから『実行』を押してください。")
        st.stop()

    # LLM へのメッセージ作成
    system_prompt = "あなたは教育の専門家です。" if mode == "教育に関する相談" \
                    else "あなたは子供の健康の専門家です。"
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    # 生成
    with st.spinner("考え中…"):
        response = llm.invoke(messages).content

    st.success("回答が生成されました！")
    st.markdown(response)