import sys, qdarktheme, keyboard, random, time, threading, json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, QTranslator, QEvent
from Scr.ui_main import Ui_MainWindow


class AICI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.show_stop_progress_page(False)
        self.setFixedSize(self.width(), self.height())

        self.trans = QTranslator(self)

        self.ui.themeComboBoxMainPage.currentTextChanged.connect(self.toggle_theme)
        self.ui.laguageComboBoxMainPage.currentTextChanged.connect(self.toggle_language)

        self.ui.newButtonMainPage.clicked.connect(self.new_button_main_page_clicked)
        self.ui.exitProgressPageButtonProgressPage.clicked.connect(self.exit_progress_page_clicked)
        self.ui.openFileButtonProgressPage.clicked.connect(self.open_file_button_progress_page_clicked)
        self.ui.startButtonProgressPage.clicked.connect(lambda: threading.Thread(target=self.start_button_progress_page_clicked).start())
        self.ui.saveProgressButtonProgressPage.clicked.connect(self.save_button_progress_tab_clicked)
        self.ui.openButtonMainPage.clicked.connect(self.open_button_main_page_clicked)
        self.ui.stopButtonProgressPage.clicked.connect(self.stop_button_progress_page_clicked)

        self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.valueChanged.connect(self.set_minimum_maximum_time_delay)
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.valueChanged.connect(self.set_minimum_maximum_time_delay)

        self.ui.contentPlainTextEditProgressPage.textChanged.connect(self.check_content_edit_progress_page_changed)
        
        self.ui.randomDelayTimeRadioButtonProgressPage.clicked.connect(lambda: self.radio_button_progress_page_clicked("RANDOM"))
        self.ui.fixedDelayTimeRadioButtonProgressPage.clicked.connect(lambda: self.radio_button_progress_page_clicked("FIXED"))
        self.currentDelayTimeMode = "FIXED"

        self.filePathProgressPage = None
        self.running = False
    

    def stop_button_progress_page_clicked(self):
        self.running = False
        self.set_enabled_progress_page(True)
        self.show_stop_progress_page(False)
    

    def show_stop_progress_page(self, show):
        if show:
            self.ui.stopButtonProgressPage.show()
            self.ui.startButtonProgressPage.hide()
        else:
            self.ui.stopButtonProgressPage.hide()
            self.ui.startButtonProgressPage.show()
    

    def open_button_main_page_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "AICI-ItCoder", "", "AICI-ItCoder Files (*.aicii)", options=options)
        if fileName:
            with open(fileName, "r", encoding="utf-8") as file:
                data = json.load(file)
            file.close()

            self.new_button_main_page_clicked()

            self.ui.waitTimeDoubleSpinBoxProgressPage.setValue(data["wait-time"])
            self.currentDelayTimeMode = data["delay-time-mode"]
            self.radio_button_progress_page_clicked(data["delay-time-mode"])
            if data["delay-time-mode"] == "RANDOM":
                self.ui.randomDelayTimeRadioButtonProgressPage.setChecked(True)
            else:
                self.ui.fixedDelayTimeRadioButtonProgressPage.setChecked(True)
            self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.setValue(data["fixed-delay-time"])
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setValue(data["random-delay-time-list"][0])
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setValue(data["random-delay-time-list"][1])
            self.ui.contentPlainTextEditProgressPage.setPlainText("\n".join(data["content"]))
            self.filePathProgressPage = data["file-path"]
            self.ui.filePathLineEditProgressPage.setText(data["file-path"])
    

    def clear_progress_page(self):
        self.ui.waitTimeDoubleSpinBoxProgressPage.setValue(5.00)
        self.currentDelayTimeMode = "FIXED"
        self.radio_button_progress_page_clicked(self.currentDelayTimeMode)
        if self.currentDelayTimeMode == "RANDOM":
            self.ui.randomDelayTimeRadioButtonProgressPage.setChecked(True)
        else:
            self.ui.fixedDelayTimeRadioButtonProgressPage.setChecked(True)
        self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.setValue(0.10)
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setValue(1.0)
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setValue(5.0)
        self.ui.contentPlainTextEditProgressPage.setPlainText("")
        self.filePathProgressPage = None
        self.ui.filePathLineEditProgressPage.setText("")
    

    def save_button_progress_tab_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "AICI-ItCoder", "Untitled-1.aicii", "AICI-ItCoder Files (*.aicii)", options=options)
        if fileName:
            data = {
                "wait-time": self.ui.waitTimeDoubleSpinBoxProgressPage.value(),
                "delay-time-mode": self.currentDelayTimeMode,
                "fixed-delay-time": self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.value(),
                "random-delay-time-list": [self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.value(), self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.value()],
                "content": self.ui.contentPlainTextEditProgressPage.toPlainText().split("\n"),
                "file-path": self.filePathProgressPage

            }
            with open(fileName, "w", encoding="utf-8") as file:
                json.dump(data, file)

            file.close()
    

    def check_content_edit_progress_page_changed(self):
        text = self.ui.contentPlainTextEditProgressPage.toPlainText()
        if bool(text):
            self.ui.startButtonProgressPage.setEnabled(True)
            self.ui.saveProgressButtonProgressPage.setEnabled(True)
        else:
            self.ui.startButtonProgressPage.setEnabled(False)
            self.ui.saveProgressButtonProgressPage.setEnabled(False)
    

    @pyqtSlot(float)
    def set_minimum_maximum_time_delay(self):
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setMaximum(self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.value())
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setMinimum(self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.value() + 1)
    

    def set_enabled_progress_page(self, enabled: bool = True):
        self.ui.saveProgressButtonProgressPage.setEnabled(enabled)
        self.ui.exitProgressPageButtonProgressPage.setEnabled(enabled)
        self.ui.fixedDelayTimeRadioButtonProgressPage.setEnabled(enabled)
        self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.setEnabled(enabled)
        self.ui.randomDelayTimeRadioButtonProgressPage.setEnabled(enabled)
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setEnabled(enabled)
        self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setEnabled(enabled)
        self.ui.contentPlainTextEditProgressPage.setEnabled(enabled)
        self.ui.openFileButtonProgressPage.setEnabled(enabled)
        self.ui.filePathLineEditProgressPage.setEnabled(enabled)
        self.ui.startButtonProgressPage.setEnabled(enabled)
        self.ui.autoBeauSourceCodeIdeItCoderCheckBoxProgressPage.setEnabled(enabled)


    def handles_content_formatting(self, content): 
        return "\n".join([i.replace("\t", "    ").strip() for i in content.split('\n')])
    

    def start_button_progress_page_clicked(self):
        aBSCI = self.ui.autoBeauSourceCodeIdeItCoderCheckBoxProgressPage.isChecked()

        waitTime = self.ui.waitTimeDoubleSpinBoxProgressPage.value()
        content = self.handles_content_formatting(self.ui.contentPlainTextEditProgressPage.toPlainText()) if aBSCI else self.ui.contentPlainTextEditProgressPage.toPlainText()
        self.running = True

        self.set_enabled_progress_page(False)

        time.sleep(waitTime)
        
        if self.running:
            self.show_stop_progress_page(True)
            if self.currentDelayTimeMode == "RANDOM":
                for t in content:
                    delayTime = random.randint(self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.value(), self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.value())
                    keyboard.write(t)
                    if t == "{" and aBSCI:
                        keyboard.press("right")
                        keyboard.press("backspace")

                    if not self.running:
                        return
                    
                    time.sleep(delayTime)

            elif self.currentDelayTimeMode == "FIXED":
                delayTime = self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.value()
                for t in content:
                    keyboard.write(t)
                    if t == "{" and aBSCI:
                        keyboard.press("right")
                        keyboard.press("backspace")

                    if not self.running:
                        return
                    
                    time.sleep(delayTime)
        
        self.running = False
        self.set_enabled_progress_page(True)
        self.show_stop_progress_page(False)
    

    def open_file_button_progress_page_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "AICI-ItCoder", self.filePathProgressPage if bool(self.filePathProgressPage) else "", "All Files (*)", options=options)
        if fileName:
            self.ui.contentPlainTextEditProgressPage.clear()
            
            with open(fileName, "r", encoding="utf-8") as file:
                try:
                    content = file.readlines()
                except UnicodeDecodeError:
                    content = ["..."]
            
            self.ui.contentPlainTextEditProgressPage.setPlainText("".join(content))
            self.ui.filePathLineEditProgressPage.setText(fileName)

            self.filePathProgressPage = fileName
            file.close()

    
    def radio_button_progress_page_clicked(self, name):
        if name == "RANDOM":
            self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.setEnabled(False)
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setEnabled(True)
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setEnabled(True)
            self.currentDelayTimeMode = "RANDOM"
        elif name == "FIXED":
            self.ui.fixedDelayTimeDoubleSpinBoxProgressPage.setEnabled(True)
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage1.setEnabled(False)
            self.ui.randomDelayTimeDoubleSpinBoxProgressPage2.setEnabled(False)
            self.currentDelayTimeMode = "FIXED"

    
    def exit_progress_page_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.mainPage)
        self.clear_progress_page()
    

    def new_button_main_page_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.progressPage)
    

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super().changeEvent(event)
    

    def closeEvent(self, event):
        if self.running:
            event.ignore()
        else:
            event.accept()
    

    @pyqtSlot(str)
    def toggle_language(self):
        index = self.ui.laguageComboBoxMainPage.currentIndex()
        if index == 0:  # Tiếng Việt
            QApplication.instance().removeTranslator(self.trans)
        elif index == 1:  # English
            self.trans.load("./Data/Languages/lang-en.qm")
            QApplication.instance().installTranslator(self.trans)

    
    @pyqtSlot(str)
    def toggle_theme(self):
        index = self.ui.themeComboBoxMainPage.currentIndex()
        if index == 0:  # System
            qdarktheme.setup_theme("auto")
        elif index == 1:  # Light
            qdarktheme.setup_theme("light")
        elif index == 2:  # Dark
            qdarktheme.setup_theme("dark")


if __name__ == "__main__":
    # qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")  # Setup system theme
    ems = AICI()
    ems.show()
    sys.exit(app.exec_())