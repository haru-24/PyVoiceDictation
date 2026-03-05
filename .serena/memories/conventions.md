# コーディング規約

## 言語・スタイル
- Python 3.10+
- Type Hints 必須
- docstring は日本語
- 命名: PascalCase（クラス）、snake_case（関数/変数）、UPPER_SNAKE_CASE（定数）、`_` prefix（プライベート）
- 行長: 100文字（ruff設定）

## 設計パターン
- 1ファイル1クラス
- 依存関係は一方向（循環依存禁止）
- スレッドセーフ: `threading.Lock` で共有状態を保護
- 遅延ロード + ダブルチェックロッキング（重いリソース初期化）
- 設定は `app/config.py` の `AppConfig` に集約、ハードコーディング禁止
- グローバルシングルトンインスタンスをモジュールレベルで定義

## ログ
- `logging` モジュール使用（`print` は使わない）
- ログフォーマット: `[タグ] メッセージ`
- STT結果: `[STT] テキスト`
- Gemini補正結果: `[Gemini補正] テキスト`（変更時のみ）
- ワード変換結果: `[ワード変換] テキスト`（変更時のみ）

## 設定管理
- Pydantic BaseModel で型安全な設定
- `.env` ファイルから `load_dotenv` で読み込み
- `set_key` で `.env` に書き込み
- UIから変更した場合はインメモリも即時更新
