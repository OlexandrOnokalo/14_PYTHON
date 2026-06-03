print("Декоратор")
#Декоратор - це окрема функція, яка приймає іншу функцію як 
# аргумент і розширює її функціональність 
# без зміни її коду. Декоратори використовуються 
# для додавання додаткової поведінки до функцій або класів.

def my_decorator(func):
    def private_decorator():
        print("---My Decorator---")
        func()
        print("---End of My Decorator---")
    return private_decorator

@my_decorator 
def hello_message():
    print("Привіт козаки!")
#один раз привязали і тепер кожного разу коли 
# викликаємо hello_message, 
# викликається my_decorator
hello_message()

#Замикання - це функція, що має доступ до змінних з зовнішньої області видимості,
# навіть після того, як зовнішня функція завершила виконання.

def my_view_message(msg):
    message = msg[0:9] #Зрізаємо рядок
    # print("message", message)
    def private_fun():
        print(message)
    return private_fun #Повертаю вказівник на функцію

#Створюю вказівник на фукнцію, яка працює у середині
closure = my_view_message("Привіт козаки і козочки. Класна погода")
closure()

#Генератор - це спеціальний тип функції, яка повертає ітератор.
# Генератори використовуються для створення послідовностей даних,
# які можна ітерувати, не зберігаючи всі елементи в пам'яті одночасно.
# yield - це ключове слово, яке використовується в генераторах для повернення значення і збереження стану функції.

def get_numbers():
    return [1, 2, 3]

print("default numbers", get_numbers())

def get_yield_numbers():
    yield 1
    yield 2
    yield 3

print("--get_yield_numbers--")
for item in get_yield_numbers():
    print(item, end="\t")


def my_counter_yield(n):
    i = 0
    while i < n:
        yield i
        i += 2

print()
for item in my_counter_yield(7):
    print(item, end="\t")