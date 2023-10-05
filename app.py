from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)


Session = sessionmaker()
# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(20))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    slot = db.Column(db.String(20))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref='timetables')

with app.app_context():
    db.create_all()



def check_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = request.args.get('user_id')  # Assuming you pass user_id in headers

            # Create the session within the application context
            with app.app_context():
                session = Session(bind=db.engine)  # Bind the session to the engine
                # import pdb; pdb.set_trace()
                user = session.get(User, user_id)
                if user and user.role == role:
                    session.close()  # Close the session when done
                    return func(*args, **kwargs)
                else:
                    session.close()  # Close the session on unauthorized access
                    return jsonify({'message': 'Unauthorized'}), 401
        return wrapper
    return decorator

# Routes for User CRUD operations
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        users_data = [{'id': user.id, 'name': user.name, 'role': user.role} for user in users]
        return jsonify(users_data)

    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(name=data['name'], role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    
@app.route('/user/<int:user_id>', methods=['PUT', 'DELETE'])
def user(user_id):
    if request.method == 'PUT':
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()
        user.name = data['name']
        user.role = data['role']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    
    elif request.method == 'DELETE':
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    
# Routes for Subject CRUD operations
@app.route('/read_subject', methods=['GET'])
@check_role('Principal')
def read_subject():
        user_id = request.headers.get('user_id')
        app.logger.info(f"Received user_id header: {user_id}")  # Log the header value
        subjects = Subject.query.all()
        subjects_data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return jsonify(subjects_data)

@app.route('/create_subject', methods=['POST'])
@check_role('Vice-principal')
def add_subject():
    data = request.get_json()
    new_subject = Subject(name=data['name'])
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({'message': 'Subject created successfully'})
    
@app.route('/update_subject/<int:subject_id>', methods=['PUT'])
@check_role('Vice-principal')
def update_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404

    data = request.get_json()
    subject.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Subject updated successfully'})

@app.route('/delete_subject/<int:subject_id>', methods=['DELETE'])
@check_role('Principal')
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404

    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully'})

# Routes for Timetable CRUD operations
@app.route('/read_timetables', methods=['GET'])
@check_role('Principal')
def read_timetables():
    timetables = Timetable.query.all()
    timetable_data = [{'id': timetable.id, 'day': timetable.day, 'slot': timetable.slot, 'subject_id': timetable.subject_id} for timetable in timetables]
    return jsonify(timetable_data)

@app.route('/add_timetables', methods=['POST'])
@check_role('Vice-principal')
def create_timetables():
    data = request.get_json()
    new_timetable = Timetable(day=data['day'], slot=data['slot'], subject_id=data['subject_id'])
    db.session.add(new_timetable)
    db.session.commit()
    return jsonify({'message': 'Timetable entry created successfully'})
    

@app.route('/update_timetables/<int:timetable_id>', methods=['PUT'])
@check_role('Vice-principal')
def update_timetable(timetable_id):
    timetable = Timetable.query.get(timetable_id)
    if not timetable:
        return jsonify({'message': 'Timetable entry not found'}), 404

    data = request.get_json()
    timetable.day = data['day']
    timetable.slot = data['slot']
    timetable.subject_id = data['subject_id']
    db.session.commit()
    return jsonify({'message': 'Timetable entry updated successfully'})
    
@app.route('/delete_timetables/<int:timetable_id>', methods=['DELETE'])
@check_role('Principal')
def delete_timetable(timetable_id):
    timetable = Timetable.query.get(timetable_id)
    if not timetable:
        return jsonify({'message': 'Timetable entry not found'}), 404

    db.session.delete(timetable)
    db.session.commit()
    return jsonify({'message': 'Timetable entry deleted successfully'})

# Routes for allocating subjects to specific timetable slots
@app.route('/allocate_subject', methods=['POST'])
@check_role('Vice-principal')
def allocate_subject():
    data = request.get_json()
    timetable_id = data['timetable_id']
    subject_id = data['subject_id']

    timetable = Timetable.query.get(timetable_id)
    subject = Subject.query.get(subject_id)

    if not timetable or not subject:
        return jsonify({'message': 'Timetable or subject not found'}), 404

    timetable.subject = subject
    db.session.commit()
    return jsonify({'message': 'Subject allocated to timetable slot successfully'})
    
@app.route('/read_allocate_subject', methods=['GET'])
@check_role('Principal')
def read_allocate_subject():
    allocations = Timetable.query.filter(Timetable.subject_id.isnot(None)).all()
    allocation_data = [{'id': allocation.id, 'day': allocation.day, 'slot': allocation.slot, 'subject_id': allocation.subject_id} for allocation in allocations]
    return jsonify(allocation_data)
    
@app.route('/update_allocations/<int:allocation_id>', methods=['PUT'])
@check_role('Vice-principal')
def update_allocation(allocation_id):
    allocation = Timetable.query.get(allocation_id)
    if not allocation:
        return jsonify({'message': 'Allocation not found'}), 404

    data = request.get_json()
    subject_id = data['subject_id']

    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({'message': 'Subject not found'}), 404

    allocation.subject = subject
    db.session.commit()
    return jsonify({'message': 'Allocation updated successfully'})
    
@app.route('/delete_allocations/<int:allocation_id>', methods=['DELETE'])
@check_role('Principal')
def delete_allocation(allocation_id):
    allocation = Timetable.query.get(allocation_id)
    if not allocation:
        return jsonify({'message': 'Allocation not found'}), 404

    allocation.subject_id = None
    db.session.commit()
    return jsonify({'message': 'Allocation deleted successfully'})

# Read API for Teacher Role
@app.route('/teachers', methods=['GET'])
@check_role('Teacher')
def get_teachers():
    teachers = User.query.filter_by(role='Teacher').all()
    teachers_data = [{'id': teacher.id, 'name': teacher.name} for teacher in teachers]
    return jsonify(teachers_data)

if __name__ == '__main__':
    app.run(debug=True)
