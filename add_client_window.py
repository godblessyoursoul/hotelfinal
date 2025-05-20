from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import QDate
from models import Session, Client, Passport, Street
from datetime import date

class AddClientWindow(QWidget):
    def __init__(self, on_save=None):
        super().__init__()
        self.on_save = on_save
        self.setWindowTitle("Добавление клиента")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Поля ввода
        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())

        self.phone_input = QLineEdit()
        self.arrival_input = QDateEdit()
        self.arrival_input.setCalendarPopup(True)
        self.arrival_input.setDate(QDate.currentDate())

        self.departure_input = QDateEdit()
        self.departure_input.setCalendarPopup(True)
        self.departure_input.setDate(QDate.currentDate())

        self.passport_combo = QComboBox()
        self.address_combo = QComboBox()

        self.load_passports()
        self.load_addresses()

        # Разметка
        layout.addLayout(self.make_row("Фамилия", self.last_name_input))
        layout.addLayout(self.make_row("Имя", self.first_name_input))
        layout.addLayout(self.make_row("Отчество", self.middle_name_input))
        layout.addLayout(self.make_row("Дата рождения", self.birth_date_input))
        layout.addLayout(self.make_row("Телефон", self.phone_input))
        layout.addLayout(self.make_row("Дата прибытия", self.arrival_input))
        layout.addLayout(self.make_row("Дата выезда", self.departure_input))
        layout.addLayout(self.make_row("Паспорт", self.passport_combo))
        layout.addLayout(self.make_row("Адрес", self.address_combo))

        # Кнопка
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_client)
        layout.addWidget(save_button)

    def make_row(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(100)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def load_passports(self):
        session = Session()
        self.passport_combo.clear()
        self.passport_map = {}
        for passport in session.query(Passport).all():
            display = f"{passport.series} {passport.number}"
            self.passport_combo.addItem(display)
            self.passport_map[display] = passport.id
        session.close()

    def load_addresses(self):
        session = Session()
        self.address_combo.clear()
        self.address_map = {}
        for street in session.query(Street).all():
            if street.city:
                display = f"{street.city.name}, {street.name}, {street.house_number}"
            else:
                display = f"{street.name}, {street.house_number}"
            self.address_combo.addItem(display)
            self.address_map[display] = street.id
        session.close()

    def save_client(self):
        session = Session()
        try:
            client = Client(
                last_name=self.last_name_input.text(),
                first_name=self.first_name_input.text(),
                middle_name=self.middle_name_input.text(),
                birth_date=self.birth_date_input.date().toPyDate(),
                phone_number=self.phone_input.text(),
                arrival_date=self.arrival_input.date().toPyDate(),
                departure_date=self.departure_input.date().toPyDate(),
                passport_id=self.passport_map[self.passport_combo.currentText()],
                address_id=self.address_map[self.address_combo.currentText()]
            )
            session.add(client)
            session.commit()
            QMessageBox.information(self, "Успех", "Клиент добавлен.")
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            session.close()
