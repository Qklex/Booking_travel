import base64
import datetime
from pprint import pprint

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from booking import app, db, manager, mail
from booking.models import User, Card, UserList

city = [{'city': 'Город отправления'}, {'city': 'Ростов-на-Дону'}, {'city': 'Молдова'}]
city2 = [{'city2': 'Город прибытия'}, {'city2': 'Ростов-на-Дону'}, {'city2': 'Молдова'}, {'city2': 'New York'}]
hotel = [{'hotel': 'Отель'}, {'hotel': 'Don-Plaza'}, {'hotel': 'Chateau Vartely'}, {'hotel': 'New-Yorker'}]
auto = [{'auto': 'Транспорт'}, {'auto': 'Поезд'}, {'auto': 'Автобус'},
        {'auto': 'Самолёт'}, {'auto': 'Каноэ'}, {'auto': 'Дирижабль'},
        {'auto': 'Теплоход'}]


@app.route('/index')
@app.route('/', methods=['GET'])
def rout():
    return render_template('index.html')


@manager.user_loader
def load_user(user_id):
    us = User.query.get(user_id)
    return us


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):

            login_user(user)

            next_page = request.args.get('next')

            redirect(next_page)
            if request.form['submit']:
                return redirect(url_for('rout'))
        else:
            flash('Некоректный логин и пароль')
    else:
        flash('Пожалуйста заполните поля Логин и Пароль')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    fam = request.form.get('fam')
    name = request.form.get('name')
    second_name = request.form.get('second_name')
    gender = request.form.get('gender')
    location = request.form.get('location')
    email = request.form.get('email')
    date = request.form.get('date')
    phone = request.form.get('phone')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста заполните формы!')
        elif password2 != password:
            flash('Пароли не совпадают!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, fam=fam, name=name, second_name=second_name, gender=gender,
                            location=location, email=email, date=date, phone=phone)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/card', methods=['POST', 'GET'])
