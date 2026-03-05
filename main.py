"""
Mac用 Push-to-Talk 音声入力ツール
==================================
右Commandキーを押している間だけ録音し、離すとGoogle Speech Recognitionで文字起こしして
アクティブなウィンドウ（ターミナル、Claude Code等）にテキスト入力する。

macOSの設定:
    システム設定 → プライバシーとセキュリティ → アクセシビリティ
    → ターミナル（またはPythonの実行環境）を許可

使い方:
    python main.py
    → メニューバーに🎤アイコンが表示される
    → 右Commandキーを押しながら話す → 離すとテキスト入力
"""

import multiprocessing
import sys
import time
from pathlib import Path

from app.config import config
from app.engine import VoiceInputEngine
from app.gemini import GeminiCorrector
from app.google_speech import GoogleSpeechTranscriber
from app.settings import SettingsWindow


def _menubar_icon_path() -> str:
    """メニューバーアイコンのパスを返す（開発時・バンドル時対応）"""
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent
    return str(base / "assets" / "menubar.png")


# rumpsのインポート試行
try:
    import rumps

    class VoiceInputApp(rumps.App):
        """メニューバーUI"""

        _status_item: rumps.MenuItem
        _sound_item: rumps.MenuItem

        def __init__(self) -> None:
            super().__init__("", icon=_menubar_icon_path(), quit_button="終了")
            self._status_item = rumps.MenuItem("待機中...")
            # STTバックエンド表示
            backend_info = f"STT: Google Speech ({config.language})"

            # サウンド設定メニュー項目
            self._sound_item = rumps.MenuItem("🔊 サウンド", callback=self.toggle_sound)
            self._sound_item.state = config.sound_enabled

            # 設定ウィンドウのインスタンス
            self._settings_window = SettingsWindow()

            self.menu = [
                self._status_item,
                None,
                rumps.MenuItem(backend_info),
                None,
                self._sound_item,
                rumps.MenuItem("設定", callback=self.open_settings),
            ]

        def set_recording(self) -> None:
            self._status_item.title = "🗣️ 録音中..."

        def set_processing(self) -> None:
            self._status_item.title = "👨🏻‍💻 変換中..."

        def set_idle(self) -> None:
            self._status_item.title = "待機中..."

        def set_error(self, msg: str) -> None:
            self._status_item.title = f"⚠️ {msg}"

        def toggle_sound(self, sender: rumps.MenuItem) -> None:
            """サウンドのON/OFFを切り替え"""
            new_state = not sender.state
            sender.state = new_state
            config.save_sound_setting(new_state)
            status = "有効" if new_state else "無効"
            print(f"[設定] サウンド再生を{status}にしました")

        def open_settings(self, _) -> None:
            """設定ウィンドウを開く"""
            self._settings_window.show()

    HAS_RUMPS = True
except ImportError:
    HAS_RUMPS = False
    VoiceInputApp = None  # type: ignore
    print("rumps未インストール。メニューバーUIなしで動作します。")


def main() -> None:
    """メイン関数"""
    transcriber = GoogleSpeechTranscriber()
    transcriber.load()
    gemini = GeminiCorrector()

    if HAS_RUMPS:
        app = VoiceInputApp()
        engine = VoiceInputEngine(transcriber, gemini, app=app)
        engine.start_keyboard_listener()
        app.run()
    else:
        engine = VoiceInputEngine(transcriber, gemini)
        engine.start_keyboard_listener()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    multiprocessing.freeze_support()  # PyInstallerバンドル時に必須
    main()
