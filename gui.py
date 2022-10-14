import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import main
import threading
import stt

bActive = False

class AssistentUI(QtWidgets.QMainWindow):
	def __init__(self):
		super(AssistentUI, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.init_UI()

	def init_UI(self):
		self.setWindowTitle('Иннокентий')
		self.setWindowIcon(QIcon('favicon.png'))
		self.ui.pushButton.clicked.connect(self.start_thread_assist)

	def OnAssistent(self):
		global bActive

		if bActive == False:
			self.ui.pushButton.setText("ВЫКЛЮЧИТЬ")
			self.ui.label_3.setText("ВКЛЮЧЕН")
			bActive = True
			stt.bActiveA = True
			main.startAssistent()
		else:
			self.ui.pushButton.setText("ВКЛЮЧИТЬ")
			self.ui.label_3.setText("ВЫКЛЮЧЕН")
			bActive = False
			stt.bActiveA = False


	def start_thread_assist(self):
		thread = threading.Thread(target=self.OnAssistent, args=())
		thread.start()

	def closeEvent(self, event):
		stt.bActiveA = False
		event.accept()

app = QtWidgets.QApplication([])
application = AssistentUI()
application.show()

sys.exit(app.exec())
self.MainWindow.closeEvent = lambda event : self.closeEvent(event)