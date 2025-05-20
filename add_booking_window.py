from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from models import Session, Booking, Client
from datetime import datetime

class AddBookingWindow(QWidget):
    def __init__(self, on_save=None):
        super().__init__()
        self.on_save = on_save
        self.setWindowTitle("Добавить бронирование")
        layout = QVBoxLayout(self)

        self.client_input = QComboBox()
        self.room_input = QLineEdit()
        self.date_input = QLineEdit()

        layout.addWidget(QLabel("Клиент"))
        layout.addWidget(self.client_input)
        layout.addWidget(QLabel("Категория номера"))
        layout.addWidget(self.room_input)
        layout.addWidget(QLabel("Дата выезда (ГГГГ-ММ-ДД)"))
        layout.addWidget(self.date_input)

        self.load_clients()

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_data)
        layout.addWidget(save_btn)

    def load_clients(self):
        session = Session()
        self.clients = session.query(Client).all()
        for client in self.clients:
            display = f"{client.id}: {client.last_name} {client.first_name}"
            self.client_input.addItem(display, client.id)
        session.close()

    def save_data(self):
        session = Session()
        try:
            booking = Booking(
                client_id=self.client_input.currentData(),
                room_category=self.room_input.text(),
                departure_date=datetime.strptime(self.date_input.text(), "%Y-%m-%d").date()
            )
            session.add(booking)
            session.commit()
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            session.close()
