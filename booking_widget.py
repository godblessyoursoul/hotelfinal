from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models import Session, Booking
from add_booking_window import AddBookingWindow

class BookingWidget(QWidget):
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
        bookings = session.query(Booking).all()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Клиент", "Категория номера", "Дата выезда"])
        self.table.setRowCount(len(bookings))
        for row, b in enumerate(bookings):
            client = f"{b.client.last_name} {b.client.first_name}" if b.client else ""
            self.table.setItem(row, 0, QTableWidgetItem(client))
            self.table.setItem(row, 1, QTableWidgetItem(b.room_category))
            self.table.setItem(row, 2, QTableWidgetItem(str(b.departure_date)))
        self.table.resizeColumnsToContents()
        session.close()

    def open_add_window(self):
        self.add_window = AddBookingWindow(on_save=self.load_data)
        self.add_window.show()
