import time

# 1
def odd_numbers_generator(start, end):
    for num in range(start, end + 1):
        if num % 2 != 0:
            yield num


for number in odd_numbers_generator(1, 10):
    print(number, end=" ")
print()

# 2
def filter_outside_range(data_list, start, end):
    for item in data_list:
        if item < start or item > end:
            yield item

my_list = [5, 12, 20, 25, 30, 8]
for val in filter_outside_range(my_list, 10, 25):
    print(val, end=" ")

# 3
def draw_horizontal(symbol):
    print(symbol * 10) # Малює лінію з 10 символів

def draw_vertical(symbol):
    for _ in range(5): # Малює вертикальну лінію з 5 символів
        print(symbol)

def show_line(symbol, function_to_call):
    function_to_call(symbol)

print("Горизонтальна лінія:")
show_line("*", draw_horizontal)

print("\nВертикальна лінія:")
show_line("#", draw_vertical)

# 4
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Час виконання: {end_time - start_time:.5f} секунд")
        return result
    return wrapper

@timer_decorator
def get_even_numbers():
    return [num for num in range(100001) if num % 2 == 0]


evens = get_even_numbers()

print("Перші та останні парні числа:", evens[:10], "...", evens[-10:])

# 5

@timer_decorator
def get_even_numbers_custom(start, end):
    return [num for num in range(start, end + 1) if num % 2 == 0]

# Приклад використання:
custom_evens = get_even_numbers_custom(50000, 150000)

print("Перші та останні парні числа:", custom_evens[:10], "...", custom_evens[-10:])