# Tasks Document

- [x] 1. scaffold-main-script
  - File: src/main.py
  - Create Python entrypoint with `run()` function, guard `if __name__ == "__main__"` を追加。
  - 目的: CLI 実行の基盤を整備する。
  - _Leverage: README (作成予定) の実行手順を参照予定_
  - _Requirements: Requirement 1_
  - _Prompt: Implement the task for spec heartbeat-counter, first run spec-workflow-guide to get the workflow guide then implement the task: Role: Python CLI Developer | Task: Create the initial `src/main.py` with `run()` entrypoint, guard節、定数 `MAX_COUNT = 100` の定義を行い、今後のロジック追加に備える | Restrictions: 外部依存を追加しない、PEP 8 に従う | _Leverage: Python 標準ライブラリのみ | _Requirements: Requirement 1 | Success: `python src/main.py` で実行可能なエントリポイントが生成され、まだループは実装していないがスクリプトが終了時に"Heartbeat counter placeholder" を出力する。

- [x] 2. implement-heartbeat-loop
  - File: src/main.py
  - `heartbeat_loop` 関数を実装し、1 秒周期でカウンターと ISO 8601 タイムスタンプを出力。
  - 目的: 基本的なカウンター更新ロジックを提供する。
  - _Leverage: Python `time`, `datetime` モジュール_
  - _Requirements: Requirement 1, Requirement 2_
  - _Prompt: Implement the task for spec heartbeat-counter, first run spec-workflow-guide to get the workflow guide then implement the task: Role: Python Timing Specialist | Task: 実行中ループを実装し、カウンターと ISO 8601 時刻を `[{timestamp}] count={value}` 形式で出力。カウンターは 0〜100 を循環させる。 | Restrictions: 1 秒周期を維持し、`time.sleep` と標準出力のフラッシュを必ず行う | _Leverage: time, datetime | _Requirements: Requirement 1, Requirement 2 | Success: 実行中に各行が 1 秒間隔で表示され、100 の後に 0 に戻る。

- [x] 3. handle-signals-and-errors
  - File: src/main.py
  - `KeyboardInterrupt` 捕捉と終了メッセージ、想定外例外のエラーハンドリングを追加。
  - 目的: ユーザー操作や I/O 異常時でも情報を残して終了させる。
  - _Leverage: Python `sys` モジュール_
  - _Requirements: Requirement 3_
  - _Prompt: Implement the task for spec heartbeat-counter, first run spec-workflow-guide to get the workflow guide then implement the task: Role: Python Reliability Engineer | Task: `KeyboardInterrupt` を捕捉し終了メッセージを標準出力へ表示、その他例外を標準エラーへ書き込み終了コード 1 で終了させる | Restrictions: 余計なログを追加しない、終了前に出力をフラッシュ | _Leverage: sys.stdout, sys.stderr | _Requirements: Requirement 3 | Success: Ctrl+C で「Interrupted by user」が表示され正常終了し、その他例外は標準エラーに内容が表示される。

- [x] 4. document-usage
  - File: README.md
  - スクリプトの実行・停止方法と循環カウンター仕様を記載。
  - 目的: ユーザーが手順と挙動を理解できるようにする。
  - _Leverage: Steering docs product.md, tech.md_
  - _Requirements: Requirement 1, Requirement 2, Requirement 3_
  - _Prompt: Implement the task for spec heartbeat-counter, first run spec-workflow-guide to get the workflow guide then implement the task: Role: Technical Writer | Task: README.md を作成し、実行方法(`python src/main.py`)、出力フォーマット、Ctrl+C での終了方法、依存ライブラリの有無を説明する | Restrictions: 日本語で記述、過度な説明を避ける | _Leverage: product.md, tech.md | _Requirements: Requirement 1, Requirement 2, Requirement 3 | Success: README を参照するだけで利用手順が理解でき、実際の動作と整合する。
