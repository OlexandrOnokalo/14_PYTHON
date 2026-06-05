# Simple class
class Car:
    # this позначає що цей метод належить класу Car
    def drive(this):
        print("Більше газу меньше ям")

bmw = Car()
bmw.drive()

class Animal:
    def speak(this):
        print("Голос тварини")

# Наслідування класами класу Animal
class MiniPig(Animal):
    def speak(this):
        print("Хрю-хрю")

class Dog(Animal):
    def speak(this):
        print("Гав-гав")

pig = MiniPig()
pig.speak()

dog = Dog()
dog.speak()

# Масив анонімних об'єктів
myAnimals = [MiniPig(), Dog()]
for animal in myAnimals:
    animal.speak()

def talk(obj):
    obj.speak() # Сюди передається вказівник на клас

talk(MiniPig())
talk(Dog())

# Class 

class Student:
    # Конструктор, має приймати self
    def __init__(self,name):
        self.Name = name
        self._age = 18 # це protected 
        self.__hobby = "programming" # це private
    # To String
    def __str__(self):
        return f"Student name: {self.Name}, age: {self._age}, hobby: {self.__hobby}"
    
    def get_hobby(self):
        return self.__hobby
    
    def set_hobby(self, hobby):
        self.__hobby = hobby
    

ivan = Student("Ivan")
print("name = ", ivan.Name)
print("age = ", ivan._age) # доступ до protected змінної
# print("hobby = ", ivan.__hobby) # доступу до приватної змінної немає
print("hobby = ", ivan.get_hobby()) # доступ до приватної змінної через геттер
print(ivan) # __str__ викликається автоматично при виводі об'єкта на екран

