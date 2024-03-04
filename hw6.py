import re
from collections import UserDict

class Field:
    pass

class Name(Field):
    def __init__(self, name):
        self.name = name

class Phone(Field):
    def __init__(self, number):
        if not re.match(r'^\d{10}$', number):
            raise ValueError("Invalid phone number format. Must be 10 digits.")
        self.number = number

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.name] = record
        return "Record added successfully."

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Record deleted successfully."
        else:
            return "Record not found."

    def show_all_records(self):
        for name, record in self.data.items():
            print(f"Name: {name}")
            for phone in record.phones:
                print(f"Phone: {phone.number}")
            print("------")


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)
        return "Phone added successfully."

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.number == phone_number:
                self.phones.remove(phone)
                return "Phone removed successfully."
        return "Phone not found."

    def edit_phone(self, new_phone):
        for phone in self.phones:
            phone.number = new_phone
        return "Phone edited successfully."

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.number == phone_number:
                return phone
        return None


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Check your name, it isn't in the database, try again"
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Check the correct input"
    return wrapper  

com_exit = ("exit" or "close")

@input_error
def parse_input(our_command):
    cmd, *args = our_command.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_record(args, address_book):
    name, *phones = args
    name_obj = Name(name)
    record = Record(name_obj)
    for phone in phones:
        record.add_phone(Phone(phone))
    address_book.add_record(record)
    return "Record added"

@input_error
def find_record(args, address_book):
    record = address_book.find(args[0])
    if record:
        return f"Record found: {record.name.name} - {', '.join([phone.number for phone in record.phones])}"
    else:
        return "Record not found"

@input_error
def delete_record(args, address_book):
    address_book.delete(args[0])
    return "Record deleted"

@input_error
def edit_phone_number(args, address_book):
    if len(args) != 2:
        return "Невірна кількість аргументів для редагування номера телефону."

    name, new_phone = args
    record = address_book.find(name)
    if record:
        result = record.edit_phone(new_phone)
        return result
    else:
        return "Запис не знайдено."

@input_error
def show_all_records(address_book):
    address_book.show_all_records()


    
@input_error
def main():
    address_book = AddressBook()
    print("Hello, it's your personal Helper")
    while True:                
        our_command = input("Enter a command: ").strip().lower()
        command, *args = parse_input(our_command)
        if command == com_exit:
            print("Bye")
            break
        elif command == "hello":
            print("How can I help you: ")
        elif command == "add":
            print(add_record(args, address_book))
        elif command == "find":
            print(find_record(args, address_book))
        elif command == "delete":
            print(delete_record(args, address_book))
        elif command == "all":
            print(show_all_records(address_book))
        elif command == "edit":
            print(edit_phone_number(args, address_book))

if __name__ == "__main__":
    main()