from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import QSize, Qt

import threading
import socket
import time

with open('../config/NOTIFY_TIMEOUT', 'r') as f:
    NOTIFY_TIMEOUT = int(f.read())

with open('../config/NOTIFY_SERVER_PORT', 'r') as f:
    NOTIFY_SERVER_PORT = int(f.read())

_notify_app = QApplication([])

class Notification(QMainWindow):
    def __init__(self):
        super(Notification, self).__init__()
        self.setFixedSize(QSize(400, 100))
        self.move(-100, -100)
        self.setWindowTitle("Paket Defender Notify Service")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        self.setStyleSheet("background-color: #1e1e1e;")

        _screen_geometry = QApplication.primaryScreen().geometry()
        x = _screen_geometry.width() - self.frameGeometry().width() - 50
        y = _screen_geometry.height() - self.frameGeometry().height() - 50
        
        self.move(x, y)

        label = QLabel("   Paket Defender")
        label.setStyleSheet("color: white; font-size: 16px;")
        label.show()

        self.text = QLabel()
        self.text.setStyleSheet("color: gray; font-size: 14px;")

        minlayout = QVBoxLayout()
        minlayout.addWidget(label)
        minlayout.addWidget(self.text)

        maincontext = QWidget()
        maincontext.setLayout(minlayout)

        self.setCentralWidget(maincontext)
        threading.Thread(target=self.service, daemon=True).start()

    def service(self):
        time.sleep(1)
        self.hide()
        while True:
            try:
                notify_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                notify_server.bind(('0.0.0.0', NOTIFY_SERVER_PORT))

                notify_server.listen(32)

                with ThreadPoolExecutor(32) as executor:
                    while True:
                        cl, ip = notify_server.accept()
                        if ip[0] == '127.0.0.1':
                            executor.submit(self.msg_handler, cl)

            except Exception as e:
                print(e)
                time.sleep(3)

    def msg_handler(self, sock: socket.socket):
        try:
            with sock:
                text = sock.recv(1024).decode()
                with open('../data/logs.txt', 'a') as f:
                    f.write(f'{text}\n')
                    
                self.showmsg(text)
        except:
            pass

    def showmsg(self, text: str):
        text = f'   {text}'
        self.text.setText(text)

        self.show()
        time.sleep(NOTIFY_TIMEOUT)
        self.hide()

if __name__ == '__main__':
    _notify_window = Notification()
    _notify_window.show()
    #_notify_window.hide()
    _notify_app.exec()

