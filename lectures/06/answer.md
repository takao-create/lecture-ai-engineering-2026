# 第6回 解答

## Memo
ローカル環境で uv run を走らせる場合は、uv run のすぐ後に --env-file .env を付けてやること

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：<br>

**uv run python -m app.agent --list-toolsの結果**<br>
・モデルに見えているツール: 5 個<br>

| ツール名| 役割| 使いどころ| 引数|
|---|---|---|---| 
| [search_materials]| 第1〜3回の本講義資料を検索し、関連ページの本文・タイトル・ページ番号を返す。| queryに調べたい内容を指定する。| 引数: {"query": {"type": "string"}}|
| [search_glossary]| 講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。| AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。| 引数: {"query": {"type": "string"}}|
| [get_lecture_summary]| 指定した回（1始まりの整数）の講義の要点を返す。| 「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。| 引数: {"lecture": {"type": "integer"}}|
| [make_quiz]| 指定した回の用語から一つを選び、確認問題と答えを返す。| 「第2回の確認問題を出して」のように、復習用の問題を求められた際に使う。| 引数: {"lecture": {"type": "integer"}}|
| [save_learning_log]| 学習記録の本文を、JSTの日時付きで learning_log/ に保存する。| 利用者から学習内容や気づきを記録するよう頼まれたときに使う。| 引数: {"saving_log": {"type": "string"}}|

**uv run python -m app.mcp_agent --list-toolsの結果**<br>
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）<br>
・モデルに見えているツール: 1 個<br>

| ツール名| 役割| 使いどころ| 引数|
|---|---|---|---| 
| [glossary_search_glossary]| 講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。| AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。| 引数: {"query": {"title": "Query", "type": "string"}}|

※MCPのサーバーのツール名は、「サーバー名」「_」「ツール名」を順につないだ名になる


- STEP 2 の [tool call]：<br>
・実行したコマンド<br>
uv run python -m app.mcp_agent --trace "AIE2026の講座の宿題にある「3レベル」とは何ですか？"<br>
・traceのログ<br>
[tool call]   glossary_search_glossary({'query': '3レベル'})
<br>
- STEP 3 の [tool call]：<br>
・実行したコマンド<br>
uv run python -m app.mcp_agent --trace "https://modelcontextprotocol.io/ の冒頭を日本語で 3行に要約して"<br>
・traceのログ<br>
[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
<br>
- STEP 4 の [tool call]：<br>
・実行したコマンド<br>
uv run python -m app.mcp_agent --trace "AWSのドキュメントを検索して、 Amazon S3 のバージョニングを 2行で説明して"<br>
・traceのログ<br>
[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})<br>
[tool call]   aws_aws___search_documentation({'search_phrase': 'What is versioning in Amazon S3', 'topics': ['general']})<br>

- 気づき・疑問：
・気づき<br>
講義資料で言及されていた通りではあるが、第3回においては`app.agent`を起動していたところ、今回は`app.mcp_agent`を使い、MCPサーバー経由でも同様にツールを呼び出せることが確認できた。用語検索はどちらでも可能だが、MCP経由ではツール名の前にサーバ名が付いて返ってきていた。<br>
・疑問<br>
そもそもMCPサーバーの起動や接続設定はどのように管理されるのだろうか？


## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
