# 第6回 解答

## Memo
・ローカル環境で uv run を走らせる場合は、uv run のすぐ後に --env-file .env を付けてやること
・git status -sbで、追跡しているかどうかわかる　つまり、ここで ## lecXX...origin/lecXX って戻るなら、git pushだけでよい　そうじゃないなら、git push -u origin lecXX としないとダメ

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

- 気づき・疑問：<br>
    ・気づき<br>
    講義資料で言及されていた通りではあるが、第3回においては`app.agent`を起動していたところ、今回は`app.mcp_agent`を使い、MCPサーバー経由でも同様にツールを呼び出せることが確認できた。用語検索はどちらでも可能だが、MCP経由ではツール名の前にサーバ名が付いて返ってきていた。<br>
    ・疑問<br>
    そもそもMCPサーバーの起動や接続設定はどのように管理されるのだろうか？


## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：<br>
    基礎・実装<br>
- やったこと：<br>
    - 基礎の内容(以下の手順はproblem.mdにおける`基礎`の進め方に基づく)<br>
    01. `app/mcp_server.py`にget_lecture_summaryを追加
    02. `git status` で、変更されたファイルが `app/mcp_server.py` だけであることを確認
    03. エージェント側を変えずに、一覧に `glossary_get_lecture_summary` が増えたことを確認
    04. uv run python -m app.mcp_agent --trace "第2回では何を学びますか？"を実行し、書き足したツールが呼ばれることを確認
    05. `uv run pytest -q` を実行し、テストがすべて通ることを確認
    <br>
    - 実装の内容<br>
    01. `app/mcp_server.py`にtools.make_quizをmcpツールとして追加
    02. uv run python -m app.mcp_agent --list-tools を実行し、[glossary_make_quiz]が含まれることを確認
    03. uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　を実行（1回目
    04. `app/mcp_agent.py`のINSTRUCTIONSに「- クイズや確認問題を求められたら、回の存在を推測せず、必ず glossary_make_quiz を指定された回で使う。 」を追加
    05. uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　を実行（2回目
    06. 存在する回のテストとして、uv run python -m app.mcp_agent --trace "第6回のクイズを作って"　を実行
    <br>
