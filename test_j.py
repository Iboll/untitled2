from requests import get, post, delete

# Получение всех работ
print(get('http://localhost:5000/api/v2/jobs').json())

# Пустой запрос
print(post('http://localhost:5000/api/v2/jobs').json())

# Передан только тимлид
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 'Peter'}).json())

# Передано только название
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'read a book'}).json())

# Корректный запрос
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 'Peter',
                 'job': 'read a book',
                 'work_size': 2,
                 'collaborators': '1',
                 'is_finished': False}).json())


# Данные первой работы
print(get('http://localhost:5000/api/v2/jobs/1').json())

# Работы с таким id нет
print(get('http://localhost:5000/api/v2/jobs/999').json())

# Указана строка
print(get('http://localhost:5000/api/v2/jobs/q').json())

# Удаление 1 работы
print(delete('http://localhost:5000/api/v2/jobs/1').json())

# Работы с таким id нет
print(delete('http://localhost:5000/api/v2/jobs/999').json())

# Указана строка
print(delete('http://localhost:5000/api/v2/jobs/q').json())