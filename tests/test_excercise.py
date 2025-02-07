import pytest
from flask import url_for
from app import app, db, HealthUsers
from health import ExerciseRecord
from datetime import date

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client
        
@pytest.fixture
def logged_in_user(client):
    with app.app_context():
        user = HealthUsers(
            email="testuser@example.com",
            hashed_password="hashedpassword",
            salt="random_salt",
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as session:
            session['user_id'] = user.user_id

        yield user

        db.session.delete(user)
        db.session.commit()
        
def test_exercise_record_page(client, logged_in_user):
    response = client.get('/health/exercise_record')
    assert response.status_code == 200
    assert "運動記録" in response.data.decode('utf-8')
    
def test_exercise_record_confirm_page(client, logged_in_user):
    response = client.post('/health/exercise_record_confirm', data={
        'date': '2025-02-05',
        'exercise_time': 30,
        'exercise_detail': 'ウォーキング'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_exercise_record_execute(client, logged_in_user):
    with client.session_transaction() as session:
        session['exercise_date'] = '2025-02-05'
        session['exercise_time'] = 30
        session['exercise_detail'] = 'ウォーキング'
    
    response = client.get('/health/exercise_record_execute', follow_redirects=False)
    assert response.status_code == 302