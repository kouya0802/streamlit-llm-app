import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 環境変数の読み込み
load_dotenv()

def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    
    # 専門家タイプに応じたシステムメッセージを設定
    system_messages = {
        "医療専門家": "あなたは経験豊富な医療専門家です。医学的な知識を基に、正確で分かりやすい回答を提供してください。ただし、診断や医療アドバイスではなく、一般的な情報提供に留めてください。",
        "プログラミング専門家": "あなたは熟練したソフトウェアエンジニアです。プログラミングに関する質問に対して、実践的で効率的な解決策を提供してください。コード例も含めて説明してください。",
        "料理専門家": "あなたは経験豊富な料理専門家・シェフです。料理に関する質問に対して、実用的なレシピや調理のコツ、食材の選び方などを詳しく説明してください。",
        "ビジネス専門家": "あなたは経営戦略とビジネス分析の専門家です。ビジネスに関する質問に対して、実践的で戦略的な視点から回答してください。",
        "教育専門家": "あなたは教育学の専門家です。学習方法や教育に関する質問に対して、効果的な学習戦略や教育理論に基づいた回答を提供してください。"
    }
    
    try:
        # ChatOpenAIのインスタンスを作成
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # メッセージを作成
        messages = [
            SystemMessage(content=system_messages.get(expert_type, "あなたは親切なアシスタントです。")),
            HumanMessage(content=input_text)
        ]
        
        # LLMから回答を取得
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlitアプリケーションのメイン部分
def main():
    st.set_page_config(
        page_title="AI専門家システム",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI専門家システム")
    
    st.markdown("""
    ## 📋 アプリケーション概要
    このアプリケーションは、様々な分野の専門家として振る舞うAIチャットボットです。
    下記の専門家から選択し、質問を入力すると、その分野の専門知識に基づいた回答を得ることができます。
    
    ## 🔧 操作方法
    1. **専門家を選択**: ラジオボタンから相談したい専門家の分野を選択してください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **回答を取得**: 「回答を取得」ボタンをクリックして、AI専門家からの回答を表示します
    
    ## ⚠️ 注意事項
    - 医療に関する回答は一般的な情報提供のみで、診断や治療の代替ではありません
    - 重要な判断については、必ず専門機関にご相談ください
    """)
    
    st.divider()
    
    # 専門家選択のラジオボタン
    expert_options = [
        "医療専門家",
        "プログラミング専門家", 
        "料理専門家",
        "ビジネス専門家",
        "教育専門家"
    ]
    
    selected_expert = st.radio(
        "🎯 相談したい専門家を選択してください：",
        expert_options,
        index=0,
        horizontal=True
    )
    
    # 入力フォーム
    st.subheader(f"💬 {selected_expert}への質問")
    user_input = st.text_area(
        "質問や相談内容を入力してください：",
        height=150,
        placeholder="こちらに質問を入力してください..."
    )
    
    # 回答取得ボタン
    if st.button("🚀 回答を取得", type="primary"):
        if user_input.strip():
            with st.spinner(f"{selected_expert}が回答を準備中..."):
                response = get_llm_response(user_input, selected_expert)
                
                st.subheader(f"📝 {selected_expert}からの回答")
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
                {response}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("質問を入力してください。")
    
    # サイドバーに追加情報
    with st.sidebar:
        st.header("📊 使用可能な専門家")
        for expert in expert_options:
            st.write(f"• {expert}")
        
        st.divider()
        st.subheader("🔧 設定")
        st.info("OpenAI APIキーは環境変数(.env)から読み込まれます")

if __name__ == "__main__":
    main()