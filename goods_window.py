
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from bson import ObjectId
import pymongo

class GoodsManagementWindow(QWidget):
    def __init__(self):
        super().__init__()

        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['goods']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)




        self.setWindowTitle('Gestión de Bienes')
        self.setGeometry(100, 100, 800, 500)
        self.goods = {}

        # Campos de entrada
        # Campo de placa con validador de expresión regular
        # Campo de placa con validadores estáticos
        self.plate_label = QLabel('Placa (AZ-1234):', self)
        self.plate_label.setGeometry(50, 50, 150, 30)
        self.plate_input = QLineEdit(self)
        self.plate_input.setGeometry(200, 50, 150, 30)

        # Validador para las dos letras
        left_validator = QRegExpValidator(QRegExp("[A-Z]{2}"), self.plate_input)
        self.plate_input.setValidator(left_validator)

        # Validador para los cuatro números
        right_validator = QIntValidator(0, 9999, self.plate_input)
        self.plate_input.setMaxLength(7)  # Establecer la longitud máxima de la entrada
        self.plate_input.setInputMask("AA-9999")  # Establecer una máscara de entrada para mostrar el formato

        self.name_label = QLabel('Nombre:', self)
        self.name_label.setGeometry(400, 50, 100, 30)
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(500, 50, 150, 30)

        self.category_label = QLabel('Categoría:', self)
        self.category_label.setGeometry(50, 100, 100, 30)
        self.category_input = QLineEdit(self)
        self.category_input.setGeometry(200, 100, 150, 30)

        self.description_label = QLabel('Descripción:', self)
        self.description_label.setGeometry(400, 100, 100, 30)
        self.description_input = QLineEdit(self)
        self.description_input.setGeometry(500, 100, 150, 30)

        self.status_label = QLabel('Estado:', self)
        self.status_label.setGeometry(50, 150, 100, 30)
        self.status_combobox = QComboBox(self)
        self.status_combobox.addItem('Asignable')
        self.status_combobox.addItem('Exclusión')
        self.status_combobox.addItem('Reparación')
        self.status_combobox.setGeometry(200, 150, 150, 30)

        # Botones
        self.create_button = QPushButton('Crear', self)
        self.create_button.setGeometry(50, 230, 80, 30)
        
        self.modify_button = QPushButton('Modificar', self)
        self.modify_button.setGeometry(250, 230, 80, 30)
        self.modify_button.setEnabled(False)

        self.delete_button = QPushButton('Eliminar', self)
        self.delete_button.setGeometry(350, 230, 80, 30)
        self.delete_button.setEnabled(False)

        self.return_button = QPushButton('Regresar', self)
        self.return_button.setGeometry(450, 230, 80, 30)

        self.clear_button = QPushButton('Limpiar cajas', self)
        self.clear_button.clicked.connect(self.clear_fields)
        self.clear_button.setGeometry(550, 230, 80, 30)

        # Tabla para listar bienes
        self.goods_table = QTableWidget(self)
        self.goods_table.move(50, 290)
        self.goods_table.setColumnCount(5)
        self.goods_table.cellClicked.connect(self.populate_fields_from_table)
        self.goods_table.setHorizontalHeaderLabels(['Placa', 'Nombre', 'Categoría', 'Descripción', 'Estado'])

        if self.collection.count_documents({}) > 0:
            self.populate_goods_table()

        # Conectar botones a funciones
        self.create_button.clicked.connect(self.create_good)
        
        self.modify_button.clicked.connect(self.modify_good)
        self.delete_button.clicked.connect(self.delete_good)
        self.return_button.clicked.connect(self.return_to_previous_window)

    def create_good(self):
        license = self.plate_input.text()
        name = self.name_input.text()
        category = self.category_input.text()
        index = self.status_combobox.currentIndex()
        status = self.status_combobox.itemText(index)
        description = self.description_input.text()
        # Lógica para crear el bien en la base de datos o en otro almacenamiento


        # Aquí podrías realizar la lógica para guardar el empleado en una base de datos o en otro almacenamiento
        if not license or not name or not category or not status or not description:
            QMessageBox.warning(self, 'Advertencia', 'Debes completar toda la información')
            return
        else: 
            good_data = {
                'license': license,
                'name': name,
                'category': category,
                'status': status,
                'desc': description
            }

            if not self.collection.find_one({'license': license}):
                self.collection.insert_one(good_data)
                QMessageBox.information(self, 'Información', f"¡El bien {name} ha sido registrado correctamente !")
            else:
                QMessageBox.critical(self, 'Error', 'Ya existe un bien con esa license')
                self.plate_input.clear()
                return
        
        self.populate_goods_table()

        # Limpiar campos después de guardar
        self.clear_fields()

    def modify_good(self):
        license = self.plate_input.text()
        name = self.name_input.text()
        category = self.category_input.text()
        index = self.status_combobox.currentIndex()
        status = self.status_combobox.itemText(index)
        description = self.description_input.text()

        if not license or not name or not category or not status or not description:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Bien para editar')
        else:
            
            self.collection.replace_one(
                {'license': self.goods['license']},
                {
                    'license': license,
                    'name': name,
                    'category': category,
                    'status': status,
                    'desc': description
                }
            )

            QMessageBox.information(self, 'Información', f"¡Bien {self.goods['name']} Editado correctamente !")    
            self.clear_fields()
            self.populate_goods_table()


    def delete_good(self):
        license = self.plate_input.text()
        name = self.name_input.text()
        

        if not license or not name:
            QMessageBox.warning(self, 'Advertencia', 'Selecciona un Bien para eliminar')
        else:
            good_id = ObjectId(self.goods['_id'])
            result = self.collection.delete_one({'_id': good_id})

            if result.deleted_count > 0:
                QMessageBox.information(self, 'Información', f"¡Bien {self.goods['name']} eliminado correctamente !")    
                self.clear_fields()
                self.populate_goods_table()
            

    def populate_goods_table(self):
        self.goods_table.setRowCount(0) # Limpiar la tabla

        for good in self.collection.find():
            row_position = self.goods_table.rowCount()
            self.goods_table.insertRow(row_position)
            self.goods_table.setItem(row_position, 0, QTableWidgetItem(good['license']))
            self.goods_table.setItem(row_position, 1, QTableWidgetItem(good['name']))
            self.goods_table.setItem(row_position, 2, QTableWidgetItem(good['category']))
            self.goods_table.setItem(row_position, 3, QTableWidgetItem(good['status']))
            self.goods_table.setItem(row_position, 4, QTableWidgetItem(good['desc']))
            self.goods_table.resizeColumnsToContents()

    def populate_fields_from_table(self, row, column):
        
        license = self.goods_table.item(row, 0).text()

        self.goods = self.collection.find_one({'license': license })

        if self.goods:
            # botones a bloquear
            self.create_button.setEnabled(False)
            self.delete_button.setEnabled(True)
            self.modify_button.setEnabled(True)
            self.plate_input.setEnabled(False)

            self.plate_input.setText(self.goods['license'])
            self.name_input.setText(self.goods['name'])
            self.category_input.setText(self.goods['category'])
            self.status_combobox.setCurrentText(self.goods['status'])
            self.description_input.setText(self.goods['desc'])
            


    def clear_fields(self):
        self.plate_input.clear()
        self.name_input.clear()
        self.category_input.clear()
        self.description_input.clear()
        self.status_combobox.setCurrentIndex(0)
        self.create_button.setEnabled(True)
        self.plate_input.setEnabled(True)
        self.delete_button.setEnabled(False)
        self.modify_button.setEnabled(False)
        self.goods = {}

    def return_to_previous_window(self):
        # Aquí puedes implementar la lógica para regresar a la ventana anterior
        self.close()