@login_required
def card():
    if request.method == "POST":
        current_user.fam = request.form.get('fam')
        current_user.name = request.form.get('name')
        current_user.second_name = request.form.get('second_name')
        current_user.gender = request.form.get('gender')
        current_user.location = request.form.get('location')
        current_user.email = request.form.get('email')
        current_user.date = request.form.get('date')
        current_user.phone = request.form.get('phone')

        try:
            db.session.commit()
            return redirect('/card')
        except:
            return "При изменение профиля произошла ошибка"
    else:
        return render_template('card.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('rout'))


@app.route('/tour', methods=['GET', 'POST'])
def tour():
    tor = Card.query.order_by(Card.id).all()

    city2 = [{'city2': 'Город прибытия'}, {'city2': 'Ростов-на-Дону'}, {'city2': 'Молдова'}, {'city2': 'New York'}]
    rst = request.form.get('city')
    hote = request.form.get('hotel')
    hot = Card.query.order_by((Card.hotel == hote).desc())
    rost = Card.query.order_by((Card.where == rst).desc())

    return render_template('tour.html', tor=tor, city2=city2, rost=rost, rst=rst, hote=hote, hot=hot, hotel=hotel)


@app.route('/tour/<int:id>')
def tour_more(id):
    tord = Card.query.get(id)

    return render_template("tour_more.html", tour=tord)


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


@app.route('/tour_create', methods=['GET', 'POST'])
def tour_create():
    hotel = [{'hotel': 'Отель'}, {'hotel': 'Don-Plaza'}, {'hotel': 'Chateau Vartely'}, {'hotel': 'New-Yorker'}]
    if request.method == 'POST':
        name = request.form.get('name')
        name_operator = request.form.get('name_operator')
        photo = request.files['photo']
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']
        photo3 = request.files['photo3']
        photo4 = request.files['photo4']
        data = photo.read()
        data1 = photo1.read()
        data2 = photo2.read()
        data3 = photo3.read()
        data4 = photo4.read()
        render_file = render_picture(data)
        render_file1 = render_picture(data1)
        render_file2 = render_picture(data2)
        render_file3 = render_picture(data3)
        render_file4 = render_picture(data4)
        where_from = request.form.get('where_from')
        where = request.form.get('where')
        date = request.form.get('date')
        date_obr = request.form.get('date_obr')
        price = request.form.get('price')
        time1 = request.form.get('time1')
        time2 = request.form.get('time2')
        time_obr1 = request.form.get('time_obr1')
        time_obr2 = request.form.get('time_obr1')
        transport = request.form.get('transport')
        hotel = request.form.get('hotel')
        hotel_date = request.form.get('hotel_date')
        hotel_date2 = request.form.get('hotel_date2')
        route_tour = request.form.get('route_tour')
        age = request.form.get('age')
        info = request.form.get('info')
        quantity = request.form.get('quantity')
        quantity_emp = request.form.get('quantity_emp')
        new_card = Card(name=name, name_operator=name_operator, date_obr=date_obr, time_obr1=time_obr1,
                        time_obr2=time_obr2, photo=render_file, where_from=where_from, where=where,
                        date=date, price=price, time1=time1, photo1=render_file1, photo2=render_file2,
                        photo3=render_file3, photo4=render_file4,
                        time2=time2, transport=transport, hotel=hotel, hotel_date=hotel_date,
                        hotel_date2=hotel_date2, route_tour=route_tour, age=age, info=info, quantity=quantity,
                        quantity_emp=quantity_emp)

        db.session.add(new_card)
        db.session.commit()

        return redirect(url_for('tour'))

    return render_template('tour_create.html', city=city, city2=city2, hotel=hotel, auto=auto)


@app.route('/tour/<int:id>/buy_terms', methods=('GET', 'POST'))
def buy_terms(id):
    tord = Card.query.get(id)
    if request.method == 'POST':


        fam = request.form.get('fam')
        name = request.form.get('name')
        second_name = request.form.get('second_name')
        gender = request.form.get('gender')
        date = request.form.get('date')
        ser = request.form.get('ser')
        num = request.form.get('num')
        id_tour = tord.id
        fam1 = request.form.get('fam1')
        name1 = request.form.get('name1')
        second_name1 = request.form.get('second_name1')
        gender1 = request.form.get('gender1')
        date1 = request.form.get('date1')
        ser1 = request.form.get('ser1')
        num1 = request.form.get('num1')
        if not (fam and name and second_name and gender and date and ser and num):
            flash('Вы ввели недостаточно данных')

        else:
            flash('Ваши данные записаны, переходите к оплате')
            list1 = UserList(fam=fam, name=name, second_name=second_name, gender=gender, date=date,
                         ser=ser, num=num, id_tour=id_tour)

            db.session.add(list1)
            db.session.commit()

            if not (fam1 and name1 and second_name1 and gender1 and date1 and ser1 and num1):
                flash('Вы не указали спутника(возможно его нет)')

            else:

                list2 = UserList(fam=fam1, name=name1, second_name=second_name1, gender=gender1, date=date1,
                                 ser=ser1, num=num1, id_tour=id_tour)

                db.session.add(list2)
                db.session.commit()



    return render_template('buy_terms.html', tour=tord)


@app.route('/tour/<int:id>/buy_terms/buy', methods=('GET', 'POST'))
def buy(id):
    sth = [{'sth': 'Страховка'}, {'sth': 'Lite'}, {'sth': 'Full'}, {'sth': 'Optimal'}]
    tord = Card.query.get(id)


    return render_template('buy.html', tour=tord, sth=sth)


@app.route('/tour/<int:id>/buy_terms/buy/check', methods=('GET', 'POST'))
def check(id):
    tord = Card.query.get(id)
    now = datetime.date.today()
    userl = UserList.query.get(id)
    if userl.id_tour == tord.id:
        tord.quantity_emp = tord.quantity_emp + 1
        db.session.commit()
    else:
        tord.quantity_emp = tord.quantity_emp + 0
        db.session.commit()
    if request.method == 'POST':
        msg = Message('Чек оплаты путёвки', recipients=[current_user.email])
        msg.html = render_template('check_email.html', tour=tord, user=current_user, time=now)

        mail.send(msg)

    return render_template('check.html', tour=tord, user=current_user, time=now, )


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next =' + request.url)

    return response
