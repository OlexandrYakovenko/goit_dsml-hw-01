from collections import UserDict
import re
import datetime as dt
from datetime import date, datetime as dtdt

import pickle

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "ValueError. Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner




#@input_error
class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)
    def __repr__(self):
        return str(self._value)
    
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
       self._value = value 

#@input_error
class Birthday(Field): 
    def __init__(self, value):
        try:
            #Дата народження має бути у форматі DD.MM.YYYY
            # Додайте перевірку коректності даних
            if re.match(r'\d{2}\.\d{2}\.\d{4}',value)==None:
                raise Exception("Birthday can be in format DD.MM.YYYY!")
            # та перетворіть рядок на об'єкт datetime
            self._value = dtdt.strptime(value, '%d.%m.%Y').date() #date_str = '24-02-2024'
        except ValueError:
            raise Exception("Invalid date format. Use DD.MM.YYYY")
        except Exception as e:
            raise e
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,str_date:str):
        try:
            #Дата народження має бути у форматі DD.MM.YYYY
            # Додайте перевірку коректності даних
            if re.match(r'\d{2}\.\d{2}\.\d{4}',str_date)==None:
                raise Exception("Birthday can be in format DD.MM.YYYY!")
            # та перетворіть рядок на об'єкт datetime
            self._value = dtdt.strptime(str_date, '%d.%m.%Y').date() #date_str = '24-02-2024'
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        except Exception as e:
            raise e
            
    def validate(self):
        if type(self._value)==date:
            return True
        return False

    def __str__(self):
        return self._value.strftime('%d.%m.%Y')
    def __repr__(self):
        return self._value.strftime('%d.%m.%Y')

#@input_error
class Name(Field):
    # реалізація класу
    def __init__(self, value):
        if value=="":
            raise Exception("The field Name is mandatory!")
        super().__init__(value)

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value:str):
        if type(value)!=str:
            self._value=str(value)   
        self._value=value
        
#@input_error
class Phone(Field):
    # Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр)
    def __init__(self, value):
        if re.fullmatch(r"\d{10}",value)==None:
            raise Exception(f'The phone number must consist of 10 digits, received: \'{value}\'')
        super().__init__(value)

    def __eq__(self,value):
        if self._value==value:
            return True
        else:
            return False
 
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value:str):
        if re.fullmatch(r"\d{10}",value)==None:
            raise Exception(f'The phone number must consist of 10 digits, received: \'{value}\'') 
        self._value=value
    
    def validate(self):
        if re.fullmatch(r"\d{10}",value)==None:
            return False
        else:
            return True
            	
#@input_error
class Record:
    #Реалізовано зберігання об'єкта Name в окремому атрибуті.
    #Реалізовано зберігання списку об'єктів Phone в окремому атрибуті (phones).
    #Додайте поле birthday для дня народження в клас Record . Це поле має бути класу Birthday. 
    #   Це поле не обов'язкове, але може бути тільки одне.
    def __init__(self, name):
         if name=="":
             raise Exception("The field Name is mandatory!")
         self._name = Name(name)
         self._phones = []
         self._birthday = None

    # реалізація класу

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value:str):
        if type(value)!=str:
            self._name=str(value)   
        self._name=value
    
    @property
    def phones(self):
        return self._phones
   
    @property
    def birthday(self):
        return self._birthday
    @birthday.setter
    def birthday(self,value:Birthday):
        if type(value)==str:
            self._birthday=Birthday(value) 
        elif  type(value)==type(Birthday("01.01.1970")):
            self._birthday=value
        else:
            raise Exception("Bitrhday can be str or Birthday!")
        
            

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    def __repr__(self):
        return self._birthday#f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"



    def add_phone(self, phone:str):
        #додавання телефону
        self.phones.append(Phone(phone))
        return "Contact added."
    def remove_phone(self, phone:str):
        #видалення телефону
        self.phones.remove(Phone(phone))
        return "Contact removed."
    
    def find_phone(self, phone:str):
        # пошук об'єкта Phone
        for phone_i in self.phones:
            if phone_i.value == phone:
                return phone_i
        return None
    
    def edit_phone(self, phone:str,new_phone:str):
        #редагування номеру телефону
        #повертаємо відредагований об'єкт Phone, якщо його знайшли за значенням phone
        for phone_i in self.phones:
            if phone_i.value == phone:
                phone_i.value = new_phone
                return phone_i
        return None
    def add_birthday(self,value:str):
        #додає день народження до контакту
        self.birthday = Birthday(value)
        
    
    
            
