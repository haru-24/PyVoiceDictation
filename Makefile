APP_NAME = PyVoDictation

.PHONY: build dist clean dev

dev:
	poetry run python main.py

build:
	poetry run pyinstaller PyVoDictation.spec --noconfirm

dist: build
	hdiutil create \
	  -volname "$(APP_NAME)" \
	  -srcfolder "dist/$(APP_NAME).app" \
	  -ov -format UDZO \
	  "dist/$(APP_NAME).dmg"
	@echo "✅ dist/$(APP_NAME).dmg を作成しました"

clean:
	rm -rf build/ dist/