- 結果：<br>
    ・基礎の内容<br>

    get_lecture_summary をMCPツールとして登録し、エージェント側を変更せずにツールを追加して実行したところ、講義要約の質問でツールが呼び出されることを確認できた。尚、この時点では app/mcp_agent.pyの INSTRUCTIONS は確認していなかった。<br>
    
    - uv run python -m app.mcp_agent --trace "第2回では何を学びますか？" の結果
    
    | traceログ| 呼ばれたtool|
    |---|---|
    | [tool call]| glossary_get_lecture_summary({'lecture': 2})|
    | [tool return]| glossary_get_lecture_summary -> # 第2回 ファインチューニングとLoRA|
    
    <br>
    ・実装の内容<br>
    第99回のクイズ作成において、1回目の実行では make_quiz は、呼び出されることがなかった。mcp_agent.pyにおけるINSTRUCTIONSに一文を追加した後は make_quiz が呼ばれ、該当回がないという結果になった。　その後の第6回クイズ作成テストでは make_quiz が呼び出され、問題なく生成された。

    - uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　の結果（1回目

    | traceログ| 呼ばれたtool|
    |---|---|
    | -| -|

    - uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　の結果（2回目

    | traceログ| 呼ばれたtool|
    |---|---|
    | [tool call]| glossary_make_quiz({'lecture': 99})|
    | [tool return]| glossary_make_quiz -> 第99回の用語が見つかりません。…|

    - uv run python -m app.mcp_agent --trace "第6回のクイズを作って"　の結果

    | traceログ| 呼ばれたtool|
    |---|---|
    | [tool call]| glossary_make_quiz({'lecture': 6}|
    | [tool return]| glossary_make_quiz -> {"question": "「fetchサーバー」の意味は？", "answer": "指定したURLのページを取得し、本文をMarkdownにして返す既製のMCPサーバー（Python製、uvx mcp-server-fetch で起動）…|


- 気づき・疑問：<br>
    ・気づき<br>
    基礎におけるget_lecture_summaryでは、app/mcp_agent.pyを何も触ることなくuv run python -m app.mcp_agent --trace "第2回では何を学びますか？"を実行したところ、glossary_get_lecture_summaryが呼ばれていた。一方、実装における1回目の試行ではmake_quizが呼ばれることはなかった。この差の理由を調査するため、app/mcp_agent.pyを確認したところ、INSTRUCTIONSに「- 回の内容を聞かれたら get_lecture_summary を使う。」の一文があることを確認した。<br>
    これに倣って、実装の内容:04の通り、 `app/mcp_agent.py`を変更したところ、 make_quiz が呼ばれるようになることが確認できた。<br>
    ・疑問<br>
    今回、1回目の試行でmake_quizが呼ばれなかったため、初手として`app/mcp_agent.py`のINSTRUCTIONSにクイズを求められた際の振る舞いに関する一文を追加し、結果として目論見通り挙動の変化を確認した。とはいえ、1回目は第99回というそもそも存在しない回のクイズ生成を求めており、LLMがmake_quizを使うまでもないと判断した可能性もある。製品として考えた場合に、挙動が安定しないことは好まれることではないが、実際に存在する回やありそうな回（第14回など）を対象として指定した場合、あるいは第99回を対象に試行を繰り返した時に、LLMがmake_quizを使うという選択をすることもあるのではないだろうか。つまり、指示文なしでも呼ばれることや、指示文があっても呼ばれないことは、どちらも可能性として考えられる。したがって、指示文によって呼び出しを促せても、LLMの挙動を常に保証するものではないと考えるべきではないだろうか？


### 以下、実行の記録

- 基礎 uv run python -m app.mcp_agent --trace "第2回では何を学びますか？"　の結果

[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第2回では、**「ファインチューニングとLoRA」**をテーマに、以下の内容を学びます。

* **事前学習とファインチューニングの違い・適性**：モデルが向く場面・向かない場面の理解
* **SFT（教師ありファインチューニング）**：入力と出力のペアによる学習とデータの重要性
* **PEFTとLoRAの考え方**：全パラメータを更新せず、低ランク行列の追加でメモリやコストを抑えて学習する仕組み（およびQLoRAとの違い）
* **過学習への注意**：学習の進め方や評価のポイント

Google Colab上で小さなモデルを用いたLoRA学習の演習も行います。

関連する回：第2回

--- trace ---
[tool call]   glossary_get_lecture_summary({'lecture': 2})
[tool return] glossary_get_lecture_summary -> # 第2回 ファインチューニングとLoRA

## この回のねらい

- 事前学習とファインチューニングの違い、ファインチューニングが向く場面と向かない場面を理解する
- LoRAの考え方を理解し、Google Colab上で小さなモデルを…
[usage] 入力 5,942 tokens / 出力 184 tokens / モデル応答 2 回
<br>
<br>

- 実装　uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　の結果（1回目

[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第99回のクイズが作成できませんでした。講座の用語集やカリキュラムに第99回は存在しないようです。（現在の講座にはそのような回は登録されていません）

他の回（例えば第1回〜最終回など）の確認問題をご希望の場合は、何回目またはどの用語について知りたいか教えていただければ、喜んでクイズを作成いたします！

--- trace ---
[usage] 入力 2,780 tokens / 出力 80 tokens / モデル応答 1 回
<br>
<br>

-  実装　uv run python -m app.mcp_agent --trace "第99回のクイズを作って"　の結果（2回目

[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第99回の用語や講義内容が用語集に見つかりませんでした。この講座（AIE2026）には存在しない回か、まだ登録されていない回である可能性があります。

--- trace ---
[tool call]   glossary_make_quiz({'lecture': 99})
[tool return] glossary_make_quiz -> 第99回の用語が見つかりません。…
[usage] 入力 5,670 tokens / 出力 58 tokens / モデル応答 2 回
<br>
<br>

-  実装　uv run python -m app.mcp_agent --trace "第6回のクイズを作って"　の結果

[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第6回の確認問題ですね。それでは、こちらのクイズに挑戦してみてください！

**【確認問題（第6回）】**
「fetchサーバー」の意味は何でしょうか？

---
💡 **ヒント：**
LLMが自らインターネット上の情報にアクセスできるようにするための、Python製の既製のMCP（Model Context Protocol）サーバーの一つです。設定を行うだけで、AIが指定したURLのページを取得し、本文をMarkdown形式で取得できるようになります。

（関係する回：第6回）

--- trace ---
[tool call]   glossary_make_quiz({'lecture': 6})
[tool return] glossary_make_quiz -> {"question": "「fetchサーバー」の意味は？", "answer": "指定したURLのページを取得し、本文をMarkdownにして返す既製のMCPサーバー（Python製、uvx mcp-server-fetch で起動）…
[usage] 入力 5,747 tokens / 出力 124 tokens / モデル応答 2 回
