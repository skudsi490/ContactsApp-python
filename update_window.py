from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class UpdateWindow(QWidget):
    def __init__(self, contact_book, refresh_callback, selected_contact_str):
        super().__init__()
        self.contact_book = contact_book
        self.refresh_callback = refresh_callback
        self.selected_contact_str = selected_contact_str
        self.contact = self.find_contact()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Update Contact')
        self.setGeometry(100, 100, 400, 300)
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
        """)

        layout = QVBoxLayout()

        # First Name
        layout.addWidget(QLabel('First Name'))
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setText(self.contact.first_name if self.contact else '')
        layout.addWidget(self.first_name_input)

        # Last Name
        layout.addWidget(QLabel('Last Name'))
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setText(self.contact.last_name if self.contact else '')
        layout.addWidget(self.last_name_input)

        # Phone Number
        layout.addWidget(QLabel('Phone Number'))
        self.phone_number_input = QLineEdit(self)
        self.phone_number_input.setText(self.contact.phone_number if self.contact else '')
        layout.addWidget(self.phone_number_input)

        # Email
        layout.addWidget(QLabel('Email'))
        self.email_input = QLineEdit(self)
        self.email_input.setText(self.contact.email if self.contact else '')
        layout.addWidget(self.email_input)

        # Notes
        layout.addWidget(QLabel('Notes'))
        self.notes_input = QLineEdit(self)
        self.notes_input.setText(self.contact.notes if self.contact else '')
        layout.addWidget(self.notes_input)

        # Save Button
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_contact)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def find_contact(self):
        first_name, last_name = self.selected_contact_str.split(' - ')[0].split(' ', 1)
        return self.contact_book.find_contact(first_name, last_name)

    def save_contact(self):
        new_first_name = self.first_name_input.text().strip()
        new_last_name = self.last_name_input.text().strip()
        new_phone_number = self.phone_number_input.text().strip()
        new_email = self.email_input.text().strip()
        new_notes = self.notes_input.text().strip()

        if not new_first_name or not new_last_name or not new_phone_number:
            QMessageBox.warning(self, 'Error', 'First Name, Last Name, and Telephone are required.')
            return

        updated_details = {
            'first_name': new_first_name,
            'last_name': new_last_name,
            'phone': new_phone_number,  # Ensure this matches the key used in your Contact class
            'email': new_email,
            'notes': new_notes
        }

        success = self.contact_book.update_contact(self.contact.first_name, self.contact.last_name, updated_details)

        if success:
            self.refresh_callback()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'There was a problem updating the contact.')
