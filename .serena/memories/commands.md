# 開発コマンド

## 実行
```bash
make dev                          # アプリ起動（= poetry run python main.py）
poetry run python main.py         # 直接起動
```

## テスト・チェック
```bash
python -m py_compile app/config.py app/engine.py app/gemini.py main.py  # 構文チェック
poetry run python -m pytest test/ -v                                      # テスト実行
```

## Lint・フォーマット
```bash
poetry run ruff check .           # lint
poetry run ruff format .          # フォーマット
```

## ビルド・配布
```bash
make build   # PyInstallerでバンドル → dist/PyVoDictation.app
make dist    # .app → .dmg 作成
make clean   # build/ dist/ 削除
```

## パッケージ管理
```bash
poetry install                    # 依存関係インストール
poetry add <package>              # パッケージ追加
```

## ログ確認
```bash
tail -f ~/.sst-python/logs/voice_input.log
```
