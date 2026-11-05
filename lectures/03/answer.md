# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：<br>
・第1回の回答（モデルの回答を要約）<br>
    AIE2026の宿題における「3レベル」は、受講生のスキルや理解度、あるいは宿題の難易度に合わせて用意された3段階の課題（レベル1、レベル2、レベル3）を指す　それぞれレベル1：基礎的な要件達成、レベル2：学習内容の応用、レベル3：自発的な工夫による発展的な成果<br>
<br>
・今回:第3回の回答（モデルの回答原文まま）<br>
    AIE2026の講座における「3レベル」とは、宿題の構成・難易度の段階を指しています。具体的には以下の3つのレベルに分かれています。<br>

    1. **基礎**：講義内容の確認（知識の定着を図る問題など）
    2. **実装**：自分でコードを書く（実際に手を動かす課題）
    3. **発展**：調査や試行（より踏み込んだ応用的な課題）

    原則として、これら3つのうち**どれか1つに取り組めばその回の宿題は完了**となります（採点は行われません）。ご自身の現在の理解度や目的に合わせて選んでみてくださいね。

    第1回

・両者の比較<br>
    第1回の時点の回答では「3レベル」について、glossary.json の記述と相違する「レベル1・2・3」の課題難易度として説明していた<br>
    一方、今回の回答では「基礎・実装・発展」と説明しており、 glossary.json の記述と一致する内容となった<br>
    また、「どれか1つに取り組めば宿題は完了」「原則として採点は行わない」という説明もglossary.jsonの内容に沿ったものとなっている<br>
    さらに回答末尾に示された関係する回について、glossary.json記載の"lecture": 1と合致していることも確認できた<br>
    説明の後に付与されている「ご自身の現在の理解度や目的に合わせて選んでみてくださいね」は回答生成にあたってモデルが補った助言であるようだ<br>
    <br>
- `--trace` で見えたツール呼び出し（ツール名と引数）：<br>
    以下、「uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"」を実行した結果<br>
    [tool call]   search_glossary({'query': 'LoRA'})<br>
    [tool call]   search_glossary({'query': 'QLoRA'})<br>
    <br>
- 1つの質問での LLM 呼び出し回数（`requests`）：<br>
    requests=2<br>
    1回目の生成：プロンプトに固有の用語が含まれるため、INSTRUCTIONSに基づき、用語をそれぞれ search_glossary の引数として実行指示を生成<br>
    2回目の生成：ツールの結果を含む会話履歴を受け、ユーザー向けの回答を生成<br>
    というような流れであると考えられる<br>
    <br>
- 追加したツールと、docstring に書いた説明：<br>
    agent.pyへ追加：agent.tool_plain(tools.make_quiz)<br>
    tools.pyへ追加：make_quiz関数を追加<br>
    make_quiz関数のdocstring:<br>
    """指定した回の用語から一つを選び、
    確認問題と答えを返す。

    「第2回の確認問題を出して」のように、
    復習用の問題を求められた際に使う。
    """
    <br>

## 宿題

- 取り組んだレベル：実装
<br>
- やったこと：<br>
    Copilotにアドバイスを貰いながら、learning_log/フォルダへ学習記録を保存するツール（save_learning_log）を実装した<br>
    ・各ファイルの変更内容<br>
        tools.py:   日付取得用のdatetimeライブラリのインポート及び、save_learning_log関数の追加<br>
        agent.py:   講義資料に倣い、DeferredToolRequestsを導入、さらにユーザーの判断結果を取得するためDeferredToolResultsも導入した<br>
                    また、LLMの出力結果をisinstance(result.output, DeferredToolRequests)にて判定し、ユーザーに確認を求める形とした<br>
<br>
- 結果：<br>
    uv run python -m app.agent "今日の学習記録として、〇〇を学んだことを保存して"　のような形で呼び出すと、リポジトリ直下のlearning_logフォルダにYYYY-MM-DD.mdファイルを作り（すでに同日のファイルが存在する場合は追加で記入される）、保存できることを確認した<br>

- 気づき・疑問：<br>
    ・AIエージェントのツールユースにおけるCLI、LLM、Pydantic AIの協調動作について確認できた<br>
        ・現時点で理解できている動作の流れを以下に整理しておく<br>
        01.CLI          :   ユーザーの指示を受け取る<br>
        02.Pydantic AI  :   指示とエージェントの設定をLLMへ<br>
        03.LLM          :   ツール呼び出しの要求を返す<br>
        04.Pydantic AI  :   設定（requires_approval=True）に基づいて承認待ちとして、DeferredToolRequests を返す<br>
        05.CLI          :   ツール名や引数を表示して、ユーザーに承認を尋ねる<br>
        06.Pydantic AI  :   承認結果を受け取り、承認されていればPython関数を実行する<br>
        07.Python       :   関数を実行して戻り値を返す<br>
        08.Pydantic AI  :   戻り値を受け取ってLLMに渡す<br>
        09.LLM          :   最終回答を作る<br>
        10.CLI          :   最終回答を表示する<br>     
