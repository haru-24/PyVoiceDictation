# sst-python プロジェクトメモリ

## 概要
macOS用 Push-to-Talk 音声入力ツール。右Commandキーを押している間録音し、離すとGoogle Speech Recognitionで文字起こし → アクティブウィンドウにテキスト入力。

## 詳細メモリファイル
- [architecture](architecture) - コード構成・依存関係
- [conventions](conventions) - コーディング規約
- [commands](commands) - 開発コマンド

## 重要な注意点
- STTバックエンドはGoogle Speech Recognitionのみ（Whisperは削除済み）
- 設定の保存先: `__generated__/.env`（開発時）、`~/Library/Application Support/stt-python/.env`（バンドル時）
- ログ出力: `~/.sst-python/logs/voice_input.log`
- 応答は日本語で行う
