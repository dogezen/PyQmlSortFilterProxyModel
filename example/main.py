import os
import sys

# adding qmlsortfilterproxymodel to import path
currentFolderPath = os.path.dirname(__file__)
srcFolderPath = os.path.abspath(os.path.join(currentFolderPath, '../src'))
sys.path.insert(0, srcFolderPath)

import qmlsortfilterproxymodel


from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

qmlsortfilterproxymodel.registerQmlTypes()

qmlFilePath = os.path.join(currentFolderPath, 'main.qml')
engine.load(qmlFilePath)

sys.exit(app.exec())