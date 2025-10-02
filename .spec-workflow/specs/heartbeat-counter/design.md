# Design Document

## Overview
1 秒ごとに循環カウンターと現在時刻を出力する CLI ユーティリティを `src/main.py` の単一モジュールとして実装する。`time.sleep` を用いたループ制御と `datetime.datetime.now` による時刻取得を組み合わせ、標準出力へ整形済みテキストを流す。SIGINT を捕捉して優雅に終了できるようにする。

## Steering Document Alignment

### Technical Standards (tech.md)
- Python 3.11 以上、標準ライブラリのみを利用する方針に従う。
- 循環カウンター方式と単一ファイル構成を採用し、CPU 負荷を抑えたシーケンシャルループを実装する。
- 例外処理とフラッシュ制御でリアルタイム性を担保し、tech.md で定義した運用要件を満たす。

### Project Structure (structure.md)
- 実装は `src/main.py` に配置し、モジュール構成・命名規則 (snake_case) を遵守する。
- `MAX_COUNT` 定数やフォーマット関数を切り出し、構造ガイドラインのインポート順序・関数構成に合わせる。
- 将来の拡張を見据え、ユーティリティ分割が容易な形で関数を配置する。

## Code Reuse Analysis
既存コードはまだ存在しないため新規実装となる。ただし Python 標準ライブラリの `time`, `datetime`, `sys` を活用して要件を満たす。

### Existing Components to Leverage
- **datetime モジュール**: 現在時刻取得と ISO 8601 形式への整形。
- **time モジュール**: 1 秒間隔の待機 (`time.sleep`).
- **sys.stdout/sys.stderr**: 出力フラッシュおよびエラーメッセージ表示。

### Integration Points
- 外部システムやデータストアとの連携はない。

## Architecture

- 単一モジュールで完結するシーケンシャルなループ構造。
- 関数分割: 初期化 (`run()`)、次のカウント値計算 (`next_count`)、出力フォーマット (`format_line`)、メインループ (`heartbeat_loop`)。
- SIGINT をハンドリングするため `KeyboardInterrupt` を捕捉する try/except ブロックを用いる。

### Modular Design Principles
- **Single File Responsibility**: `main.py` はカウンター制御と表示に限定。
- **Component Isolation**: カウンター更新ロジックと出力フォーマットを関数化しテストしやすくする。
- **Service Layer Separation**: 規模が小さいため層分けは最小限だが、将来 `timer.py` 等へスケールできるよう関数 API を明確にする。
- **Utility Modularity**: 補助関数をトップレベルに定義し、他ファイルから再利用可能な形にする。

```mermaid
graph TD
    A[run()] --> B[heartbeat_loop()]
    B --> C[next_count()]
    B --> D[format_line()]
    B -->|uses| E[time.sleep]
    D --> F[datetime.now]
```

## Components and Interfaces

### Component 1: `run()` エントリポイント
- **Purpose:** 初期状態を設定し、ハートビートループを開始する。
- **Interfaces:** `run(max_count: int = 100) -> None`
- **Dependencies:** `heartbeat_loop`
- **Reuses:** `MAX_COUNT` 定数。

### Component 2: `heartbeat_loop()`
- **Purpose:** 無限ループでカウンターと時刻を取得し出力する。
- **Interfaces:** `heartbeat_loop(max_count: int) -> None`
- **Dependencies:** `next_count`, `format_line`, `time.sleep`, `sys.stdout.flush`
- **Reuses:** `KeyboardInterrupt` ハンドリングロジック。

### Component 3: `next_count()`
- **Purpose:** 現在値と上限値から次のカウントを算出する。
- **Interfaces:** `next_count(current: int, max_count: int) -> int`
- **Dependencies:** なし
- **Reuses:** 後続でテスト可能な純粋関数として利用。

### Component 4: `format_line()`
- **Purpose:** 時刻とカウンターを表示用文字列に変換する。
- **Interfaces:** `format_line(timestamp: datetime, count: int) -> str`
- **Dependencies:** `datetime`
- **Reuses:** フォーマットロジックを一箇所に集約し、将来の出力変更に備える。

## Data Models
データベースや複雑なモデルは不要。以下の単純な構造のみ扱う。

### カウンター状態
```
CounterState:
- count: int   # 現在のカウンター値 (0〜100)
```

### 出力レコード（概念モデル）
```
OutputLine:
- timestamp: datetime
- count: int
- text: str  # format_line で生成される出力
```

## Error Handling

### Error Scenario 1: SIGINT による中断
- **Handling:** `KeyboardInterrupt` を捕捉し、終了メッセージを `print("Interrupted")` 等で出力後、`return`。
- **User Impact:** ユーザーは Ctrl+C 後に「Interrupted」メッセージを確認し、安全に終了できる。

### Error Scenario 2: 出力時の例外 (I/O エラー)
- **Handling:** `IOError` や `OSError` を捕捉し、内容を標準エラーへ書き出した上で非ゼロ終了コードで終了。
- **User Impact:** ユーザーはエラー内容を把握し、リダイレクト先の問題などを調査できる。

### Error Scenario 3: 時刻取得の例外
- **Handling:** `datetime.now()` は通常例外を投げないが、念のため予期せぬ例外を最上位で捕捉しログを出力して終了。
- **User Impact:** 想定外の障害が発生した際も原因を把握しやすい。

## Testing Strategy

### Unit Testing
- `next_count` の挙動をテストし、0→1、99→100、100→0 などのケースを検証する。
- `format_line` のフォーマットが ISO 8601 形式であることを確認するスモールテストを用意できる。

### Integration Testing
- `pytest` から `capsys` を用いて `heartbeat_loop` を短時間実行し、出力のタイミングとフラッシュが行われるかを確認する。
- SIGINT を疑似的に発生させ、終了メッセージが表示されるかを検証する。

### End-to-End Testing
- 手動テスト: ターミナルで `python src/main.py` を 5〜10 秒実行し、秒間出力と 100 でのリセット動作を確認。
- ログへのリダイレクト (`python src/main.py > output.log`) を試み、フラッシュの効果でリアルタイムに追記されることを確認。
