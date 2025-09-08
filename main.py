import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
from googletrans import Translator
import pyperclip

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Translator")
        self.setWindowIcon(QIcon.fromTheme("preferences-desktop-locale"))  # system icon
        self.setFixedSize(400, 250)  # small window size

        self.translator = Translator()

        # Input label and text field
        self.input_label = QLabel("Enter text:")
        self.input_label.setFont(QFont("Arial", 10))
        self.input_text = QTextEdit()
        self.input_text.setFont(QFont("Arial", 10))

        # Language selection
        self.lang_label = QLabel("Translate to:")
        self.lang_label.setFont(QFont("Arial", 10))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "hi", "fr", "de", "es", "zh-cn", "ja"])
        self.lang_combo.setCurrentText("en")

        # Output
        self.output_label = QLabel("Translated text:")
        self.output_label.setFont(QFont("Arial", 10))
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Arial", 10))
        self.output_text.setReadOnly(True)

        # Buttons
        self.translate_btn = QPushButton(QIcon.fromTheme("document-send"), " Translate")
        self.translate_btn.setIconSize(QSize(16, 16))  # small icon
        self.translate_btn.clicked.connect(self.translate_text)

        self.copy_btn = QPushButton(QIcon.fromTheme("edit-copy"), " Copy")
        self.copy_btn.setIconSize(QSize(16, 16))  # small icon
        self.copy_btn.clicked.connect(self.copy_text)

        # Layouts
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.translate_btn)
        btn_layout.addWidget(self.copy_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addLayout(lang_layout)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def translate_text(self):
        text = self.input_text.toPlainText().strip()
        if text:
            lang = self.lang_combo.currentText()
            try:
                translated = self.translator.translate(text, dest=lang)
                self.output_text.setPlainText(translated.text)
            except Exception as e:
                self.output_text.setPlainText(f"Error: {e}")

    def copy_text(self):
        text = self.output_text.toPlainText()
        if text:
            pyperclip.copy(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
