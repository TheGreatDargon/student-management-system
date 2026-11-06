from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per 10 minutes"],
    storage_uri="memory://",
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Class Model
class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    post_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    father_number = db.Column(db.String(15), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    mother_number = db.Column(db.String(15), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    class_ = db.relationship('Class', backref='students')

# Staff Model
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create database and add sample classes
with app.app_context():
    db.create_all()
    if not Class.query.first():
        classes = [
            Class(name='Class 10A'),
            Class(name='Class 10B'),
            Class(name='Class 11A'),
            Class(name='Class 12A')
        ]
        db.session.bulk_save_objects(classes)
        db.session.commit()

@app.route('/')
def index():
    if 'staff' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('table.html', students=students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        staff = Staff.query.filter_by(username=username).first()
        if staff and bcrypt.checkpw(password, staff.password):
            session['staff'] = staff.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_staff = Staff(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_staff)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Username or email already exists.', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('staff', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'staff' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            new_student = Student(
                username=request.form['username'],
                email=request.form['email'],
                password=request.form['password'],
                name=request.form['name'],
                age=int(request.form['age']),
                date_of_birth=request.form['dateOfBirth'],
                gender=request.form['gender'],
                street=request.form['street'],
                city=request.form['city'],
                region=request.form['region'],
                post_code=request.form['postCode'],
                country=request.form['country'],
                father_name=request.form['fatherName'],
                father_number=request.form['fatherNumber'],
                mother_name=request.form['motherName'],
                mother_number=request.form['motherNumber'],
                class_id=int(request.form['class_id'])
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid input. Please check the data.', 'danger')
        except:
            db.session.rollback()
            flash('Error adding student. Ensure all fields are valid.', 'danger')
    classes = Class.query.all()
    return render_template('form.html', classes=classes)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'staff' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.age = int(request.form['age'])
            student.date_of_birth = request.form['dateOfBirth']
            student.gender = request.form['gender']
            student.street = request.form['street']
            student.city = request.form['city']
            student.region = request.form['region']
            student.post_code = request.form['postCode']
            student.country = request.form['country']
            student.father_name = request.form['fatherName']
            student.father_number = request.form['fatherNumber']
            student.mother_name = request.form['motherName']
            student.mother_number = request.form['motherNumber']
            student.class_id = int(request.form['class_id'])
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid input. Please check the data.', 'danger')
        except:
            db.session.rollback()
            flash('Error updating student.', 'danger')
    classes = Class.query.all()
    return render_template('update.html', datas=student, classes=classes)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    if 'staff' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Error deleting student.', 'danger')
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_student():
    if 'staff' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    search_id = request.form['search_id']
    try:
        student = Student.query.filter_by(id=int(search_id)).all()
        if student:
            return render_template('table.html', students=student)
        else:
            flash('No student found with that ID.', 'danger')
    except ValueError:
        flash('Please enter a valid ID.', 'danger')
    return redirect(url_for('index'))


@app.route("/slow")
@limiter.limit("5 per 10 minutes")
def slow():
    return ":("



if __name__ == '__main__':
    app.run(debug=True)