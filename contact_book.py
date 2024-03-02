import json
from contact import Contact


class ContactBook:
    def __init__(self, file_path='contacts.json'):
        self.file_path = file_path
        self.contacts = self.load_contacts()

    def load_contacts(self):
        """Loads contacts from a JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                contacts_data = json.load(file)
                # Ensure that 'phone' from JSON matches 'phone' parameter in Contact
                return [Contact(**data) for data in contacts_data]
        except FileNotFoundError:
            return []

    def save_contacts(self):
        """Saves contacts to a JSON file."""
        with open(self.file_path, 'w') as file:
            # 'phone' key is used to match the Contact's to_dict() output
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def add_contact(self, contact):
        """Adds a new contact to the contact book."""
        self.contacts.append(contact)
        self.save_contacts()

    def find_contact(self, first_name, last_name):
        """Searches for a contact by first name and last name."""
        for contact in self.contacts:
            if contact.first_name == first_name and contact.last_name == last_name:
                return contact
        return None

    def update_contact(self, first_name, last_name, new_details):
        """Updates contact details."""
        contact = self.find_contact(first_name, last_name)
        if contact:
            # Update attributes directly, including phone_number using 'phone' from new_details
            contact.first_name = new_details.get('first_name', contact.first_name)
            contact.last_name = new_details.get('last_name', contact.last_name)
            contact.phone_number = new_details.get('phone', contact.phone_number)  # Use 'phone' to match Contact class
            contact.email = new_details.get('email', contact.email)
            contact.notes = new_details.get('notes', contact.notes)
            contact.url = new_details.get('url', contact.url)
            self.save_contacts()
            return True
        return False

    def delete_contact(self, first_name, last_name):
        """Deletes a contact from the contact book."""
        contact = self.find_contact(first_name, last_name)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            return True
        return False

    def search_contacts(self, search_term):
        """Searches for contacts that match the search term in the first or last name."""
        search_term = search_term.lower()
        return [contact for contact in self.contacts if
                search_term in contact.first_name.lower() or
                search_term in contact.last_name.lower()]

    def reset_contacts(self):
        """Clears all contacts from the contact book."""
        self.contacts = []
        self.save_contacts()

