from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models import Session, Price

class AddPriceWindow(QWidget):
    def __init__(self, on_save=None):
        super().__init__()
        self.on_save = on_save
        self.setWindowTitle("Добавить номер")
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.price_input = QLineEdit()

        layout.addWidget(QLabel("Название"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Описание"))
        layout.addWidget(self.desc_input)
        layout.addWidget(QLabel("Цена"))
        layout.addWidget(self.price_input)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_data)
        layout.addWidget(save_btn)

    def save_data(self):
        session = Session()
        try:
            price = Price(
                name=self.name_input.text(),
                description=self.desc_input.text(),
                price=float(self.price_input.text())
            )
            session.add(price)
            session.commit()
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            session.close()
