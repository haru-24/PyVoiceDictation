# アーキテクチャ

## ファイル構成
```
main.py               # エントリポイント + VoiceInputApp (rumps)
app/
  config.py           # AppConfig (Pydantic) + グローバル config インスタンス
  google_speech.py    # GoogleSpeechTranscriber
  gemini.py           # GeminiCorrector + グローバル gemini インスタンス
  engine.py           # VoiceInputEngine (録音・文字起こし・入力統合) + type_text()
  word_replacement.py # WordReplacer + グローバル word_replacer インスタンス
  settings.py         # SettingsWindow (別プロセスでQtウィンドウ起動)
ui/
  settings_window.py  # SettingsDialog (PyQt6)
config/
  settings.json       # サウンド設定など
__generated__/
  .env                # APIキー等（開発時）
  prompts.json        # Geminiプロンプト
test/
  test_gemini.py
  test_text_input.py
```

## 依存関係（一方向）
```
config.py ← 依存なし
gemini.py ← config
google_speech.py ← config
engine.py ← config, google_speech, gemini, word_replacement
main.py   ← engine, gemini, google_speech, config, settings
ui/settings_window.py ← config, gemini, word_replacement
```

## モジュールレベルインスタンス
- `app.config.config` - AppConfig シングルトン
- `app.gemini.gemini` - GeminiCorrector シングルトン
- `app.word_replacement.word_replacer` - WordReplacer シングルトン

## テキスト処理フロー
1. `[STT]` Google Speech Recognition → テキスト
2. `[Gemini補正]` Gemini API補正（APIキー設定時のみ、変更があれば）
3. `[ワード変換]` WordReplacer適用（変更があれば）
4. CoreGraphicsでアクティブウィンドウに入力

## 設定ファイルパス
- 開発時: `__generated__/.env`, `__generated__/prompts.json`, `config/settings.json`
- バンドル時: `~/Library/Application Support/stt-python/`
