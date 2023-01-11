import re
import sys

from collections import UserDict

'''
Класс AddressBook, который наследуется от UserDict, и мы потом добавим логику поиска по записям в этот класс.
Класс Record, который отвечает за логику добавления/удаления/редактирования необязательных полей и хранения обязательного поля Name.
Класс Field, который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.
Класс Name, обязательное поле с именем.
Класс Phone, необязательное поле с телефоном и таких одна запись (Record) может содержать несколько.
Критерии приёма
Реализованы все классы из задания.
- Записи Record в AddressBook хранятся как значения в словаре. В качестве ключей используется значение Record.name.value.
- Record хранит объект Name в отдельном атрибуте.
- Record хранит список объектов Phone в отдельном атрибуте.
- Record реализует методы для добавления/удаления/редактирования объектов Phone.
- AddressBook реализует метод add_record, который добавляет Record в self.data.
'''



class AddressBook(UserDict):
    def search_for_contact(self, name):
        contact = self.data.get(name.title(), "Not found")
        return f"{' '.join(contact.get_phone())}"

    def add_record(self, contact):
        self.data.update({contact.name.value: contact})
        return (
        f"Assistant: New contact {contact.name.value} with number {contact.get_phone()} has been successfully added")

    def delete_contact(self, name):
        deleted = self.date.pop(name)
        if deleted:
            return f"Contact {name} was succesfully deleted"
        else:
            return f"Contact with {name} was not found"
    def show_all(self):
        return f"{self.data}"

class Record:
    def __init__(self, name, phone = ''):
        self.name = name
        self.phone_numbers = [phone]
   
    def add_phone(self, phone):
        self.phone_numbers.append(phone)
    def edit_phone(self, phone):
        phone.value = phone
    def delete_phone(self, phone):
        idx = self.phone_numbers.index(phone)
        self.phone_numbers.pop(idx)
    def get_phone(self):
        phones_list = map(lambda x: x.value, self.phone_numbers)
        return f"{' '.join(phones_list)}"



class Field:
    pass


class Name(Field):
    def __init__ (self, value):
        self.value = value.title()

class Phone(Field):
    def __init__ (self, value):
        self.value = value




# name = Name("Dima")
# phone = Phone('+33333')

# record = Record(name, phone)

# addres_book = AddressBook()

# addres_book.add_record(record)

# print(addres_book.data["Dima"].name.value)
# print(addres_book.data["Dima"].phone_numbers[0].value)




phone_book = AddressBook()

COMMANDS = ['show all', 'good bye', 'hello',
            'exit', 'close', 'add', 'change', 'phone']

DATA_FORMATS = {
    'phone': '^[+][0-9]{12}$'
}

chat_in_progress = True


def input_error(func):
    def inner_func(args):
        try:
            result = func(args)
            return result
        except KeyError:
            print("Assistant: Please, type a name in order to find a number")
        except IndexError:
            print("Assistant: Please, type name and number")
        except ValueError as err:
            print(err.args[0])
            return None
    return inner_func


def check_number_validity(number):
    valid_number = re.match(DATA_FORMATS['phone'], number)
    if not valid_number:
        raise ValueError(
            "Assistant: Number should start with '+' and contain 12 digits. Please, try again")


def if_contact_exists(name):
    exists = None

    for person in phone_book:
        if person["name"] == name.title():
            exists = person
    return exists


@input_error
def get_instruction(message):
    message = message.replace('You: ', '').lower()
    command_not_found = True

    for command in COMMANDS:
        if message.startswith(command):
            args = message.replace(command, '').strip().split(' ')
            command_not_found = False
            return (command, args)
    if command_not_found:
        raise ValueError(
            f"Assistant: Please enter a valid command: {', '.join(COMMANDS)}")


def greet():
    return ('Assistant: Hello. How can I assist you?')


def show_all_contacts():
    for contact in phone_book:
        return (f"Assistant: Here are all your contacts:\n\t{contact['name']}: {contact['number']}")


@input_error
def add_contact(args):
    person_data = args[1]
    check_number_validity(person_data[1])
    contact = if_contact_exists(person_data[0])

    if contact:
        return ("Assistant: contact with such name alreday exists")

    new_person = {'name': person_data[0].title(), 'number': person_data[1]}
    phone_book.append(new_person)
    return (
        f"Assistant: New contact {person_data[0].title()} with number {person_data[1]} has been successfully added")


@input_error
def get_number(args):
    found_person = {}

    for person in phone_book:
        if person["name"] == args[1][0].title():
            found_person = person
            return (f"Assistant: {found_person['number']}")

    if found_person == {}:
        return ("Assistant: Person with such name was not found")


@input_error
def change_number(args):
    contact = if_contact_exists(args[1][0])

    if not contact:
        return ("Assistant: Person with such name was not found")

    check_number_validity(args[1][1])
    contact["number"] = args[1][1]
    return (
        f"Assistant: {contact['name']}'s number was successfully changed to {contact['number']}.")


def terminate_assistant():
    global chat_in_progress
    chat_in_progress = False
    return('Assistant: Bye. See you later ;)')


def main():
    message = input("You: ")
    command_args = get_instruction(message)
    bot_message = None


    if not command_args:
        return

    command, args = command_args

    match command:
        case 'hello':
            bot_message = greet()
        case "show all":
            bot_message = phone_book.show_all()
        case "phone":
            [name] = args
            bot_message = phone_book.search_for_contact(name)
        case 'add':
            [name, phone ] = args
            new_record = Record(Name(name), Phone(phone))
            bot_message = phone_book.add_record(new_record)
        case 'change':
            bot_message = change_number(command_args)

    if bot_message:
        print(bot_message)

    if command in ['close', 'exit', 'good bye']:
       bot_message = terminate_assistant()
       print(bot_message)




while chat_in_progress:
    main()