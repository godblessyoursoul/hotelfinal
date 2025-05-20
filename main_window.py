from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from clients_widget import ClientsWidget
from price_widget import PriceWidget
from services_widget import ServicesWidget
from booking_widget import BookingWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отель ЦЕМЕНТ")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.get_stylesheet())

        main_layout = QHBoxLayout(self)

        # Левый сайдбар
        sidebar = QVBoxLayout()
        title = QLabel("Гостиница")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar.addWidget(title)

        # Кнопки меню
        self.buttons = []
        menu_names = ["Клиенты", "Номерной фонд", "Доп. услуги", "Бронирования"]
        for name in menu_names:
            btn = QPushButton(name)
            btn.setObjectName("menuButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons.append(btn)
            sidebar.addWidget(btn)
        sidebar.addStretch()
        main_layout.addLayout(sidebar, 1)

        # Центральная часть — таблицы
        self.content = QStackedWidget()
        self.clients_widget = ClientsWidget()
        self.content.addWidget(self.clients_widget)
        self.content.addWidget(PriceWidget())
        self.content.addWidget(ServicesWidget())
        self.content.addWidget(BookingWidget())
        main_layout.addWidget(self.content, 3)

        # Обработка переключений
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.content.setCurrentIndex(idx))

    def get_stylesheet(self):
        return """
        QWidget {
            background-color: #2e2e2e;
            color: white;
        }
        QPushButton#menuButton {
            background-color: #444;
            color: white;
            padding: 10px;
            border: none;
            text-align: left;
        }
        QPushButton#menuButton:hover {
            background-color: #0055aa;
        }
        QPushButton#menuButton:pressed {
            background-color: #003377;
        }
        QTableWidget {
            background-color: #3e3e3e;
            gridline-color: #666;
            color: white;
        }
        QHeaderView::section {
            background-color: #444;
            color: white;
        }
        """

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
