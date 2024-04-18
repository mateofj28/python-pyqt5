
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from bson import ObjectId
import pymongo

class UserManagementWindow(QWidget):
    def __init__(self):
        super().__init__()

        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['user']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)

        
        self.setWindowTitle('Gestión de Usuarios')
        self.setGeometry(100, 100, 600, 500)
        self.user = {}

        # Campos de entrada
        self.name_label = QLabel('Nombre:', self)
        self.name_label.setGeometry(50, 50, 100, 30)

        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(200, 50, 200, 30)

        self.username_label = QLabel('Nombre de usuario', self)
        self.username_label.setGeometry(50, 100, 100, 30)

        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(200, 100, 200, 30)

        self.password_label = QLabel('Contraseña:', self)
        self.password_label.setGeometry(50, 150, 100, 30)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(200, 150, 200, 30)

        # Botones
        self.save_button = QPushButton('Guardar', self)
        self.save_button.setGeometry(200, 200, 80, 30)
        

        self.delete_button = QPushButton('Eliminar', self)
        self.delete_button.setGeometry(300, 200, 80, 30)
        self.delete_button.setEnabled(False)

        self.clear_button = QPushButton('Limpiar Campos', self)
        self.clear_button.setGeometry(400, 200, 120, 30)

        # Tabla para listar usuarios
        self.user_table = QTableWidget(self)
        self.user_table.resizeColumnsToContents()
        self.user_table.move(150, 260)
        self.user_table.setFixedHeight(220)
        self.user_table.setColumnCount(2)
        self.user_table.cellClicked.connect(self.populate_fields_from_table)
        self.user_table.setHorizontalHeaderLabels(['Nombre', 'Nombre de usuario'])

        if self.collection.count_documents({}) > 0:
            self.populate_user_table()

        # Botón para regresar a la ventana anterior
        self.back_button = QPushButton('Regresar', self)
        self.back_button.setGeometry(420, 450, 100, 30)
        self.back_button.clicked.connect(self.returnToPreviousWindow)

        # Botón para regresar a la ventana anterior
        self.update_button = QPushButton('Editar', self)
        self.update_button.setGeometry(50, 200, 100, 30)
        self.update_button.clicked.connect(self.update_user)
        self.update_button.setEnabled(False)

        # Conectar botones a funciones
        self.save_button.clicked.connect(self.save_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.clear_button.clicked.connect(self.clear_fields)

    def save_user(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        # Aquí podrías realizar la lógica para guardar el usuario en una base de datos o en otro almacenamiento
        if not name or not username or not password:
            QMessageBox.warning(self, 'Advertencia', 'Debes completar toda la información')
            return
        else: 
            user_data = {
                'name': name,
                'username': username,
                'password': password
            }

            self.collection.insert_one(user_data)

            QMessageBox.information(self, 'Información', f"¡El usuario {name} ha sido registrado correctamente !")

        
        self.populate_user_table()

        # Limpiar campos después de guardar
        self.clear_fields()



    def update_user(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not name or not username or not password:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Usuario para editar')
        else:
            
            self.collection.replace_one(
                {'username': self.user['username']},
                {
                    "name": name,
                    "username": username,
                    "password": password
                }
            )

            QMessageBox.information(self, 'Información', f"¡Usuario {self.user['name']} Editado correctamente !")    
            self.clear_fields()
            self.populate_user_table()
            
                

    def delete_user(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not name or not username or not password:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Usuario para eliminar')
        else:
            user_id = ObjectId(self.user['_id'])
            result = self.collection.delete_one({'_id': user_id})

            if result.deleted_count > 0:
                QMessageBox.information(self, 'Información', f"¡Usuario {self.user['name']} eliminado correctamente !")    
                self.clear_fields()
                self.populate_user_table()
        

    def clear_fields(self):
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.user = {}
        self.save_button.setEnabled(True)
        self.delete_button.setEnabled(False)
        self.update_button.setEnabled(False)

    def populate_user_table(self):
        self.user_table.setRowCount(0) # Limpiar la tabla

        for user in self.collection.find():
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            self.user_table.setItem(row_position, 0, QTableWidgetItem(user['name']))
            self.user_table.setItem(row_position, 1, QTableWidgetItem(user['username']))
            self.user_table.resizeColumnsToContents()

            

    def populate_fields_from_table(self, row, column):
        
        username = self.user_table.item(row, 1).text()

        self.user = self.collection.find_one({'username': username })

        if self.user:
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(True)
            self.update_button.setEnabled(True)
            self.name_input.setText(self.user['name'])
            self.username_input.setText(self.user['username'])
            self.password_input.setText(self.user['password'])
            



    def returnToPreviousWindow(self):
        self.close()  # Cierra la ventana actual

        



