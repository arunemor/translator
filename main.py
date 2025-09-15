import sys
import os
import pyperclip
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QComboBox, QVBoxLayout,
    QPushButton, QHBoxLayout, QMenu
)
from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QRegion
from deep_translator import GoogleTranslator

if not os.environ.get("DISPLAY"):
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

# -------------------- Floating Draggable Circular Icon --------------------
class MiniIcon(QWidget):
    """Black circular icon with 'A' that opens the translator/chat popup"""
    def __init__(self, translator_popup):
        super().__init__()
        self.translator_popup = translator_popup
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setGeometry(1300, 700, 50, 50)
        self.setStyleSheet("background: transparent;")
        self.old_pos = None  # for dragging
        self.setMask(QRegion(0, 0, 50, 50, QRegion.Ellipse))
        self.show()

        # Right-click menu to exit
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu()
        exit_action = menu.addAction("Exit Bot")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == exit_action:
            QApplication.quit()  # Exit app completely

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Open popup near the icon
            icon_geo = self.geometry()
            self.translator_popup.move(icon_geo.x() - 250, icon_geo.y() - 50)  # Popup appears near icon
            self.translator_popup.show()
            self.old_pos = event.globalPos()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))  # Black circle
        painter.setPen(QPen(Qt.black))
        painter.drawEllipse(0, 0, 50, 50)

        painter.setPen(QPen(Qt.white))
        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "A")


# -------------------- Translator/Chat Popup --------------------
class MiniTranslator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(1100, 400, 300, 250)
        self.setStyleSheet("""
            background-color: #1e1e2f;
            border-radius: 12px;
            border: 2px solid #6a11cb;
        """)
        self.old_pos = None  # for dragging

        # ---------------- Buttons ----------------
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.setStyleSheet("color:white; background: #ff4c4c; border:none;")
        self.close_btn.clicked.connect(self.hide)

        self.minimize_btn = QPushButton("—")
        self.minimize_btn.setFixedSize(25, 25)
        self.minimize_btn.setStyleSheet("color:white; background: #4c6aff; border:none;")
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedSize(50,25)
        self.clear_btn.setStyleSheet("color:white; background: #00c853; border:none;")
        self.clear_btn.clicked.connect(lambda: self.text_area.clear())

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.minimize_btn)
        btn_layout.addWidget(self.close_btn)
        btn_layout.setContentsMargins(5,5,5,5)

        # ---------------- Language Selection & Text Area ----------------
        self.language_box = QComboBox()
        self.language_box.addItems(["hi", "en", "es", "fr", "de", "zh", "ar"])
        self.language_box.setStyleSheet("background-color: #6a11cb; color:white; border-radius:5px; padding:2px;")
        self.language_box.currentIndexChanged.connect(self.translate_last_text)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            background-color: #2b2b3f;
            color:white;
            border-radius:5px;
        """)

        # ---------------- Layout ----------------
        layout = QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(self.language_box)
        layout.addWidget(self.text_area)
        layout.setContentsMargins(5,5,5,5)
        self.setLayout(layout)

        # ---------------- Clipboard Monitoring ----------------
        self.last_text = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)

    # ---------------- Drag Events ----------------
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # ---------------- Clipboard & Translation ----------------
    def check_clipboard(self):
        text = pyperclip.paste()
        if text != self.last_text:
            self.last_text = text
            self.translate_text(text)

    def translate_last_text(self):
        if self.last_text:
            self.translate_text(self.last_text)

    def translate_text(self, text):
        try:
            target_lang = self.language_box.currentText()
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            self.text_area.setText(translated)
        except Exception as e:
            self.text_area.setText(f"Error: {e}")


# -------------------- Main --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    translator_popup = MiniTranslator()
    icon = MiniIcon(translator_popup)

    sys.exit(app.exec_())

 
