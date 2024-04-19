
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QListWidget, QPushButton, QMessageBox
import pymongo

class ToAssignToAllocateGoodWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Asignación y Desligado de Bienes')
        self.documentsEmpleadosAsignados = []


        try: 
            self.client = pymongo.MongoClient('localhost', 27017)
            self.db = self.client['dbgoods']
            self.collection = self.db['goods']
            self.collectionEmploye = self.db['employe']

            print("Conexión exitosa a mongo")
        except Exception as e:
            print("Error a la conexión a mongo", e)

        
        self.setGeometry(100, 100, 700, 400)
        self.empleado_a_desligar = {}
        
        # Etiqueta y menú desplegable para seleccionar empleado
        self.lbl_empleado = QLabel('Seleccionar empleado:', self)
        self.lbl_empleado.setGeometry(20, 20, 170, 20)
        self.cmb_empleado = QComboBox(self)
        self.cmb_empleado.setGeometry(20, 40, 150, 20)
        self.llenar_empleados()

        # Etiqueta para seleccionar bien
        self.lbl_bien = QLabel('Seleccionar bien:', self)
        self.lbl_bien.setGeometry(200, 20, 150, 20)
        self.cmb_bien = QComboBox(self)
        self.cmb_bien.setGeometry(200, 40, 150, 20)
        self.llenar_bienes()  # Ejemplo, puedes cargar los bienes desde la base de datos
        
        
        # Botón para asignar bien
        self.btn_asignar = QPushButton('Asignar Bien', self)
        self.btn_asignar.setGeometry(400, 35, 110, 30)
        self.btn_asignar.clicked.connect(self.asignar_bien)
         
        # Etiqueta para visualizar bienes asignados
        self.lbl_bienes_asignados = QLabel('Bienes asignados:', self)
        self.lbl_bienes_asignados.setGeometry(20, 130, 150, 20)
        # Lista para mostrar bienes asignados
        self.lst_bienes_asignados = QListWidget(self)
        
        self.lst_bienes_asignados.setGeometry(20, 160, 300, 150)

        # Etiqueta y menú desplegable para seleccionar empleado
        self.lbl_empleado = QLabel('Seleccionar empleado:', self)
        self.lbl_empleado.setGeometry(400, 130, 170, 20)
        self.cmb_empleado_desligar = QComboBox(self)
        self.cmb_empleado_desligar.setGeometry(400, 160, 150, 20)
        self.cmb_empleado_desligar.currentIndexChanged.connect(self.llenar_bienes_asignados)

        
        self.llenar_empleados_asignados()
        


        self.btn_return = QPushButton('Regresar', self)
        self.btn_return.setGeometry(200, 360, 150, 30)
        self.btn_return.clicked.connect(self.regresar)

        # Botón para desligar bienes
        self.btn_desligar = QPushButton('Desligar Bien(es)', self)
        self.btn_desligar.setGeometry(20, 360, 150, 30)
        self.btn_desligar.clicked.connect(self.desligar_bienes)
        
        
    
    def asignar_bien(self):
        indexEmploye = self.cmb_empleado.currentIndex()
        indexGood = self.cmb_bien.currentIndex()

        employe = self.cmb_empleado.itemText(indexEmploye)
        good = self.cmb_bien.itemText(indexGood)

        if not employe or not good:
            QMessageBox.warning(self, 'Advertencia', 'Debes seleccionar un empleado o un bien.')
            return
        else:

            goodFound = self.collection.find_one({"name": good})
            employeFound = self.collectionEmploye.find_one({"name": employe})

            employeFound['goods'].append(goodFound)

            self.collection.replace_one(
                {'license': goodFound['license']},
                {
                   'license': goodFound['license'],
                    'name': goodFound['name'],
                    'category': goodFound['category'],
                    'status': goodFound['status'],
                    'desc': goodFound['desc'],
                    'assigned': True,
                    'employe': employeFound 
                }    
            )

            self.collectionEmploye.replace_one(
                {'identification': employeFound['identification']},
                employeFound    
            )

            QMessageBox.information(self, 'Información', "Asignación satisfactoria")    
            self.clear_fields()
            self.llenar_bienes()
            self.llenar_empleados_asignados()
            self.llenar_bienes_asignados(0)

    def llenar_bienes_asignados(self, i):
        selected_value = self.cmb_empleado_desligar.itemText(i)
        asignado = {}
        self.lst_bienes_asignados.clear()

        
        for employe in self.documentsEmpleadosAsignados:
            if employe['name'] == selected_value:
                asignado = employe

        if asignado == {}:
            for employe in self.documentsEmpleadosAsignados:
                if employe['name'] == self.documentsEmpleadosAsignados[0]['name']:
                    asignado = employe

        self.empleado_a_desligar = asignado
        
        for good in asignado['goods']:
            self.lst_bienes_asignados.addItem(good['name'])       

        

    def clear_fields(self):
        self.cmb_empleado.setCurrentIndex(0)    
        self.cmb_bien.setCurrentIndex(0)
        self.cmb_empleado_desligar.setCurrentIndex(1)
        
    
    def desligar_bienes(self):
        empleado = self.empleado_a_desligar

        for good in empleado['goods']:
            self.collection.replace_one(
                {'license': good['license']},
                {
                   'license': good['license'],
                    'name': good['name'],
                    'category': good['category'],
                    'status': good['status'],
                    'desc': good['desc'],
                    'assigned': False,
                    'employe': None 
                }    
            )


        empleado['goods'] = []

        self.collectionEmploye.replace_one(
            {'identification': empleado['identification']},
            empleado    
        )

        self.llenar_bienes_asignados(0)
        self.llenar_bienes()

    def llenar_empleados(self):        
        # Consultar los empleados 
        employes = self.collectionEmploye.find()

        # Limpiar el QComboBox
        self.cmb_empleado.clear()

        # Agregar los nombres de los jefes al QComboBox
        for employe in employes:
            nombre_completo = employe['name']
            self.cmb_empleado.addItem(nombre_completo)

    
    def llenar_empleados_asignados(self):        
    
        cursor = self.collectionEmploye.find()
        documents = [] 

        for document in cursor:
            documents.append(document)
            
        # Limpiar el QComboBox
        self.cmb_empleado_desligar.clear()
        self.lst_bienes_asignados.clear()

        
        # Agregar los nombres de los jefes al QComboBox
        for employe in documents:

            if len(employe['goods'])>0:
                self.documentsEmpleadosAsignados.append(employe)

                nombre_completo = employe['name']
                self.cmb_empleado_desligar.addItem(nombre_completo)

            
                   

    def llenar_bienes(self):        
        # Consultar los empleados 
        goods = self.collection.find({"status": "Asignable", "assigned": False})

        # Limpiar el QComboBox
        self.cmb_bien.clear()

        # Agregar los nombres de los jefes al QComboBox
        for good in goods:
            nombre_completo = good['name']
            self.cmb_bien.addItem(nombre_completo)

    def regresar(self):
        # Aquí puedes implementar la lógica para regresar a la ventana anterior
        self.close()