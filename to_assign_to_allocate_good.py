
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QListWidget, QPushButton, QMessageBox
import pymongo

class ToAssignToAllocateGoodWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Asignación y Desligado de Bienes')


        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['goods']
            self.collectionEmploye = self.db['employe']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)

        
        self.setGeometry(100, 100, 400, 300)
        
        # Etiqueta y menú desplegable para seleccionar empleado
        self.lbl_empleado = QLabel('Seleccionar empleado:', self)
        self.lbl_empleado.setGeometry(20, 20, 170, 20)
        self.cmb_empleado = QComboBox(self)
        self.cmb_empleado.setGeometry(20, 40, 150, 20)
        self.cmb_empleado.addItems(['Empleado 1', 'Empleado 2', 'Empleado 3'])  # Ejemplo, puedes cargar los empleados desde la base de datos

        # Etiqueta para seleccionar bien
        self.lbl_bien = QLabel('Seleccionar bien:', self)
        self.lbl_bien.setGeometry(40, 20, 150, 20)
        self.cmb_bien = QComboBox(self)
        self.cmb_bien.setGeometry(60, 20, 150, 20)
        self.cmb_bien.addItems(['Bien 1', 'Bien 2', 'Bien 3'])  # Ejemplo, puedes cargar los bienes desde la base de datos
        
        
        # Botón para asignar bien
        self.btn_asignar = QPushButton('Asignar Bien', self)
        self.btn_asignar.setGeometry(200, 40, 100, 20)
        self.btn_asignar.clicked.connect(self.asignar_bien)
        
        # Etiqueta para visualizar bienes asignados
        self.lbl_bienes_asignados = QLabel('Bienes asignados:', self)
        self.lbl_bienes_asignados.setGeometry(20, 80, 150, 20)
        
        # Lista para mostrar bienes asignados
        self.lst_bienes_asignados = QListWidget(self)
        for i in range(1, 8):
            self.lst_bienes_asignados.addItem(f'bien {i}')
        self.lst_bienes_asignados.setGeometry(20, 100, 300, 150)

        self.btn_desligar_only_good = QPushButton('Desligar Bien', self)
        self.btn_desligar_only_good.setGeometry(40, 260, 150, 30)

        # Botón para desligar bienes
        self.btn_desligar = QPushButton('Desligar Bien(es)', self)
        self.btn_desligar.setGeometry(20, 260, 150, 30)
        self.btn_desligar.clicked.connect(self.desligar_bienes)
        
        
    
    def asignar_bien(self):
        empleado_seleccionado = self.cmb_empleado.currentText()
        # Aquí puedes implementar la lógica para asignar el bien seleccionado al empleado seleccionado
        QMessageBox.information(self, 'Asignación de bien', f"Se asignó un bien a '{empleado_seleccionado}'")
    
    def desligar_bienes(self):
        empleado_seleccionado = self.cmb_empleado.currentText()
        bienes_seleccionados = [item.text() for item in self.lst_bienes_asignados.selectedItems()]
        # Aquí puedes implementar la lógica para desligar los bienes seleccionados del empleado seleccionado
        QMessageBox.information(self, 'Desligado de bienes', f"Se desligaron los bienes seleccionados de '{empleado_seleccionado}'")