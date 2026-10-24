"""「実装」にチャレンジ

models.generate_content() を使い、会話履歴を自分で管理して複数回質問するスクリプト。

使い方:
    uv run python -m app.ask_generate_content
"""

import time

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key


def ask(
    client: genai.Client,
    history: list[types.Content],
    question: str,
) -> str:
    history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    )

    started_at = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL,
        contents=history,
    )
    elapsed = time.perf_counter() - started_at

    if not response.candidates or response.candidates[0].content is None:
        raise RuntimeError("モデルから回答が返りませんでした。")

    answer = response.text
    if answer is None:
        raise RuntimeError("モデルからテキスト形式の回答が返りませんでした。")

    history.append(response.candidates[0].content)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else "不明"
    output_tokens = usage.candidates_token_count if usage else "不明"
    print(
        f"[tokens] 応答時間(sec): {elapsed:.2f}, "
        f"入力: {input_tokens}, 出力: {output_tokens}"
    )

    return answer


def main() -> None:
    client = genai.Client(api_key=get_api_key())
    history: list[types.Content] = []

    while True:
        question = input("質問を入力してください（終了するには exit）> ")
        if question.strip().lower() == "exit":
            break
        if not question.strip():
            continue

        print(f"[model] {MODEL}")
        print(f"[質問] {question}\n")

        try:
            answer = ask(client, history, question)
            print(f"[回答] {answer}\n")
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
