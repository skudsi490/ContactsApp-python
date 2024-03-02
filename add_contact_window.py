from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from contact import Contact


class AddContactWindow(QWidget):
    def __init__(self, contact_book, refresh_callback):
        super().__init__()
        self.contact_book = contact_book
        self.refresh_callback = refresh_callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Contact')
        self.setGeometry(100, 100, 400, 300)  # Set size and position
        self.setWindowModality(Qt.ApplicationModal)  # Make window modal

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #007bff;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin-bottom: 5px;
            }
        """)

        layout = QVBoxLayout()

        layout.addWidget(QLabel('First Name'))
        self.first_name_input = QLineEdit(self)
        layout.addWidget(self.first_name_input)

        layout.addWidget(QLabel('Last Name'))
        self.last_name_input = QLineEdit(self)
        layout.addWidget(self.last_name_input)

        layout.addWidget(QLabel('Phone Number'))
        self.phone_number_input = QLineEdit(self)
        layout.addWidget(self.phone_number_input)

        layout.addWidget(QLabel('Email'))
        self.email_input = QLineEdit(self)
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel('Notes'))
        self.notes_input = QLineEdit(self)
        layout.addWidget(self.notes_input)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_contact)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_contact(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        phone_number = self.phone_number_input.text().strip()
        email = self.email_input.text().strip()
        notes = self.notes_input.text().strip()

        if not first_name or not last_name or not phone_number:
            QMessageBox.warning(self, 'Error', 'First Name, Last Name, and Phone Number are required.')
            return

        contact = Contact(first_name, last_name, phone_number, email, notes)
        self.contact_book.add_contact(contact)
        self.refresh_callback()
        self.close()