<br>
    ・気づき・疑問
        ・何度かsaving_logを使ってデータを保存させてみたが、以下の通り保存スタイルに揺れが生じた<br>
        name     | input prompt | saved contents<br>                                
        sample01 | 今日の学習記録として、Pydantic AIの承認付きツールについて学んだことを保存して | Pydantic AIの承認付きツールについて学んだ<br>
        sample02 | 今日の学習記録として、エージェントとツールの関係について学んだことを保存して | 本日の学習内容: エージェントとツールの関係について学びました。AIエージェントはLLM（モデル）を中核に、自律的なループを回しながら、検索や計算などのツールを呼び出してタスクを遂行することを理解しました。<br>
        sample03 | 今日の学習記録として、AIエージェントのツールユースにおけるCLI,LLM,Pydantic AIの協調動作の流れを確認・整理したことを保存して | AIエージェントのツールユースにおけるCLI, LLM, Pydantic AIの協調動作の流れを確認・整理した。<br>
        sample04 | 今日の学習記録として、AIエージェントのツールユースにおいて回答のスタイルや形式に揺れが生じることを確認したことを保存して | AIエージェントのツールユースにおいて回答のスタイルや形式に揺れが生じることを確認した<br>
<br>
        ・まとめと考察
        今回の試行においては、プロンプトの依頼内容をほぼそのまま保存する場合もあれば、sample02のように{title:contents}の形式＋プロンプトに記述されていない内容を補った上で保存するケースも確認された<br>
        また、save_learning_logから返される「学習記録を{ファイル名} に保存しました」の後に、「〜について学習されたとのこと、素晴らしいですね！この調子で学習を進めていきましょう。」のような形で一文添える、他にも「（関係する回：第7回）」のような出力が見られることもあった<br>
        とはいえ、後者についてglossary.jsonを調べたところ、同jsonファイルには第7回の内容は含まれていない　この回答は最終回答の生成で補われたと考えられるが、どのような根拠に基づいて生成されたのかは疑問である<br>
        <br>
        つまり、saving_logとしてsave_learning_logに渡されるテキストと、最終的に回答としてCLIに表示されるテキストのように、リクエスト数は処理によって複数回になりうるはずと考えた<br>
        確認として、--traceを付与して同様に保存し、traceを確認したところ、以下のようなログが得られた<br>
        <br>
        ```
        --- trace ---
        [tool call]   search_glossary({'query': 'ツールユース'})
        [tool call]   search_glossary({'query': 'LLM'})
        [tool return] search_glossary -> [{"term": "ツール（Tool use / Function calling）", "lecture": 3, "definition": "モデルが呼び出せるように用意した関数。モデルはツールの名前・説明・引数の型を見て、必要なと…
        [tool return] search_glossary -> [{"term": "LLM（大規模言語モデル）", "lecture": 1, "definition": "大量のテキストで学習し、入力に続くトークンを予測することで文章を生成するモデル。質問応答、要約、コード生成など多くのタスクを、指…
        [tool call]   save_learning_log({'saving_log': 'AIエージェントのツールユースにおいて回答のスタイルや形式に揺れが生じる原因及びLLMがテキストを生成するタイミングについて考察した。'})
        [tool return] save_learning_log -> 学習記録を 2026-11-05.md に保存しました…
        [usage] RunUsage(cost=Decimal('0.0005236'), details={'text_prompt_tokens': 1062}, input_text_tokens=1062, input_tokens=1062, output_tokens=82, requests=1, tool_calls=1)
        ```
        <br>
        <br>
        どう見ても複数回requestやtool callをしているはずだが、requests=1, tool_calls=1となっており、traceのログと一致しない<br>
        このため、usageのログは全体の呼び出し回数を表す値ではないと考えて、改めてコードを確認したところ、承認前後に run_sync が複数回実行され、result.usage が最後の実行分だけを示すようになっていた<br>
        そこで、各実行のusageを合算して usage total として表示するよう実装を追加した<br>
        複数のツールを使う依頼で再度試したところ、requests=3, tool_calls=3 となり、モデル応答の回数であるrequest, 成功したツール呼び出しの回数であるtool call共に、最初の検索を含めた合計を確認できるようになった<br>
        このような実装にしておけば、[usage] は最後の実行分、[usage total] は各実行分を合算した値として区別可能である