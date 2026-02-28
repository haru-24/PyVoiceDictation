"""
py2app ビルド設定
"""
from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,  # Dockに表示しない（メニューバーアプリ）
        'CFBundleName': 'STT音声入力',
        'CFBundleDisplayName': 'STT 音声入力',
        'CFBundleIdentifier': 'com.local.stt-python',
        'CFBundleVersion': '1.0.0',
        'NSMicrophoneUsageDescription': '音声入力のためマイクが必要です',
        'NSAppleEventsUsageDescription': 'テキスト入力のためアクセシビリティが必要です',
    },
    'packages': [
        'app', 'ui',
        'faster_whisper', 'ctranslate2',
        'sounddevice', '_sounddevice_data',
        'numpy', 'pynput', 'rumps',
        'PyQt6', 'google', 'pydantic',
        'dotenv', 'speech_recognition',
    ],
    'excludes': ['test'],
    'iconfile': None,  # アイコンがあれば 'assets/icon.icns' に設定
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
