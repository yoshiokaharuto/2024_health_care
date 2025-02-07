import pytest
from flask import url_for
from app import app, db, HealthUsers
from health import FoodRecord
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
        
def test_health_record_page(client, logged_in_user):
    response = client.get('/health/health_record')
    assert response.status_code == 200
    assert "健康記録" in response.data.decode('utf-8')
    
def test_health_record_confirm_page(client, logged_in_user):
    response = client.post('/health/health_record_confirm', data={
        'date': '2025-02-05',
        'sleep_time': 7,
        'weight': 60,
        'water_intake':1000,
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_exercise_record_execute(client, logged_in_user):
    with client.session_transaction() as session:
        session['health_date'] = '2025-02-05'
        session['sleep_time'] = 6
        session['weight'] = 60,
        session['water_intake'] = 1000
    
    response = client.get('/health/health_record_execute', follow_redirects=False)
    assert response.status_code == 302
    

def test_meal_search_page_get(client, logged_in_user):
    response = client.get('/health/health_search')
    assert response.status_code == 200

def test_meal_search_page_post(client, logged_in_user):
    response = client.post('/health/health_search', data={
        'health_date': '2025-02-05'
    }, follow_redirects=True)
    
    assert response.status_code == 200
