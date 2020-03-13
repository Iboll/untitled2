from flask import Flask, render_template
from data import db_session
from data.news import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.sqlite")


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(Jobs).filter(Jobs.is_private != True)
    return render_template("index.html", news=news)


def main():
    session = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    session.add(user)
    session.commit()
    session = db_session.create_session()
    user = User()
    user.surname = "Martin"
    user.name = "Iden"
    user.age = 23
    user.position = "engineer"
    user.speciality = "research engineer"
    user.address = "module_2"
    user.email = "asd@mars.org"
    session.add(user)
    session.commit()
    session = db_session.create_session()
    user = User()
    user.surname = "Mark"
    user.name = "Jacobs"
    user.age = 19
    user.position = "second captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "jacobs@mars.org"
    session.add(user)
    session.commit()
    session = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Sanders"
    user.age = 21
    user.position = "second engineer"
    user.speciality = "research engineer"
    user.address = "module_3"
    user.email = "rt@mars.org"
    session.add(user)
    session.commit()
    #app.run()


if __name__ == '__main__':
    main()
