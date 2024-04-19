
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateTimeEdit
from bson import ObjectId
from PyQt5.QtCore import QDateTime, Qt
import pymongo

class EmployeeManagementWindow(QWidget):
    def __init__(self):
        super().__init__()

        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['employe']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)


        self.setWindowTitle('Gestión de Empleados')
        self.setGeometry(100, 100, 850, 600)
        self.employe = {}

        # Campos de entrada
        self.id_label = QLabel('Cédula:', self)
        self.id_label.setGeometry(50, 50, 100, 30)
        self.id_input = QLineEdit(self)
        self.id_input.setGeometry(200, 50, 200, 30)

        self.name_label = QLabel('Nombre:', self)
        self.name_label.setGeometry(50, 100, 100, 30)
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(200, 100, 200, 30)

        self.last_name_label = QLabel('Apellido:', self)
        self.last_name_label.setGeometry(50, 150, 100, 30)
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setGeometry(200, 150, 200, 30)

        self.phone_label = QLabel('Teléfono:', self)
        self.phone_label.setGeometry(50, 200, 100, 30)
        self.phone_input = QLineEdit(self)
        self.phone_input.setGeometry(200, 200, 200, 30)

        self.address_label = QLabel('Dirección:', self)
        self.address_label.setGeometry(50, 250, 100, 30)
        self.address_input = QLineEdit(self)
        self.address_input.setGeometry(200, 250, 200, 30)

        self.position_label = QLabel('Puesto:', self)
        self.position_label.setGeometry(450, 50, 100, 30)
        self.position_input = QLineEdit(self)
        self.position_input.setGeometry(600, 50, 200, 30)

        self.date_label = QLabel('Fecha de Ingreso:', self)
        self.date_label.setGeometry(450, 100, 150, 30)
        self.date_input = QDateTimeEdit(self)
        self.date_input.setGeometry(600, 100, 150, 30)
        self.date_input.setDisplayFormat('yyyy-MM-dd')  # Establecer el formato de visualización de la fecha

        self.is_manager_label = QLabel('¿Es Jefatura?', self)
        self.is_manager_label.setGeometry(450, 150, 150, 30)
        self.is_manager_combobox = QComboBox(self)
        self.is_manager_combobox.addItem('Sí')
        self.is_manager_combobox.addItem('No')
        self.is_manager_combobox.setGeometry(600, 150, 150, 30)

        # Botones
        self.save_button = QPushButton('Guardar', self)
        self.save_button.setGeometry(50, 300, 100, 30)

        self.delete_button = QPushButton('Eliminar', self)
        self.delete_button.setGeometry(180, 300, 100, 30)
        self.delete_button.setEnabled(False)

        self.update_button = QPushButton('Editar', self)
        self.update_button.setGeometry(560, 300, 100, 30)
        self.update_button.setEnabled(False)

        self.clear_button = QPushButton('Limpiar Campos', self)
        self.clear_button.setGeometry(310, 300, 120, 30)

        self.return_button = QPushButton('Regresar', self)
        self.return_button.setGeometry(450, 300, 100, 30)

        # Tabla para listar empleados
        self.employee_table = QTableWidget(self)
        self.employee_table.setGeometry(50, 350, 700, 200)
        self.employee_table.setColumnCount(8)
        self.employee_table.cellClicked.connect(self.populate_fields_from_table)
        self.employee_table.setHorizontalHeaderLabels(['Cédula', 'Nombre', 'Apellido', 'Teléfono', 'Dirección', 'Puesto', 'Fecha de Ingreso', 'Jefatura'])

        if self.collection.count_documents({}) > 0:
            self.populate_employe_table()

        # Conectar botones a funciones
        self.save_button.clicked.connect(self.save_employee)
        self.update_button.clicked.connect(self.update_employe)
        self.delete_button.clicked.connect(self.delete_employee)
        self.clear_button.clicked.connect(self.clear_fields)
        self.return_button.clicked.connect(self.return_to_previous_window)

    def save_employee(self):
        identification = self.id_input.text()
        name = self.name_input.text()
        lastname = self.last_name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        position = self.position_input.text()
        startDate = self.date_input.text()
        index = self.is_manager_combobox.currentIndex()
        isHead = self.is_manager_combobox.itemText(index)


        # Aquí podrías realizar la lógica para guardar el empleado en una base de datos o en otro almacenamiento
        if not identification or not name or not lastname or not phone or not address or not position or not startDate or not isHead:
            QMessageBox.warning(self, 'Advertencia', 'Debes completar toda la información')
            return
        else: 
            employe_data = {
                'identification': identification,
                'name': name,
                'lastname': lastname,
                'phone': phone,
                'address': address,
                'position': position,
                'startDate': startDate,
                'isHead': isHead,
                'goods': []
            }

            if not self.collection.find_one({'identification': identification}):
                self.collection.insert_one(employe_data)
                QMessageBox.information(self, 'Información', f"¡El empleado {name} ha sido registrado correctamente !")
            else:
                QMessageBox.critical(self, 'Error', 'Ya existe un empleado con esa cedula')
                self.id_input.clear()
                return
        
        self.populate_employe_table()

        # Limpiar campos después de guardar
        self.clear_fields()

    def update_employe(self):
        identification = self.id_input.text()
        name = self.name_input.text()
        lastname = self.last_name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        position = self.position_input.text()
        startDate = self.date_input.text()
        index = self.is_manager_combobox.currentIndex()
        isHead = self.is_manager_combobox.itemText(index)

        if not identification or not name or not lastname or not phone or not address or not position or not startDate or not isHead:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Empleado para editar')
        else:
            
            self.collection.replace_one(
                {'identification': self.employe['identification']},
                {
                    'identification': identification,
                    'name': name,
                    'lastname': lastname,
                    'phone': phone,
                    'address': address,
                    'position': position,
                    'startDate': startDate,
                    'isHead': isHead,
                }
            )

            QMessageBox.information(self, 'Información', f"¡Usuario {self.employe['name']} Editado correctamente !")    
            self.clear_fields()
            self.populate_employe_table()

    def delete_employee(self):
        identification = self.id_input.text()
        name = self.name_input.text()
        

        if not identification or not name:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Empleado para eliminar')
        else:
            employe_id = ObjectId(self.employe['_id'])
            result = self.collection.delete_one({'_id': employe_id})

            if result.deleted_count > 0:
                QMessageBox.information(self, 'Información', f"¡Empleado {self.employe['name']} eliminado correctamente !")    
                self.clear_fields()
                self.populate_employe_table()

    
    def populate_employe_table(self):
        self.employee_table.setRowCount(0) # Limpiar la tabla

        for employe in self.collection.find():
            row_position = self.employee_table.rowCount()
            self.employee_table.insertRow(row_position)
            self.employee_table.setItem(row_position, 0, QTableWidgetItem(employe['identification']))
            self.employee_table.setItem(row_position, 1, QTableWidgetItem(employe['name']))
            self.employee_table.setItem(row_position, 2, QTableWidgetItem(employe['lastname']))
            self.employee_table.setItem(row_position, 3, QTableWidgetItem(employe['phone']))
            self.employee_table.setItem(row_position, 4, QTableWidgetItem(employe['address']))
            self.employee_table.setItem(row_position, 5, QTableWidgetItem(employe['position']))
            self.employee_table.setItem(row_position, 6, QTableWidgetItem(employe['startDate']))
            self.employee_table.setItem(row_position, 7, QTableWidgetItem(employe['isHead']))
            self.employee_table.resizeColumnsToContents()

    def populate_fields_from_table(self, row, column):
        
        identification = self.employee_table.item(row, 0).text()

        self.employe = self.collection.find_one({'identification': identification })

        if self.employe:
            # botones a bloquear
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(True)
            self.update_button.setEnabled(True)
            self.id_input.setEnabled(False)

            self.id_input.setText(self.employe['identification'])
            self.name_input.setText(self.employe['name'])
            self.last_name_input.setText(self.employe['lastname'])
            self.phone_input.setText(self.employe['phone'])
            self.address_input.setText(self.employe['address'])
            self.position_input.setText(self.employe['position'])
            start_date_time = QDateTime.fromString(self.employe['startDate'], Qt.ISODate)
            start_date = start_date_time.date()
            self.date_input.setDate(start_date)
            self.is_manager_combobox.setCurrentText(self.employe['isHead'])


    def clear_fields(self):
        # Limpiar los campos de entrada
        self.id_input.clear()
        self.name_input.clear()
        self.last_name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.position_input.clear()
        start_date_time = QDateTime.fromString('2000-01-01', Qt.ISODate)
        start_date = start_date_time.date()
        self.date_input.setDate(start_date)
        self.is_manager_combobox.setCurrentIndex(0)
        self.save_button.setEnabled(True)
        self.delete_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.id_input.setEnabled(True)
        self.employe = {}

    def return_to_previous_window(self):
        # Aquí puedes implementar la lógica para regresar a la ventana anterior
        self.close()

    


