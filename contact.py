class Contact:
    def __init__(self, first_name, last_name, phone, email='', notes='', url=''):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone
        self.email = email
        self.notes = notes
        self.url = url

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone_number,
            'email': self.email,
            'notes': self.notes,
            'url': self.url

        }

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
