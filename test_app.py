import json
import pytest
from app import app, db, User, Subject, Session, Timetable

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_get_users(client):
    user1 = User(name='Aman Raj', role='Principal')
    user2 = User(name='Sumit Kumar', role='Teacher')
    with app.app_context():
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2

def test_create_user(client):
    user_data = {'name': 'Aman Raj', 'role': 'Teacher'}
    response = client.post('/users', json=user_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'User created successfully'

def test_update_user(client):
    with app.app_context():
        user = User(name='Aman Raj', role='Teacher')
        db.session.add(user)
        db.session.commit()

        user.name = 'Updated Name'
        user.role = 'Updated Role'
        db.session.commit()

        response = client.put(f'/user/{user.id}', json={'name': 'Updated Name', 'role': 'Updated Role'})

        assert response.status_code == 200
        updated_user = User.query.get(user.id)
        assert updated_user.name == 'Updated Name'
        assert updated_user.role == 'Updated Role'

def test_delete_user(client):
    with app.app_context():
        user = User(name='Aman Raj', role='Teacher')
        db.session.add(user)
        db.session.commit()

        response = client.delete(f'/user/{user.id}')

        assert response.status_code == 200
        deleted_user = User.query.get(user.id)
        assert deleted_user is None

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_create_subject(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        request_data = {'name': 'Test Subject'}

        session = Session(bind=db.engine)
        user = session.query(User).filter_by(id=user.id).first()

        query_params = {'user_id': user.id}

        response = client.post('/create_subject', data=json.dumps(request_data), query_string=query_params, content_type='application/json')
        session.close()

    assert response.status_code == 200

def test_add_subject(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        request_data = {'name': 'Test Subject'}

        session = Session(bind=db.engine)
        user = session.query(User).filter_by(id=user.id).first()

        query_params = {'user_id': user.id}

        response = client.post('/create_subject', data=json.dumps(request_data), query_string=query_params, content_type='application/json')
        session.close()

    assert response.status_code == 200

def test_update_subject(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        subject = Subject(name='Sample Subject')
        db.session.add(subject)
        db.session.commit()

        request_data = {'name': 'Updated Subject'}

        session = Session(bind=db.engine)
        user = session.query(User).filter_by(id=user.id).first()

        query_params = {'user_id': user.id}

        response = client.put(f'/update_subject/{subject.id}', data=json.dumps(request_data), query_string=query_params, content_type='application/json')
        session.close()

    assert response.status_code == 200

def test_delete_subject(client):
    with app.app_context():
        user = User(name='Principal User', role='Principal')
        db.session.add(user)
        db.session.commit()

        subject = Subject(name='Sample Subject')
        db.session.add(subject)
        db.session.commit()

        query_params = {'user_id': user.id}

        response = client.delete(f'/delete_subject/{subject.id}', query_string=query_params)

    assert response.status_code == 200

    with app.app_context():
        deleted_subject = Subject.query.get(subject.id)
        assert deleted_subject is None

def test_read_timetables(client):
    with app.app_context():
        user = User(name='Principal User', role='Principal')
        db.session.add(user)
        db.session.commit()

        timetables = [
            Timetable(day='Monday', slot='Morning', subject_id=1),
            Timetable(day='Tuesday', slot='Afternoon', subject_id=2),
            Timetable(day='Wednesday', slot='Evening', subject_id=3),
        ]
        db.session.add_all(timetables)
        db.session.commit()

        query_params = {'user_id': user.id}

        response = client.get('/read_timetables', query_string=query_params)

    assert response.status_code == 200

    expected_timetable_data = [
        {'id': 1, 'day': 'Monday', 'slot': 'Morning', 'subject_id': 1},
        {'id': 2, 'day': 'Tuesday', 'slot': 'Afternoon', 'subject_id': 2},
        {'id': 3, 'day': 'Wednesday', 'slot': 'Evening', 'subject_id': 3},
    ]
    assert response.json == expected_timetable_data

def test_create_timetables(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        request_data = {'day': 'Monday', 'slot': 'Morning', 'subject_id': 1}
        query_params = {'user_id': user.id}

        response = client.post(
            '/add_timetables',
            data=json.dumps(request_data),
            query_string=query_params,
            content_type='application/json',
        )

    assert response.status_code == 200
    assert response.json == {'message': 'Timetable entry created successfully'}

def test_update_timetable(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        timetable = Timetable(day='Monday', slot='Morning', subject_id=1)
        db.session.add(timetable)
        db.session.commit()

        request_data = {'day': 'Tuesday', 'slot': 'Afternoon', 'subject_id': 2}
        query_params = {'user_id': user.id}

        response = client.put(
            f'/update_timetables/{timetable.id}',
            data=json.dumps(request_data),
            query_string=query_params,
            content_type='application/json',
        )

    assert response.status_code == 200
    assert response.json == {'message': 'Timetable entry updated successfully'}

def test_delete_timetable(client):
    with app.app_context():
        user = User(name='Principal User', role='Principal')
        db.session.add(user)
        db.session.commit()

        timetable = Timetable(day='Monday', slot='Morning', subject_id=1)
        db.session.add(timetable)
        db.session.commit()

        query_params = {'user_id': user.id}

        response = client.delete(
            f'/delete_timetables/{timetable.id}',
            query_string=query_params,
            content_type='application/json',
        )

    assert response.status_code == 200
    assert response.json == {'message': 'Timetable entry deleted successfully'}

def test_allocate_subject(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        timetable = Timetable(day='Monday', slot='Morning', subject_id=None)
        subject = Subject(name='Sample Subject')
        db.session.add(timetable)
        db.session.add(subject)
        db.session.commit()

        request_data = {'timetable_id': timetable.id, 'subject_id': subject.id}
        query_params = {'user_id': user.id}

        response = client.post(
            '/allocate_subject',
            data=json.dumps(request_data),
            query_string=query_params,
            content_type='application/json',
        )

    assert response.status_code == 200
    assert response.json == {'message': 'Subject allocated to timetable slot successfully'}

    with app.app_context():
        updated_timetable = Timetable.query.get(timetable.id)
        assert updated_timetable.subject_id == subject.id

def test_read_allocate_subject(client):
    with app.app_context():
        user = User(name='Principal User', role='Principal')
        db.session.add(user)
        db.session.commit()

        timetable1 = Timetable(day='Monday', slot='Morning', subject_id=1)
        timetable2 = Timetable(day='Tuesday', slot='Afternoon', subject_id=2)
        db.session.add(timetable1)
        db.session.add(timetable2)
        db.session.commit()

        query_params = {'user_id': user.id}

        response = client.get('/read_allocate_subject', query_string=query_params)

    assert response.status_code == 200

def test_update_allocation(client):
    with app.app_context():
        user = User(name='Vice-principal User', role='Vice-principal')
        db.session.add(user)
        db.session.commit()

        subject = Subject(name='Sample Subject')
        db.session.add(subject)

        allocation = Timetable(day='Monday', slot='Morning', subject_id=None)
        db.session.add(allocation)
        db.session.commit()

        request_data = {'subject_id': subject.id}
        query_params = {'user_id': user.id}

        response = client.put(
            f'/update_allocations/{allocation.id}',
            data=json.dumps(request_data),
            query_string=query_params,
            content_type='application/json',
        )

    assert response.status_code == 200
    assert response.json == {'message': 'Allocation updated successfully'}

def test_delete_allocation(client):
    with app.app_context():
        user = User(name='Principal User', role='Principal')
        db.session.add(user)
        db.session.commit()

        subject = Subject(name='Sample Subject')
        db.session.add(subject)

        allocation = Timetable(day='Monday', slot='Morning', subject_id=subject.id)
        db.session.add(allocation)
        db.session.commit()

        query_params = {'user_id': user.id}

        response = client.delete(f'/delete_allocations/{allocation.id}', query_string=query_params)

    assert response.status_code == 200
    assert response.json == {'message': 'Allocation deleted successfully'}

def test_get_teachers(client):
    with app.app_context():
        teacher = User(name='Sample Teacher', role='Teacher')
        db.session.add(teacher)
        db.session.commit()

        query_params = {'user_id': teacher.id}

        response = client.get('/teachers', query_string=query_params)

    assert response.status_code == 200
    expected_data = [{'id': teacher.id, 'name': teacher.name}]
    assert response.json == expected_data
