from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from models import Session, Service

class ServicesWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_data()

    def load_data(self):
        session = Session()
        services = session.query(Service).all()

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price"])
        self.table.setRowCount(len(services))

        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service.id)))
            self.table.setItem(row, 1, QTableWidgetItem(service.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(service.price)))

        self.table.resizeColumnsToContents()
        session.close()
