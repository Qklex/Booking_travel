from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user

from booking import db, admin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    fam = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    rol = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return self.name


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text, nullable=False)
    photo1 = db.Column(db.Text, nullable=False)
    photo2 = db.Column(db.Text, nullable=False)
    photo3 = db.Column(db.Text, nullable=False)
    photo4 = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    name_operator = db.Column(db.String(128), nullable=False)
    where_from = db.Column(db.String(128), nullable=False)
    where = db.Column(db.String(128), nullable=False)
    date = db.Column(db.String(15), nullable=False)
    date_obr = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time1 = db.Column(db.String(10), nullable=False)
    time2 = db.Column(db.String(10), nullable=False)
    time_obr1 = db.Column(db.String(10), nullable=False)
    time_obr2 = db.Column(db.String(10), nullable=False)
    transport = db.Column(db.String(20), nullable=False)
    hotel = db.Column(db.String(30), nullable=False)
    hotel_date = db.Column(db.String(15), nullable=False)
    hotel_date2 = db.Column(db.String(15), nullable=False)
    route_tour = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    info = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    quantity_emp = db.Column(db.Integer, nullable=False)


class UserList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fam = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    ser = db.Column(db.String(20), nullable=False)
    num = db.Column(db.String(20), nullable=False)
    id_tour = db.Column(db.Integer, nullable = False)


class UserView(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.rol == 1


class CardView(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.rol == 1

class UserListView(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.rol == 1


admin.add_view(UserView(User, db.session))
admin.add_view(UserListView(UserList, db.session))
admin.add_view(CardView(Card, db.session))
