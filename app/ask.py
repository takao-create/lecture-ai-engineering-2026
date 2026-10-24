"""「実装」にチャレンジ

第1回（改）: 素のLLMに会話履歴を保ったまま複数回質問するスクリプト。

使い方:
    uv run python -m app.ask で、質問を入力してEnterを押すと、回答が返ってくる。
    exitと入力してEnterを押すと終了する。

用語集などのツールは使用しないため、講座に固有のことを聞くと、「分からない」と答えるか、
一般論でもっともらしく答える（講座の実際とは違う）ことがある。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

import time # 応答時間計測用

# 第1回の既定の質問。会話モードでは、起動後に質問を入力する。
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:

    started_at = time.perf_counter()            # 問い合わせ前の時間を確保
    response = chat.send_message(question)
    elapsed = time.perf_counter() - started_at  # started_atとの差でresponseが戻るまでの時間を得る

    usage = response.usage_metadata                                     # responseのメタデータ
    input_tokens = usage.prompt_token_count if usage else "不明"         # promptのトークン数 
    output_tokens = usage.candidates_token_count if usage else "不明"    # 回答のトークン数
    thinking_tokens = usage.thoughts_token_count                        # 回答のトークン数

    print(f"[tokens] 入力: {input_tokens}, 出力: {output_tokens}, 思考: {thinking_tokens}")
    print(f'[応答時間(sec)] {elapsed:.2f}')

    return response.text


def main() -> None:

    client = genai.Client(api_key=get_api_key())    # Geminiクライアントを作る
    chat = client.chats.create(model=MODEL,         # チャットセッションを作る
                               config=types.GenerateContentConfig(
                                   thinking_config=types.ThinkingConfig(
                                        thinking_level=types.ThinkingLevel.MINIMAL) #thinking_level="low")でもいいみたい
                                        )
                                )

    while True:
        question = input("質問を入力してください（終了するには exit）> ")
        if question.strip().lower() == "exit":      # 終了判定
            break
        if not question.strip():
            continue

        print(f"[model] {MODEL} ")
        print(f"[質問] {question}\n")

        try:
            answer = ask(chat, question)            # ask関数から回答textを受け取り
            print(f"[回答] {answer}\n")
        except errors.APIError as e:                # ask関数がErrorならこっち
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
