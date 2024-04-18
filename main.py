import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from main_window import MainWindow
import pymongo

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inicio de Sesión')


        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['user']

            admin = self.collection.find_one({'username': "admin"})

            if not admin:
                user_data = {
                    'name': "San",
                    'username': "admin",
                    'password': "1234"
                }

                self.collection.insert_one(user_data)

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)

        # Etiquetas y campos de entrada
        self.username_label = QLabel('Nombre de usuario:', self)
        self.username_label.setGeometry(50, 50, 200, 40)
        self.username_label.setStyleSheet('color: #333; font-size: 16px')

        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(250, 50, 200, 40)
        self.username_input.setFont(QFont("Arial", 10))

        self.password_label = QLabel('Contraseña:', self)
        self.password_label.setGeometry(50, 100, 200, 40)
        self.password_label.setStyleSheet('color: #333; font-size: 16px')

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(250, 100, 200, 40)
        self.password_input.setFont(QFont("Arial", 10))

        # Botón de inicio de sesión
        self.login_button = QPushButton('Iniciar Sesión', self)
        self.login_button.setGeometry(250, 160, 200, 40)
        self.login_button.setStyleSheet('background-color: #4CAF50; color: white; font-size: 16px')
        self.login_button.clicked.connect(self.openMainScreen)

        # Tamaño de la ventana
        self.setGeometry(100, 100, 600, 250)

    def openMainScreen(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Advertencia', 'Debes completar toda la información')
        else : 
            user_query = {'username': username, 'password': password}
            user = self.collection.find_one(user_query)

            if user:
                self.hide()  # Ocultar la ventana de inicio de sesión
                self.main_window = MainWindow()  # Crear una instancia de la ventana principal
                self.main_window.show()  # Mostrar la ventana principal
            else: 
                QMessageBox.warning(self, 'Error', 'Usuario no encontrado')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
