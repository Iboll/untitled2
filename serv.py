from os import abort

from flask import Flask, render_template, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mars_explorer.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template("index.html", news=jobs)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_jobs(сurrent_user=current_user):
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        current_job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            team_leader=form.team_leader.data,
            is_finished=form.is_finished.data
        )
        current_user.job.append(current_job)
        session.merge(сurrent_user)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()

        news = session.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user).first()
        news1 = session.query(Jobs).filter(Jobs.id == id).first()
        if news:
            form.job.data = news.job
            form.work_size.data = news.work_size
            form.collaborators.data = news.collaborators
            form.team_leader.data = news.team_leader
            form.is_finished.data = news.is_finished
        if news1:
            form.job.data = news1.job
            form.work_size.data = news1.work_size
            form.collaborators.data = news1.collaborators
            form.team_leader.data = news1.team_leader
            form.is_finished.data = news1.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user).first()
        news1 = session.query(Jobs).filter(Jobs.id == id).first()
        if news:
            news.job = form.job.data
            news.work_size = form.work_size.data
            news.collaborators = form.collaborators.data
            news.team_leader = form.team_leader.data
            news.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        if news1:
            news1.job = form.job.data
            news1.work_size = form.work_size.data
            news1.collaborators = form.collaborators.data
            news1.team_leader = form.team_leader.data
            news1.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html', title='Редактирование новости', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user).first()
    news1 = session.query(Jobs).filter(Jobs.id == id).first()
    if news:
        session.delete(news)
        session.commit()
    if news1:
        session.delete(news1)
        session.commit()
    else:
        abort(404)
    return redirect('/')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = StringField('Возраст пользователя', validators=[DataRequired()])
    position = StringField('Должность пользователя', validators=[DataRequired()])
    speciality = StringField('Профессия пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    work_size = StringField('Время на работу', validators=[DataRequired()])
    collaborators = StringField('сollaborators', validators=[DataRequired()])
    team_leader = StringField('team_leader', validators=[DataRequired()])
    is_finished = BooleanField("Законченость")
    submit = SubmitField('Применить')


def main():
    app.run()


if __name__ == '__main__':
    main()
