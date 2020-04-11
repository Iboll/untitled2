from requests import get, post, delete

# Получение всех пользователей
print(get('http://localhost:5000/api/v2/users').json())

# Пустой запрос
print(post('http://localhost:5000/api/v2/users').json())

# Передана только почта
print(post('http://localhost:5000/api/v2/users',
           json={'email': 'mail@mail.ru'}).json())

# Передано только имя
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Sasha'}).json())

# Корректный запрос
print(post('http://localhost:5000/api/v2/users',
           json={'email': 'mail@mail.ru',
                 'name': 'John',
                 'surname': 'Ivanov',
                 'age': 23,
                 'position': 'captain',
                 'speciality': 'doctor',
                 'about': 'hello',
                 'address': None}).json())

# Данные первого пользователя
print(get('http://localhost:5000/api/v2/users/1').json())

# Пользователя с таким id нет
print(get('http://localhost:5000/api/v2/users/999').json())

# Указана строка
print(get('http://localhost:5000/api/v2/users/q').json())

# Удаление пятого пользователя
print(delete('http://localhost:5000/api/v2/users/5').json())

# Пользователя с таким id нет
print(delete('http://localhost:5000/api/v2/users/999').json())

# Указана строка
print(delete('http://localhost:5000/api/v2/users/q').json())

