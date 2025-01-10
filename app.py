from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, current_user, UserMixin, LoginManager
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ansh'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False, default=func.now())

    user = db.relationship('User', backref='reservations', lazy=True)
    table = db.relationship('Table', backref='reservations', lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('view_available_tables' if user.role == 'user' else 'view_all_tables'))
        else:
            return render_template('login.html', message="Invalid credentials")

    return render_template('login.html')


@app.route('/tables', methods=['GET'])
@login_required
def view_available_tables():
    if current_user.role != 'user':
        return render_template('error.html', message="Unauthorized access"), 403

    available_tables = Table.query.filter_by(is_reserved=False).all()
    return jsonify([{
        "table_number": table.table_number,
        "capacity": table.capacity
    } for table in available_tables])


@app.route('/tables/reserve/table<int:table_number>', methods=['POST'])
@login_required
def reserve_table(table_number):
    if current_user.role != 'user':
        return render_template('error.html', message="Unauthorized access"), 403

    table = Table.query.filter_by(table_number=table_number).first()
    if not table or table.is_reserved:
        return jsonify({"message": "Table not available"}), 400

    reservation_time = datetime.now()
    reservation = Reservation(user_id=current_user.id, table_id=table.id, reservation_time=reservation_time)
    table.is_reserved = True
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Table reserved successfully"}), 200


@app.route('/tables/cancel', methods=['DELETE'])
@login_required
def cancel_reservation():
  
    if current_user.role != 'user':
        return render_template('error.html', message="Unauthorized access"), 403


    reservation = Reservation.query.filter_by(user_id=current_user.id, table_id=Table.id).first()


    if not reservation:
        return jsonify({"message": "No reservation found for this user."}), 404

    
    table = Table.query.get(reservation.table_id)
    if table:
        table.is_reserved = False
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation canceled successfully."}), 200
    else:
        return jsonify({"message": "Table not found."}), 404




@app.route('/admin/tables', methods=['GET'])
@login_required
def view_all_tables():
    if current_user.role != 'admin':
        return render_template('error.html', message="Unauthorized access"), 403

    tables = Table.query.all()
    return render_template('admin_tables.html', tables=tables)


@app.route('/admin/tables', methods=['POST'])
@login_required
def add_table():
    if current_user.role != 'admin':
        return render_template('error.html', message="Unauthorized access"), 403

    table_number = request.form['table_number']
    capacity = request.form['capacity']
    new_table = Table(table_number=table_number, capacity=capacity)
    db.session.add(new_table)
    db.session.commit()
    return redirect(url_for('view_all_tables'))


@app.route('/admin/tables/<int:table_id>', methods=['PUT'])
@login_required
def update_table(table_id):
    if current_user.role != 'admin':
        return render_template('error.html', message="Unauthorized access"), 403

    table = Table.query.get(table_id)
    if not table:
        return render_template('error.html', message="Table not found"), 404

    data = request.get_json()
    if 'capacity' in data:
        table.capacity = data['capacity']
        db.session.commit()
        return jsonify({"message": "Table updated successfully", "table_id": table.id}), 200
    else:
        return jsonify({"message": "Invalid data, 'capacity' required"}), 400


@app.route('/admin/tables/<int:table_id>', methods=['DELETE'])
@login_required
def delete_table(table_id):
    if current_user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    table = Table.query.get(table_id)
    if not table:
        return jsonify({"message": "Table not found"}), 404

    db.session.delete(table)
    db.session.commit()
    
    return jsonify({"message": "Table deleted successfully", "table_id": table.id}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.first():
            admin = User(username='admin', password='admin123', role='admin')
            user = User(username='user', password='user123', role='user')
            db.session.add_all([admin, user])

        if not Table.query.first():
            db.session.add_all([
                Table(table_number=1, capacity=4),
                Table(table_number=2, capacity=2)
            ])
        db.session.commit()
        print("Initial data seeded!")

    app.run(debug=True)


