#ЛЯмбда вирази - це анонімні функції, які можна використовувати 
# для створення коротких функцій без необхідності визначати 
# їх за допомогою def. Вони часто використовуються 
# в поєднанні з функціями вищого порядку, такими як map(), filter() та sorted().

mysquare = lambda x: x*x # буде підносити до квадрату
print(mysquare(5))

#оголошення звуичайної функції
def square(num):
    return num*num

print(square(5))

students = [
    {"name": "Іван Марко", "age": 35},
    {"name": "Олена Петрова", "age": 20},
    {"name": "Сергій Коваль", "age": 30}
]

#Мутація для сортування - змінюємо сам масив
# students.sort(key=lambda x: x["age"])
# print(students)

sorted_stud = sorted(students, key=lambda student:student["age"]) #створює новий масив
print(sorted_stud)

print(type(students[0])) #виводить тип даних першого елемента масиву

