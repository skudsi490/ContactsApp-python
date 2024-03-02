import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from contact_book import ContactBook
from add_contact_window import AddContactWindow
from update_window import UpdateWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.contact_book = ContactBook()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Contact Book')
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QVBoxLayout()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #007bff;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QListWidget {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
        """)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText('Search by First or Last Name...')
        self.main_layout.addWidget(self.search_field)

        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_contacts)
        self.main_layout.addWidget(self.search_button)

        self.show_all_button = QPushButton('Show All Contacts', self)
        self.show_all_button.clicked.connect(self.refresh_contacts_list)
        self.main_layout.addWidget(self.show_all_button)

        self.add_button = QPushButton('Add Contact', self)
        self.add_button.clicked.connect(self.open_add_contact_window)
        self.main_layout.addWidget(self.add_button)

        self.contacts_list = QListWidget(self)
        self.contacts_list.itemSelectionChanged.connect(self.toggle_edit_delete_buttons)
        self.main_layout.addWidget(self.contacts_list)

        edit_delete_layout = QHBoxLayout()
        self.edit_button = QPushButton('Edit', self)
        self.edit_button.clicked.connect(self.open_edit_window)
        self.edit_button.setEnabled(False)
        edit_delete_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.delete_contact_directly)
        self.delete_button.setEnabled(False)
        edit_delete_layout.addWidget(self.delete_button)

        self.reset_button = QPushButton('Reset Contacts', self)
        self.reset_button.clicked.connect(self.reset_contacts)
        edit_delete_layout.addWidget(self.reset_button)

        self.main_layout.addLayout(edit_delete_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.refresh_contacts_list()

    def refresh_contacts_list(self):
        self.contacts_list.clear()
        for contact in self.contact_book.contacts:
            self.contacts_list.addItem(str(contact))

    def search_contacts(self):
        search_text = self.search_field.text().strip().lower()
        if search_text:
            try:
                matching_contacts = self.contact_book.search_contacts(search_text)
                self.contacts_list.clear()
                for contact in matching_contacts:
                    self.contacts_list.addItem(str(contact))
            except Exception as e:
                QMessageBox.critical(self, "Search Error", f"An error occurred while searching: {e}")
        else:
            self.refresh_contacts_list()

    def open_add_contact_window(self):
        self.add_contact_window = AddContactWindow(self.contact_book, self.refresh_contacts_list)
        self.add_contact_window.show()

    def open_edit_window(self):
        selected_item = self.contacts_list.currentItem()
        if selected_item:
            selected_contact = selected_item.text()
            self.update_window = UpdateWindow(self.contact_book, self.refresh_contacts_list, selected_contact)
            self.update_window.setWindowModality(Qt.ApplicationModal)
            self.update_window.show()

    def delete_contact_directly(self):
        selected_item = self.contacts_list.currentItem()
        if selected_item:
            selected_contact = selected_item.text().split(' - ')[0]
            first_name, last_name = selected_contact.split(' ', 1)
            confirmation = QMessageBox.question(self, 'Confirm Deletion',
                                                f'Are you sure you want to delete {selected_contact}?',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.contact_book.delete_contact(first_name, last_name)
                self.refresh_contacts_list()

    def reset_contacts(self):
        confirmation = QMessageBox.question(self, 'Reset Contacts', 'Are you sure you want to reset all contacts?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.contact_book.reset_contacts()
            self.refresh_contacts_list()

    def refresh_contacts_list(self):
        """Refreshes the contact list and displays all contacts."""
        self.contacts_list.clear()
        for contact in self.contact_book.contacts:
            self.contacts_list.addItem(str(contact))

    def toggle_edit_delete_buttons(self):
        has_selection = bool(self.contacts_list.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
