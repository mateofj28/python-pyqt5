
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
import pymongo
from bson import ObjectId

class DepartmentManagementWindow(QWidget):
    def __init__(self):
        super().__init__()


        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['deparments']
            self.collectionEmploye = self.db['employe']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)


        self.setWindowTitle('Gestión de Departamentos')
        self.setGeometry(100, 100, 800, 450)
        self.departments = {}

        # Campos de entrada
        self.code_label = QLabel('Código:', self)
        self.code_label.setGeometry(50, 50, 100, 30)
        self.code_input = QLineEdit(self)
        self.code_input.setGeometry(150, 50, 200, 30)

        self.name_label = QLabel('Nombre:', self)
        self.name_label.setGeometry(390, 50, 100, 30)
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(450, 50, 200, 30)

        self.manager_label = QLabel('Jefe:', self)
        self.manager_label.setGeometry(50, 100, 100, 30)
        self.manager_combobox = QComboBox(self)
        self.llenar_jefes() # metodo que llena el combo box
        self.manager_combobox.setGeometry(150, 100, 200, 30)

        # Botones
        self.save_button = QPushButton('Guardar', self)
        self.save_button.setGeometry(50, 160, 100, 30)

        self.clear_button = QPushButton('Limpiar Campos', self)
        self.clear_button.setGeometry(180, 160, 120, 30)

        self.return_button = QPushButton('Regresar', self)
        self.return_button.setGeometry(310, 160, 100, 30)

        self.modify_button = QPushButton('Modificar', self)
        self.modify_button.setGeometry(420, 160, 100, 30)
        self.modify_button.setEnabled(False)

        self.delete_button = QPushButton('Eliminar', self)
        self.delete_button.setGeometry(530, 160, 100, 30)
        self.delete_button.setEnabled(False)

        # Tabla para listar departamentos
        self.department_table = QTableWidget(self)
        self.department_table.setGeometry(150, 220, 455, 200)
        self.department_table.setColumnCount(3)
        self.department_table.cellClicked.connect(self.populate_fields_from_table)
        self.department_table.setHorizontalHeaderLabels(['Código', 'Nombre', 'Jefe'])

        
        if self.collection.count_documents({}) > 0:
            self.populate_departments_table()

        # Conectar botones a funciones
        self.save_button.clicked.connect(self.save_department)
        self.clear_button.clicked.connect(self.clear_fields)
        self.return_button.clicked.connect(self.return_to_previous_window)
        
        self.modify_button.clicked.connect(self.modify_department)
        self.delete_button.clicked.connect(self.delete_department)

    def save_department(self):
        code = self.code_input.text()
        name = self.name_input.text()
        index = self.manager_combobox.currentIndex() 
        manager = self.manager_combobox.itemText(index)
        # Lógica para guardar el departamento en la base de datos o en otro almacenamiento

        # Aquí podrías realizar la lógica para guardar el empleado en una base de datos o en otro almacenamiento
        if not license or not code or not name or not manager:
            QMessageBox.warning(self, 'Advertencia', 'Debes completar toda la información')
            return
        else: 

            

            department_data = {
                'code': code,
                'name': name,
                'manager': self.collectionEmploye.find_one({"name": manager})
            }

            if not self.collection.find_one({'name': name}):
                self.collection.insert_one(department_data)
                QMessageBox.information(self, 'Información', f"¡El departamento {name} ha sido registrado correctamente !")
            else:
                QMessageBox.critical(self, 'Error', 'Ya existe un departamento con ese nombre')
                self.name_input.clear()
                return
        
        self.populate_departments_table()

        # Limpiar campos después de guardar
        self.clear_fields()


    def clear_fields(self):
        self.code_input.clear()
        self.name_input.clear()
        self.manager_combobox.setCurrentIndex(0)
        self.save_button.setEnabled(True)
        self.modify_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.name_input.setEnabled(True)
        self.departments = {}
        

    def return_to_previous_window(self):
        # Aquí puedes implementar la lógica para regresar a la ventana anterior
        self.close()

    def populate_departments_table(self):
        self.department_table.setRowCount(0) # Limpiar la tabla

        for departments in self.collection.find():
            row_position = self.department_table.rowCount()
            self.department_table.insertRow(row_position)
            self.department_table.setItem(row_position, 0, QTableWidgetItem(departments['code']))
            self.department_table.setItem(row_position, 1, QTableWidgetItem(departments['name']))
            self.department_table.setItem(row_position, 2, QTableWidgetItem(departments['manager']['name']))
            self.department_table.resizeColumnsToContents()

    def populate_fields_from_table(self, row, column):
        
        code = self.department_table.item(row, 0).text()

        self.departments = self.collection.find_one({'code': code })

        if self.departments:
            # botones a bloquear
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(True)
            self.modify_button.setEnabled(True)
            self.name_input.setEnabled(False)
            

            self.code_input.setText(self.departments['code'])
            self.name_input.setText(self.departments['name'])
            self.manager_combobox.setCurrentText(self.departments['manager']['name'])
            

    def modify_department(self):
        code = self.code_input.text()
        name = self.name_input.text()
        index = self.manager_combobox.currentIndex()
        status = self.manager_combobox.itemText(index)
        

        if not code or not name or not status:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Departamento para editar')
        else:
            
            self.collection.replace_one(
                {'name': self.departments['name']},
                {
                    'code': code,
                    'name': name,
                    'manager': status,
                }
            )

            QMessageBox.information(self, 'Información', f"¡Bien {self.departments['name']} Editado correctamente !")    
            self.clear_fields()
            self.populate_departments_table()


    def delete_department(self):
        code = self.code_input.text()
        name = self.name_input.text()
        

        if not code or not name:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un departamento para eliminar')
        else:
            departments_id = ObjectId(self.departments['_id'])
            result = self.collection.delete_one({'_id': departments_id})

            if result.deleted_count > 0:
                QMessageBox.information(self, 'Información', f"¡Departamento {self.departments['name']} eliminado correctamente !")    
                self.clear_fields()
                self.populate_departments_table()

    def llenar_jefes(self):        
        # Consultar los empleados que son jefes (isHead = "si")
        employes = self.collectionEmploye.find({"isHead": "Sí"})

        # Limpiar el QComboBox
        self.manager_combobox.clear()

        # Agregar los nombres de los jefes al QComboBox
        for employe in employes:
            nombre_completo = employe['name']
            self.manager_combobox.addItem(nombre_completo)


