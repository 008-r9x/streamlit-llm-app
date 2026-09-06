import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .envファイルの環境変数を読み込む
load_dotenv()

# プロンプト定義
scientist_prompt = """
あなたは科学的根拠を重視する科学者です。

以下の方針で回答してください。
- 怪奇現象や不思議な体験について、まず自然現象・物理現象・生物学・心理学などの観点から考察してください。
- 可能性が複数ある場合は、考えられる原因をいくつか挙げてください。
- 科学的に確認されていない内容を事実として断定しないでください。
- 情報が不足している場合は、「現時点では断定できない」と明示してください。
- 専門用語を使う場合は、一般の人にも分かるよう簡潔に説明してください。
- 霊的・超常的な説については、科学的に検証されているかどうかを区別してください。

冷静で論理的ですが、ユーザーの体験そのものを頭ごなしに否定しない姿勢で回答してください。
"""

psychic_prompt = """
あなたは怪談・心霊現象・超常現象に詳しい霊能者です。

以下の方針で回答してください。
- 不思議な現象を、霊・念・土地の記憶・気配などの霊的な観点から解釈してください。
- 日本の怪談や心霊文化で語られる考え方も交えながら回答してください。
- 現象から考えられる霊的な可能性を複数提示しても構いません。
- 恐怖を過度に煽らず、落ち着いた語り口で回答してください。
- 霊的な解釈は科学的に証明された事実ではないことが分かる表現にしてください。
- 危険な行動や高額な除霊・祈祷などを勧めないでください。

少し神秘的で怪談らしい雰囲気を持たせながら、ユーザーの体験に寄り添って回答してください。
"""

# 専門家設定
expert_prompts = {'科学者':scientist_prompt, '霊能者': psychic_prompt}

# 呼び出しモデルの指定
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# LangChainコードの関数化
def get_llm_response(input_text, expert_type):

    # ラジオボタン選択肢判定
    # if expert_type == "科学者":
    #     system_message = scientist_prompt
    # elif expert_type == "霊能者":
    #     system_message = psychic_prompt

    # ラジオボタン選択肢によるプロンプト設定
    system_message = expert_prompts[expert_type]
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    print("-----")
    print(messages)

    # LLMにメッセージを送信し、応答取得
    response = llm.invoke(messages)
    return response.content

# アプリの概要と操作方法を表示
st.title("科学か怪異か")
st.write("不思議な現象や怪奇現象について、2つの異なる視点から回答するAIアプリです。")
st.write("専門家を選択して、気になる現象を入力してください。")
# 質問例
# 夜の墓地で青白い火の玉を見ました
# 深夜になると、『パキッ』『ミシッ』という音が聞こえます。誰もいないはずなのに、、
# いつもの道を歩いていたら、見たことのない路地がありました。入ってみると誰もおらず、引き返したらその路地自体が消えていました。私はどこに行っていたのでしょうか？

# radio()：ラジオボタン表示
# 第一引数：ラジオボタンのラベル
# 第二引数：リスト形式の各要素がラジオボタンの選択肢
expert_type = st.radio(
    "専門家を選択してください。",
    ["科学者", "霊能者"]
)

# 区切り線
# st.divider()


# input_text = st.text_input(label="不思議な現象を入力してください")

# if st.button("回答"):
#     st.divider()

#     if input_text:
#         response = get_llm_response(input_text, expert_type)
#         print("-----")
#         print(response)

#         st.write(f"専門家の回答：**{response}**")

#     else:
#         st.warning("不思議な現象を入力してください")


# 入力欄を空にする
def clear_input():
    # input_textはkeyの設定値
    st.session_state.input_text = ""

input_text = st.text_input(
    "不思議な現象を入力してください",
    key="input_text"
)

# ボタン位置調整：画面を三分割
# col1, col2 = st.columns(2)
col1, col2, _ = st.columns([1, 2, 6])

# 回答ボタンを配置
with col1:
    answer_button = st.button("回答")

# ボタン押下で関数実行
with col2:
    st.button("入力内容クリア", on_click=clear_input)

if answer_button:
    if input_text:
        with st.spinner("回答中..."):
            try:
                response = get_llm_response(input_text, expert_type)
                print("-----")
                print(response)
                st.write(f"専門家の回答：**{response}**")
            except Exception as e:
                st.error(f'エラーが発生しました。：{e}')
    else:
        st.warning("不思議な現象を入力してください")



