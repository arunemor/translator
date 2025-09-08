import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox, QVBoxLayout, 
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint
from googletrans import Translator
import pyperclip

class PopupTranslator(QWidget):
    def __init__(self):
        super().__init__()
        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(220, 70)
        self.setWindowTitle("Translator")
        
        self.translator = Translator()
        self.last_clipboard = ""

        # Clipboard timer
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)

        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "hi", "fr", "de", "es", "zh-cn", "ja"])
        self.lang_combo.setCurrentText("hi")

        # Output
        self.output_text = QLineEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translation appears here")

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.addWidget(self.lang_combo)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        # Dragging
        self.old_pos = None

    # Dragging events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # Clipboard monitor
    def check_clipboard(self):
        try:
            clipboard_text = pyperclip.paste().strip()
        except:
            return
        if clipboard_text and clipboard_text != self.last_clipboard:
            self.last_clipboard = clipboard_text
            self.translate_text(clipboard_text)

    def translate_text(self, text):
        lang = self.lang_combo.currentText()
        try:
            translated = self.translator.translate(text, dest=lang)
            self.output_text.setText(translated.text)
        except Exception as e:
            self.output_text.setText(f"Error: {e}")

    # Show popup and start clipboard monitoring
    def popup(self):
        self.show()
        self.clipboard_timer.start(500)  # check every 0.5s

    # Hide popup and stop monitoring
    def hide_popup(self):
        self.clipboard_timer.stop()
        self.hide()


# Main application
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create a simple built-in icon (avoids missing icon warning)
pixmap = QPixmap(16,16)
pixmap.fill(Qt.blue)  # simple blue square
icon = QIcon(pixmap)

tray_icon = QSystemTrayIcon(icon, app)
menu = QMenu()

translator_popup = PopupTranslator()

# Show/hide actions
show_action = QAction("Open Translator")
show_action.triggered.connect(translator_popup.popup)
menu.addAction(show_action)

hide_action = QAction("Hide Translator")
hide_action.triggered.connect(translator_popup.hide_popup)
menu.addAction(hide_action)

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

tray_icon.setContextMenu(menu)
tray_icon.show()

sys.exit(app.exec_())