#@input_error    
class AddressBook(UserDict):
    # реалізація класу
    def __init__(self, value=None):
        if type(value)==type(UserDict):
            self.data = value
        elif type(value)==type(dict):
            self.data = UserDict(value)
        elif type(value)==type(None):
            self.data = UserDict({})
        else:
            self.data = UserDict({})
    
    @input_error
    def add_record(self,r:Record):
        #додає запис до self.data.
        if r not in self.data:
            self.data [r.name]=r
    def __str__(self):
        #перетворює у зручний для виведення формат збережені значення
        book_string = ""
        for KeyValue in self.data.values():
            book_string+=str(KeyValue)+'\n'
        return book_string
    def find(self,name:str):
        #знаходить запис за ім'ям
        for key in self.data.keys():
            if key.value == name:
                return self.data[key]
        return None    

    @input_error
    def delete(self,name:str):
        #видаляє запис за ім'ям
        for key in self.data.keys():
            if key.value == name:
                return self.data.pop(key)
        return None
    @input_error
    def get_upcoming_birthdays(self):
        # функція отримує словник імен користувачів та їх дати народження, повертаэ словник майбутніх днів народження
        today_date=dtdt.today().date() # беремо сьогоднішню дату
        birthdays_list=[] # створюємо список для майбутніх днів народження
        for key in self.data: # перебираємо словник користувачів
            record=self.data[key] # поточний запис класу Record
            birthday_date=record.birthday # отримуємо дату народження зі списку у вигляді рядка
            if birthday_date is None:
                continue
            birthday_date=str(birthday_date)[:6] +str(today_date.year) # Замінюємо рік на поточний 
            birthday_date=dtdt.strptime(birthday_date, "%d.%m.%Y").date() # перетворюємо дату народження в об’єкт date з формату РРРР-ММ-ДД
            week_day=birthday_date.isoweekday() # Отримуємо день тижня (1-7)
            days_between=(birthday_date-today_date).days # рахуємо різницю між зараз і днем народження цьогоріч у днях
            if 0<=days_between<7: # якщо день народження протягом 7 днів від сьогодні включаючи поточний день
                if week_day<6: #  якщо пн-пт (1-5)
                    birthdays_list.append({'name':record.name, 'birthday':birthday_date.strftime("%Y.%m.%d")}) 
                    # Додаємо запис у список.
                else:
                    if (birthday_date+dt.timedelta(days=1)).weekday()==0:# якщо неділя (понеділок - 0-й день для weekday(), 1 день до понеділка - це неділя)
                        birthdays_list.append({'name':record.name, 'birthday':(birthday_date+dt.timedelta(days=1)).strftime("%Y.%m.%d")})
                        #Переносимо на понеділок. Додаємо запис у список.
                    elif (birthday_date+dt.timedelta(days=2)).weekday()==0: #якщо субота (понеділок - 0-й день для weekday(), 2 дня до понеділка - це субота)
                        birthdays_list.append({'name':record.name, 'birthday':(birthday_date+dt.timedelta(days=2)).strftime("%Y.%m.%d")})
                        #Переносимо на понеділок. Додаємо запис у список.
        return birthdays_list


@input_error 
def parse_input(user_input):
    #розбиратиме введений користувачем рядок на команду та її аргументи. Команди та аргументи мають бути розпізнані незалежно від регістру введення.
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args, book:AddressBook):
    name = args[0]
    birthday = args[1]
    record=book.find(name)
    if record==None:
        return f"No find record by name {name}"
    record.birthday=birthday
    return "Birthday added"

@input_error
def show_birthday(args, book:AddressBook):
    name = args[0]
    record=book.find(name)
    if record==None:
        return None
    return record.birthday
    

@input_error
def birthdays(args, book:AddressBook):
    di=book.get_upcoming_birthdays()
    s='Congratulations on the next week: \n'
    for key in di:
        s+=f"{key}\n"
    return s
  
 
@input_error
def add_contact(args, book:AddressBook):
    #додати контакт
    if len(args)<2 or len(args)>2:
        return "Input 2 parameters"
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def show_phone(args, book:AddressBook):
    #показати телефон
    if len(args)<1 or len(args)>1:
        return "Input 1 parameters"
    name=args[0]
    record=book.find(name)
    if record==None:
        return None
    return record.phones


@input_error
def change_contact(args, book:AddressBook):
    #змінити контакт 
    if len(args)<3 or len(args)>3:
        return "Input name, old phone, new phone parameters"
    name, old_phone, new_phone = args
    name=args[0]
    record=book.find(name)
    if record==None:
        return None
    return record.edit_phone(old_phone,new_phone)
    


@input_error
def show_all(args, book:AddressBook):
    #надрукувати всі контакти
    if len(args)!=0:
        return "Function don't take parameters"
    return str(book)

@input_error
def save_data(book:AddressBook, filename="addressbook1.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

@input_error
def load_data(filename="addressbook1.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
    
   
def main():

    # Створення/завантаження нової адресної книги
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)  # Викликати перед виходом з програми
            exit()
            
        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book)) 

        elif command == "add-birthday":
            print(add_birthday(args, book)) 

        elif command == "show-birthday":
            print(show_birthday(args, book)) 

        elif command == "birthdays":
            print(birthdays(args, book)) 

        else:
            print("Invalid command.")
            


if __name__ == "__main__":
    main()