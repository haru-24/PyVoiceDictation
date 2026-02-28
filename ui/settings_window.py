"""
設定ウィンドウUI（統合版）
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.config import config
from app.word_replacement import word_replacer

# ログファイルパス
LOG_FILE = Path.home() / ".sst-python" / "logs" / "voice_input.log"


class SettingsDialog(QDialog):
    """設定ダイアログ（メイン）"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("🎤🏻 音声入力設定")
        self.setMinimumSize(900, 700)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UIをセットアップ"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # タブウィジェット
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Helvetica", 12))

        # 設定タブ
        settings_tab = self._create_settings_tab()
        self.tabs.addTab(settings_tab, "⚙️ 設定")

        # ログタブ
        log_tab = self._create_log_tab()
        self.tabs.addTab(log_tab, "📋 ログ")

        # ワード変換タブ
        replacement_tab = self._create_replacement_tab()
        self.tabs.addTab(replacement_tab, "🔄 ワード変換")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def _create_settings_tab(self) -> QWidget:
        """設定タブを作成"""
        # 外側レイアウト（スクロールエリア + 固定ボタン行）
        outer_widget = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.setSpacing(0)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # ── スクロールエリア ───────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 15)

        # ── Gemini API 設定セクション ──────────────────────────────
        api_header = QLabel("🔑 Gemini API 設定")
        api_header.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        api_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(api_header)

        api_description = QLabel(
            "APIキーとモデルを設定すると音声認識結果の補正機能が有効になります。"
            "未設定の場合は補正機能が無効になります。"
        )
        api_description.setFont(QFont("Helvetica", 11))
        api_description.setStyleSheet("color: gray;")
        api_description.setWordWrap(True)
        layout.addWidget(api_description)

        # APIキー行
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("API キー:")
        api_key_label.setFont(QFont("Helvetica", 12))
        api_key_label.setFixedWidth(80)
        api_key_layout.addWidget(api_key_label)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setFont(QFont("Monaco", 12))
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Gemini API キーを入力...")
        self.api_key_edit.setText(config.gemini_api_key)
        api_key_layout.addWidget(self.api_key_edit)

        toggle_btn = QPushButton("表示")
        toggle_btn.setFixedWidth(60)
        toggle_btn.setCheckable(True)
        toggle_btn.setFont(QFont("Helvetica", 11))
        toggle_btn.toggled.connect(
            lambda checked: self.api_key_edit.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        api_key_layout.addWidget(toggle_btn)
        layout.addLayout(api_key_layout)

        # モデル行
        model_layout = QHBoxLayout()
        model_label = QLabel("モデル:")
        model_label.setFont(QFont("Helvetica", 12))
        model_label.setFixedWidth(80)
        model_layout.addWidget(model_label)

        self.model_edit = QLineEdit()
        self.model_edit.setFont(QFont("Monaco", 12))
        self.model_edit.setPlaceholderText("例: gemini-2.0-flash-exp")
        self.model_edit.setText(config.gemini_model)
        model_layout.addWidget(self.model_edit)
        layout.addLayout(model_layout)

        # Gemini設定ステータス + 保存ボタン
        gemini_btn_layout = QHBoxLayout()
        self.gemini_status_label = QLabel(
            "✅ Gemini補正: 有効"
            if config.gemini_enabled
            else "⚠️ Gemini補正: 無効（APIキーを設定してください）"
        )
        self.gemini_status_label.setFont(QFont("Helvetica", 11))
        self.gemini_status_label.setStyleSheet(
            "color: #4CAF50;" if config.gemini_enabled else "color: #FF9800;"
        )
        gemini_btn_layout.addWidget(self.gemini_status_label)
        gemini_btn_layout.addStretch()

        save_gemini_btn = QPushButton("💾 保存")
        save_gemini_btn.setMinimumSize(120, 36)
        save_gemini_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        save_gemini_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #388E3C; }
            """
        )
        save_gemini_btn.clicked.connect(self._on_save_gemini)
        gemini_btn_layout.addWidget(save_gemini_btn)
        layout.addLayout(gemini_btn_layout)

        # 区切り線
        line0 = QFrame()
        line0.setFrameShape(QFrame.Shape.HLine)
        line0.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line0)

        # ── プロンプト設定セクション ───────────────────────────────
        header = QLabel("🤖 Gemini 補正プロンプト設定")
        header.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        description = QLabel(
            "音声認識結果を補正するためのプロンプトを編集できます。"
            "{text} の部分に音声認識結果が挿入されます。"
        )
        description.setFont(QFont("Helvetica", 11))
        description.setStyleSheet("color: gray;")
        description.setWordWrap(True)
        layout.addWidget(description)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line1)

        # テキストエリア
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(config.gemini_prompt)
        self.text_edit.setFont(QFont("Monaco", 12))
        self.text_edit.setMinimumHeight(300)
        layout.addWidget(self.text_edit)

        # ステータスラベル
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Helvetica", 10))
        self.status_label.setStyleSheet("color: gray;")
        self.status_label.setMinimumHeight(20)
        layout.addWidget(self.status_label)

        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

        # ── 固定ボタン行（スクロール外）────────────────────────────
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        outer_layout.addWidget(line2)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(25, 10, 25, 10)
        button_layout.addStretch()

        cancel_btn = QPushButton("✖️ キャンセル")
        cancel_btn.setMinimumSize(140, 40)
        cancel_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #616161; }
            QPushButton:pressed { background-color: #424242; }
            """
        )
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        reset_btn = QPushButton("🔄 デフォルトに戻す")
        reset_btn.setMinimumSize(180, 40)
        reset_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        reset_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #F57C00; }
            QPushButton:pressed { background-color: #E65100; }
            """
        )
        reset_btn.clicked.connect(self._on_reset)
        button_layout.addWidget(reset_btn)

        save_btn = QPushButton("💾 保存")
        save_btn.setMinimumSize(140, 40)
        save_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #388E3C; }
            """
        )
        save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(save_btn)

        outer_layout.addLayout(button_layout)
        outer_widget.setLayout(outer_layout)
        return outer_widget

    def _create_log_tab(self) -> QWidget:
        """ログタブを作成"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # ヘッダー
        header = QLabel("📋 音声入力ログ")
        header.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # 説明
        description = QLabel("音声認識と入力のログをリアルタイムで表示します")
        description.setFont(QFont("Helvetica", 11))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: gray;")
        layout.addWidget(description)

        # 区切り線
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line1)

        # ログテキストエリア
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Monaco", 11))
        self.log_text.setMinimumHeight(400)
        self.log_text.setStyleSheet(
            """
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #3E3E3E;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )
        layout.addWidget(self.log_text)

        # ボタン群
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # クリアボタン
        clear_btn = QPushButton("🗑️ クリア")
        clear_btn.setMinimumSize(140, 40)
        clear_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        clear_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """
        )
        clear_btn.clicked.connect(self._on_clear_log)
        button_layout.addWidget(clear_btn)

        # 更新ボタン
        refresh_btn = QPushButton("🔄 更新")
        refresh_btn.setMinimumSize(140, 40)
        refresh_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        )
        refresh_btn.clicked.connect(self._on_refresh_log)
        button_layout.addWidget(refresh_btn)

        layout.addLayout(button_layout)
        widget.setLayout(layout)

        # 初回ロード
        self._load_log()

        return widget

    def _create_replacement_tab(self) -> QWidget:
        """ワード変換タブを作成"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # ヘッダー
        header = QLabel("🔄 ワード変換ルール")
        header.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # 説明
        description = QLabel(
            "音声認識結果の特定の文字列を別の文字列に変換します。ルールは上から順番に適用されます。"
        )
        description.setFont(QFont("Helvetica", 11))
        description.setStyleSheet("color: gray;")
        description.setWordWrap(True)
        layout.addWidget(description)

        # 区切り線
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line1)

        # テーブル
        self.replacement_table = QTableWidget()
        self.replacement_table.setColumnCount(2)
        self.replacement_table.setHorizontalHeaderLabels(["入力", "出力"])
        self.replacement_table.setFont(QFont("Helvetica", 12))
        header = self.replacement_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.replacement_table.setMinimumHeight(350)
        layout.addWidget(self.replacement_table)

        # ステータスラベル
        self.replacement_status_label = QLabel("")
        self.replacement_status_label.setFont(QFont("Helvetica", 10))
        self.replacement_status_label.setStyleSheet("color: gray;")
        self.replacement_status_label.setMinimumHeight(20)
        layout.addWidget(self.replacement_status_label)

        # 区切り線
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)

        # ボタン群
        button_layout = QHBoxLayout()

        # 追加ボタン
        add_btn = QPushButton("➕ 追加")
        add_btn.setMinimumSize(120, 40)
        add_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        )
        add_btn.clicked.connect(self._on_add_replacement_row)
        button_layout.addWidget(add_btn)

        # 削除ボタン
        delete_btn = QPushButton("🗑️ 削除")
        delete_btn.setMinimumSize(120, 40)
        delete_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """
        )
        delete_btn.clicked.connect(self._on_delete_replacement_row)
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()

        # 保存ボタン
        save_btn = QPushButton("💾 保存")
        save_btn.setMinimumSize(140, 40)
        save_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """
        )
        save_btn.clicked.connect(self._on_save_replacement)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        widget.setLayout(layout)

        # 初回ロード
        self._load_replacement_rules()

        return widget

    # ========== 設定タブのアクション ==========

    def _on_save_gemini(self) -> None:
        """Gemini API設定を保存"""
        api_key = self.api_key_edit.text().strip()
        model = self.model_edit.text().strip()

        if not model:
            self.gemini_status_label.setText("❌ モデル名を入力してください")
            self.gemini_status_label.setStyleSheet("color: red;")
            return

        try:
            config.save_gemini_settings(api_key, model)
            if config.gemini_enabled:
                self.gemini_status_label.setText("✅ Gemini補正: 有効")
                self.gemini_status_label.setStyleSheet("color: #4CAF50;")
            else:
                self.gemini_status_label.setText("⚠️ Gemini補正: 無効（APIキーを設定してください）")
                self.gemini_status_label.setStyleSheet("color: #FF9800;")
        except Exception as ex:
            self.gemini_status_label.setText(f"❌ 保存エラー: {ex}")
            self.gemini_status_label.setStyleSheet("color: red;")

    def _on_save(self) -> None:
        """保存ボタンのコールバック"""
        new_prompt = self.text_edit.toPlainText().strip()

        if not new_prompt:
            self.status_label.setText("❌ エラー: プロンプトを入力してください")
            self.status_label.setStyleSheet("color: red;")
            return

        if "{text}" not in new_prompt:
            # 警告ダイアログ
            reply = QMessageBox.question(
                self,
                "警告",
                "プロンプトに {text} が含まれていません。\n"
                "音声認識結果が挿入されない可能性があります。\n\n"
                "保存しますか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        try:
            config.save_prompt(new_prompt)
            self.status_label.setText(
                "✅ プロンプトを保存しました。次回の音声入力から反映されます。"
            )
            self.status_label.setStyleSheet("color: #4CAF50;")
        except Exception as ex:
            self.status_label.setText(f"❌ エラー: 保存に失敗しました: {ex}")
            self.status_label.setStyleSheet("color: red;")

    def _on_reset(self) -> None:
        """デフォルトに戻すボタンのコールバック"""
        reply = QMessageBox.question(
            self,
            "確認",
            "プロンプトをデフォルトに戻しますか？\n\n現在の内容は失われます。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                default_prompt = config.reset_prompt_to_default()
                self.text_edit.setPlainText(default_prompt)
                self.status_label.setText("✅ デフォルトプロンプトに戻しました")
                self.status_label.setStyleSheet("color: #4CAF50;")
            except Exception as ex:
                self.status_label.setText(f"❌ エラー: リセットに失敗しました: {ex}")
                self.status_label.setStyleSheet("color: red;")

    # ========== ワード変換タブのアクション ==========

    def _load_replacement_rules(self) -> None:
        """ワード変換ルールをテーブルに読み込む"""
        rules = word_replacer.get_rules()
        self.replacement_table.setRowCount(len(rules))
        for row, (input_word, output_word) in enumerate(rules):
            self.replacement_table.setItem(row, 0, QTableWidgetItem(input_word))
            self.replacement_table.setItem(row, 1, QTableWidgetItem(output_word))

    def _on_add_replacement_row(self) -> None:
        """空行を末尾に追加"""
        row = self.replacement_table.rowCount()
        self.replacement_table.insertRow(row)
        self.replacement_table.setItem(row, 0, QTableWidgetItem(""))
        self.replacement_table.setItem(row, 1, QTableWidgetItem(""))
        self.replacement_table.editItem(self.replacement_table.item(row, 0))

    def _on_delete_replacement_row(self) -> None:
        """選択行を削除"""
        selected_rows = sorted(
            {index.row() for index in self.replacement_table.selectedIndexes()},
            reverse=True,
        )
        for row in selected_rows:
            self.replacement_table.removeRow(row)

    def _on_save_replacement(self) -> None:
        """ワード変換ルールを保存"""
        rules = []
        for row in range(self.replacement_table.rowCount()):
            input_item = self.replacement_table.item(row, 0)
            output_item = self.replacement_table.item(row, 1)
            input_word = input_item.text().strip() if input_item else ""
            output_word = output_item.text().strip() if output_item else ""
            if input_word:
                rules.append((input_word, output_word))

        try:
            word_replacer.set_rules(rules)
            word_replacer.save_csv()
            self.replacement_status_label.setText("✅ 保存しました")
            self.replacement_status_label.setStyleSheet("color: #4CAF50;")
        except Exception as ex:
            self.replacement_status_label.setText(f"❌ エラー: 保存に失敗しました: {ex}")
            self.replacement_status_label.setStyleSheet("color: red;")

    # ========== ログタブのアクション ==========

    def _load_log(self) -> None:
        """ログファイルを読み込んで表示"""
        try:
            if LOG_FILE.exists():
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    self.log_text.setPlainText(log_content)
                    # 最後の行にスクロール
                    cursor = self.log_text.textCursor()
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.log_text.setTextCursor(cursor)
            else:
                self.log_text.setPlainText(
                    "ログファイルがまだ作成されていません。\n音声入力を開始するとログが記録されます。"
                )
        except Exception as ex:
            self.log_text.setPlainText(f"エラー: ログファイルの読み込みに失敗しました\n{ex}")

    def _on_refresh_log(self) -> None:
        """ログを更新"""
        self._load_log()

    def _on_clear_log(self) -> None:
        """ログをクリア"""
        reply = QMessageBox.question(
            self,
            "確認",
            "ログファイルをクリアしますか？\n\nこの操作は元に戻せません。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if LOG_FILE.exists():
                    LOG_FILE.unlink()
                self.log_text.setPlainText("ログをクリアしました。")
            except Exception as ex:
                self.log_text.setPlainText(f"エラー: ログのクリアに失敗しました\n{ex}")
