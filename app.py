import streamlit as st
import os
from dotenv import load_dotenv
from gemini_service import evaluate_test

# 環境変数の読み込み
load_dotenv()

st.set_page_config(
    page_title="共通テスト 自動採点＆講評システム",
    page_icon="📝",
    layout="wide"
)

st.title("📝 共通テスト 自動採点＆講評システム")
st.markdown("""
PDFファイル（**問題**、**解答解説**、**生徒のマークシート**）をアップロードすると、Gemini APIが自動で丸つけを行い、間違えた問題についての講評を作成します。
""")

# サイドバーにAPI設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key_input = st.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password", help="Gemini APIキーを入力してください（.envからの自動読み込みも対応）")
    
st.header("1. ファイルのアップロード")
col1, col2, col3 = st.columns(3)

with col1:
    question_pdf = st.file_uploader("問題 (PDF)", type=["pdf"])
with col2:
    answer_pdf = st.file_uploader("解答・解説 (PDF)", type=["pdf"])
with col3:
    marksheet_pdf = st.file_uploader("生徒のマークシート (PDF)", type=["pdf"])

if st.button("採点と講評を開始 ✨", type="primary", use_container_width=True):
    if not api_key_input:
        st.error("左のサイドバーから Gemini API Key を入力してください。")
    elif not question_pdf or not answer_pdf or not marksheet_pdf:
        st.warning("すべてのPDFファイル（問題、解答、マークシート）をアップロードしてください。")
    else:
        st.info("処理を開始します。複数のPDFを解析するため、これには数十秒かかる場合があります...")
        
        with st.spinner("Gemini APIで解析中... ⏳"):
            try:
                # PDFファイルのバイナリデータを取得
                q_bytes = question_pdf.getvalue()
                a_bytes = answer_pdf.getvalue()
                m_bytes = marksheet_pdf.getvalue()
                
                # Gemini処理呼び出し
                result = evaluate_test(api_key_input, q_bytes, a_bytes, m_bytes)
                
                st.success("解析が完了しました！ 🎉")
                
                # 結果表示
                st.header("📊 採点結果と講評")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
