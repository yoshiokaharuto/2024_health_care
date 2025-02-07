import pytest
import db
from flask import url_for
from app import app,db, HealthUsers
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
        

def test_food_record_page(client, logged_in_user):
    """食事記録ページが開けるかテスト"""
    response = client.get('/health/food_record')
    assert response.status_code == 200
    assert "食事記録" in response.data.decode('utf-8')

def test_food_record_confirm_page(client, logged_in_user):
    """食事記録の確認画面の動作テスト"""
    response = client.post('/health/food_record_confirm', data={
        'date': '2025-02-05',
        'meal_type': 'breakfast',
        'meal_detail': 'パン, サラダ'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
def test_food_record_execute(client, logged_in_user):
    """食事記録がDBに保存されるかのテスト"""
    with client.session_transaction() as session:
        session['date'] = '2025-02-05'
        session['meal_type'] = 'breakfast'
        session['meal_detail'] = ['パン', 'サラダ']
    
    response = client.get('/health/food_record_execute', follow_redirects=False)
    
    assert response.status_code == 302
    
def test_meal_search_page_get(client, logged_in_user):
    """食事検索ページ（GET）のテスト"""
    response = client.get('/health/meal_search')
    assert response.status_code == 200

def test_meal_search_page_post(client, logged_in_user):
    """食事検索ページ（POST）のテスト"""
    # 日付のフォームを送信して検索結果を得る
    response = client.post('/health/meal_search', data={
        'meal_date': '2025-02-05'
    }, follow_redirects=True)
    
    assert response.status_code == 200
