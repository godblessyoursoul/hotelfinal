from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models import Session, Price
from add_price_window import AddPriceWindow

class PriceWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_window)
        layout.addWidget(self.add_button)

        self.load_data()

    def load_data(self):
        session = Session()
        prices = session.query(Price).all()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Название", "Описание", "Цена"])
        self.table.setRowCount(len(prices))
        for row, p in enumerate(prices):
            self.table.setItem(row, 0, QTableWidgetItem(p.name))
            self.table.setItem(row, 1, QTableWidgetItem(p.description or ""))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.price)))
        self.table.resizeColumnsToContents()
        session.close()

    def open_add_window(self):
        self.add_window = AddPriceWindow(on_save=self.load_data)
        self.add_window.show()
