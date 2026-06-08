# 1
class Car:
    def __init__(self, model="", year=0, manufacturer="", engine_volume=0.0, color="", price=0.0):
        self.model = model
        self.year = year
        self.manufacturer = manufacturer
        self.engine_volume = engine_volume
        self.color = color
        self.price = price

    def display_info(self):
        print(f"--- Автомобіль {self.manufacturer} {self.model} ---")
        print(f"Рік випуску: {self.year}")
        print(f"Об'єм двигуна: {self.engine_volume} л")
        print(f"Колір: {self.color}")
        print(f"Ціна: ${self.price}")
        print("-" * 30)

    def input_info(self):
        print("Введіть дані автомобіля:")
        self.model = input("Модель: ")
        self.manufacturer = input("Виробник: ")
        self.year = int(input("Рік випуску: "))
        self.engine_volume = float(input("Об'єм двигуна (л): "))
        self.color = input("Колір: ")
        self.price = float(input("Ціна: "))


my_car = Car("Camry", 2021, "Toyota", 2.5, "Чорний", 25000)
my_car.display_info()

#2
class Book:
    def __init__(self, title="", year=0, publisher="", genre="", author="", price=0.0):
        self.title = title
        self.year = year
        self.publisher = publisher
        self.genre = genre
        self.author = author
        self.price = price

    def display_info(self):
        print(f"--- Книга: «{self.title}» ---")
        print(f"Автор: {self.author}")
        print(f"Жанр: {self.genre}")
        print(f"Видавництво: {self.publisher}")
        print(f"Рік видання: {self.year}")
        print(f"Ціна: {self.price} грн")
        print("-" * 30)

    def input_info(self):
        print("Введіть дані книги:")
        self.title = input("Назва: ")
        self.author = input("Автор: ")
        self.genre = input("Жанр: ")
        self.publisher = input("Видавництво: ")
        self.year = int(input("Рік видання: "))
        self.price = float(input("Ціна: "))


my_book = Book("1984", 1949, "Secker & Warburg", "Антиутопія", "Джордж Орвелл", 350.50)
my_book.display_info()

#3
class Stadium:
    def __init__(self, name="", opening_date="", country="", city="", capacity=0):
        self.name = name
        self.opening_date = opening_date
        self.country = country
        self.city = city
        self.capacity = capacity

    def display_info(self):
        print(f"--- Стадіон: {self.name} ---")
        print(f"Локація: {self.city}, {self.country}")
        print(f"Дата відкриття: {self.opening_date}")
        print(f"Місткість: {self.capacity} глядачів")
        print("-" * 30)

    def input_info(self):
        print("Введіть дані стадіону:")
        self.name = input("Назва стадіону: ")
        self.country = input("Країна: ")
        self.city = input("Місто: ")
        self.opening_date = input("Дата відкриття (напр., 01.09.2000): ")
        self.capacity = int(input("Місткість: "))

# Приклад використання:
dinamo = Stadium("Динамо", "01.08.1955", "Україна", "Київ", 90000)
dinamo.display_info()