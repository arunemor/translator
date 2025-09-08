# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QTextEdit, QComboBox, 
#     QVBoxLayout, QSystemTrayIcon, QMenu, QAction
# )
# from PyQt5.QtGui import QIcon, QFont, QPixmap
# from PyQt5.QtCore import Qt, QTimer
# from googletrans import Translator
# import pyperclip

# class RobotoTranslator(QWidget):
#     def __init__(self):
#         super().__init__()
#         # Window settings
#         self.setWindowFlags(Qt.WindowStaysOnTopHint)
#         self.setMinimumSize(300, 150)
#         self.setWindowTitle("Mini Translator")

#         self.translator = Translator()
#         self.last_clipboard = ""

#         # Clipboard timer
#         self.clipboard_timer = QTimer()
#         self.clipboard_timer.timeout.connect(self.check_clipboard)

#         # Roboto font
#         self.roboto_font = QFont("Roboto", 10)

#         # Language selection
#         self.lang_combo = QComboBox()
#         self.lang_combo.addItems(["en", "hi", "fr", "de", "es", "zh-cn", "ja"])
#         self.lang_combo.setCurrentText("hi")
#         self.lang_combo.setFont(self.roboto_font)

#         # Output text
#         self.output_text = QTextEdit()
#         self.output_text.setReadOnly(True)
#         self.output_text.setFont(self.roboto_font)
#         self.output_text.setStyleSheet(
#             "background-color: #f0f0f0; border: 1px solid #ccc; padding: 4px;"
#         )

#         # Layout
#         layout = QVBoxLayout()
#         layout.setContentsMargins(5,5,5,5)
#         layout.addWidget(self.lang_combo)
#         layout.addWidget(self.output_text)
#         self.setLayout(layout)

#     # Clipboard monitor
#     def translate_text(self, text):
#         lang = self.lang_combo.currentText()
#         try:
#             translated = self.translator.translate(text, dest=lang)
#             self.output_text.setPlainText(translated.text)
#         except Exception as e:
#             self.output_text.setPlainText(f"Error: {e}")

#     def check_clipboard(self):
#         try:
#             clipboard_text = pyperclip.paste().strip()
#         except:
#             return
#         if clipboard_text and clipboard_text != self.last_clipboard:
#             self.last_clipboard = clipboard_text
#             self.translate_text(clipboard_text)

    
#     # Show popup and start clipboard monitoring
#     def popup(self):
#         self.show()
#         self.clipboard_timer.start(500)

#     # Hide popup and stop monitoring
#     def hide_popup(self):
#         self.clipboard_timer.stop()
#         self.hide()


# # Main
# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(False)

# # System tray icon
# pixmap = QPixmap(32,32)
# pixmap.fill(Qt.transparent)  # transparent background
# icon = QIcon("translator.png")  # small attractive PNG icon
# if icon.isNull():
#     pixmap.fill(Qt.blue)
#     icon = QIcon(pixmap)

# tray_icon = QSystemTrayIcon(icon, app)
# menu = QMenu()

# translator_popup = RobotoTranslator()

# # Tray menu actions
# show_action = QAction("Open Translator")
# show_action.triggered.connect(translator_popup.popup)
# menu.addAction(show_action)

# hide_action = QAction("Hide Translator")
# hide_action.triggered.connect(translator_popup.hide_popup)
# menu.addAction(hide_action)

# quit_action = QAction("Quit")
# quit_action.triggered.connect(app.quit)
# menu.addAction(quit_action)

# tray_icon.setContextMenu(menu)
# tray_icon.show()

# sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QComboBox, QVBoxLayout,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from googletrans import Translator
import pyperclip

class RealTimeTranslator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(300, 150)
        self.setWindowTitle("Mini Translator")

        self.translator = Translator()
        self.last_clipboard = ""

        # Clipboard timer
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)

        # Roboto font
        self.roboto_font = QFont("Roboto", 10)

        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "hi", "fr", "de", "es", "zh-cn", "ja"])
        self.lang_combo.setCurrentText("hi")
        self.lang_combo.setFont(self.roboto_font)
        self.lang_combo.currentIndexChanged.connect(self.update_translation)

        # Output text
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(self.roboto_font)
        self.output_text.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #ccc; padding: 4px;"
        )

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.addWidget(self.lang_combo)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        # Store current clipboard text
        self.current_text = ""

    # Clipboard monitor
    def check_clipboard(self):
        try:
            clipboard_text = pyperclip.paste().strip()
        except:
            return
        if clipboard_text and clipboard_text != self.last_clipboard:
            self.last_clipboard = clipboard_text
            self.current_text = clipboard_text
            self.translate_text(clipboard_text)

    def translate_text(self, text):
        lang = self.lang_combo.currentText()
        try:
            translated = self.translator.translate(text, dest=lang)
            self.output_text.setPlainText(translated.text)
        except Exception as e:
            self.output_text.setPlainText(f"Error: {e}")

    # Called when language selection changes
    def update_translation(self):
        if self.current_text:
            self.translate_text(self.current_text)

    # Show popup and start clipboard monitoring
    def popup(self):
        self.show()
        self.clipboard_timer.start(500)

    # Hide popup and stop monitoring
    def hide_popup(self):
        self.clipboard_timer.stop()
        self.hide()


# Main
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# System tray icon
pixmap = QPixmap(32,32)
pixmap.fill(Qt.transparent)
icon = QIcon("translator.png")  # place your small attractive PNG icon
if icon.isNull():
    pixmap.fill(Qt.blue)
    icon = QIcon(pixmap)

tray_icon = QSystemTrayIcon(icon, app)
menu = QMenu()

translator_popup = RealTimeTranslator()

# Tray menu actions
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
