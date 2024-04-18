from PyQt5.QtWidgets import QWidget, QPushButton
from user_window import UserManagementWindow
from employe_window import EmployeeManagementWindow
from departments_window import DepartmentManagementWindow
from goods_window import GoodsManagementWindow
from to_assign_to_allocate_good import ToAssignToAllocateGoodWindow



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menú Principal')

        # Botones del menú principal
        self.button_users = QPushButton('Usuarios', self)
        self.button_users.setGeometry(50, 50, 200, 40)
        self.button_users.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')
        self.button_users.clicked.connect(self.openUserManagementWindowScreen)

        self.button_employees = QPushButton('Empleados', self)
        self.button_employees.setGeometry(50, 100, 200, 40)
        self.button_employees.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')
        self.button_employees.clicked.connect(self.openEmploye_windowScreen)

        self.button_departments = QPushButton('Departamentos', self)
        self.button_departments.setGeometry(50, 150, 200, 40)
        self.button_departments.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')
        self.button_departments.clicked.connect(self.openDepartmentManagementWindowScreen)

        self.button_assets = QPushButton('Bienes', self)
        self.button_assets.setGeometry(300, 50, 200, 40)
        self.button_assets.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')
        self.button_assets.clicked.connect(self.openGoodsManagementWindowScreen)

        self.button_assign_assets = QPushButton('Asignar/Quitar Bienes', self)
        self.button_assign_assets.setGeometry(300, 100, 200, 40)
        self.button_assign_assets.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')
        self.button_assign_assets.clicked.connect(self.openToAssignToAllocateGoodWindowScreen)

        self.button_reports = QPushButton('Reportes', self)
        self.button_reports.setGeometry(300, 150, 200, 40)
        self.button_reports.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')

        self.button_storage = QPushButton('Almacenamientos', self)
        self.button_storage.setGeometry(550, 50, 200, 40)
        self.button_storage.setStyleSheet('background-color: #1E3A5F; color: white; font-size: 16px')

        


        # Tamaño de la ventana
        self.setGeometry(100, 100, 800, 250)

    def openUserManagementWindowScreen(self):
        self.user_window = UserManagementWindow()  # Crear una instancia de la ventana principal
        self.user_window.show()
        
    def openEmploye_windowScreen(self):
        self.employe_window = EmployeeManagementWindow()  # Crear una instancia de la ventana principal
        self.employe_window.show()  # Mostrar la ventana principal

    def openDepartmentManagementWindowScreen(self):
        self.departments_window = DepartmentManagementWindow()  # Crear una instancia de la ventana principal
        self.departments_window.show()  # Mostrar la ventana principal

    def openGoodsManagementWindowScreen(self):
        self.goods_window = GoodsManagementWindow()  # Crear una instancia de la ventana principal
        self.goods_window.show()

    def openToAssignToAllocateGoodWindowScreen(self):
        self.to_assign_to_allocate_good = ToAssignToAllocateGoodWindow()  # Crear una instancia de la ventana principal
        self.to_assign_to_allocate_good.show()  

    
