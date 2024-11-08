# gemini_chat.py

import os
import google.generativeai as genai

# APIキー設定
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# モデル設定
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def generate_reply(user_message):
    """
    Google Gemini APIを使って応答を生成する関数。
    user_message: ユーザーからの入力メッセージ
    return: 応答テキスト
    """
    # モデルインスタンス作成
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    # チャットセッションの開始
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)
    return response.text
