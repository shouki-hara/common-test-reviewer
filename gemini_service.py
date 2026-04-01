import os
import time
import tempfile
import google.generativeai as genai

def upload_to_gemini(file_bytes, mime_type="application/pdf"):
    """
    一時ファイルを作成し、GeminiのFile APIにアップロードする。
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        # File APIでアップロード
        uploaded_file = genai.upload_file(temp_path, mime_type=mime_type)
        
        # ページ数が多いPDFの場合、Gemini側での事前処理に時間がかかるためACTIVEになるまで待機
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = genai.get_file(uploaded_file.name)
            
        if uploaded_file.state.name == "FAILED":
            raise ValueError(f"Gemini API側でのPDF読み込み処理に失敗しました。")
            
        return uploaded_file
    finally:
        # 一時ファイルの削除
        if os.path.exists(temp_path):
            os.remove(temp_path)

def evaluate_test(api_key: str, question_bytes: bytes, answer_bytes: bytes, marksheet_bytes: bytes) -> str:
    """
    Gemini APIを呼び出し、複数PDFから採点と講評を生成する。
    """
    genai.configure(api_key=api_key)
    
    # モデルの初期化 (推奨: gemini-1.5-pro または gemini-2.0-flash 等)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    question_file = None
    answer_file = None
    marksheet_file = None
    
    try:
        # 1. ファイルのアップロード
        question_file = upload_to_gemini(question_bytes)
        answer_file = upload_to_gemini(answer_bytes)
        marksheet_file = upload_to_gemini(marksheet_bytes)
        # 2. プロンプトの設計
        prompt = """
        あなたは熟練した予備校講師です。提供された3つのPDF（問題、解答解説、生徒のマークシート）を注意深く読み取り、以下の作業を行ってください。

        1. **マークシートの読み取りと採点**:
           生徒のマークシート（画像/PDF）から解答を正確に読み取ってください。
           解答解説の正答と照らし合わせて採点を行い、各設問の正誤状況（正解/不正解）と、おおよその分野別の得点状況を出力してください。

        2. **間違えた問題の分析と講評**:
           生徒が間違えた問題に注目し、「なぜ間違えやすいのか（よくある誤答パターンなど）」や「解答解説に基づいた正しい導き方」を簡潔に説明してください。
           生徒を励まし、今後の学習に向けた的確で前向きなアドバイス（講評）を作成してください。

        出力は可読性の高いMarkdown形式（表やリストを活用し、見出しを適切に構造化）で出力してください。
        """
        
        # 3. リクエストの送信
        response = model.generate_content(
            [question_file, answer_file, marksheet_file, prompt],
            request_options={"timeout": 600} # リクエストタイムアウトを長めに設定
        )
        
        return response.text
        
    finally:
        # 4. アップロードしたファイルのクリーンアップ（サーバー上のファイルを削除）
        if question_file:
            genai.delete_file(question_file.name)
        if answer_file:
            genai.delete_file(answer_file.name)
        if marksheet_file:
            genai.delete_file(marksheet_file.name)
