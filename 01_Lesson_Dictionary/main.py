student = {
    "name": "Іван Марко",
    "age": 18,
    "grade": 95
}
# Значення словника
print(student)

print(student.get("name")) #Звертаємося по ключу
print(student["name"]) #Звертаємося по ключу

student["email"] = "ivan@gmail.com"
# Додали нове значення у словник
print(student)

del student["grade"]
print(student)

for key in student:
    print (f"{key}:{student[key]}")


