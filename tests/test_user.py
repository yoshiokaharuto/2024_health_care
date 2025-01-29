import pytest
from flask import url_for
from app import app, db, HealthUsers
import hashlib

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client
        
def test_sign_up_page(client):
    response = client.get('/user/sign_up')
    assert response.status_code == 200
    assert '新規登録' in response.data.decode('utf-8') #ページ内に含まれている文字列確認
    

def test_sign_up_confirm_page(client):
    response = client.get('/user/sign_up')
    assert response.status_code == 200
    
    response = client.post('/user/sign_up_confirm', data={
        'email': 'test@example.com',
        'password': 'password123',
        'password_confirm': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"test@example.com" in response.data  # 確認画面にメールアドレスが表示される
    

def test_sign_up_execute(client):
    with client.session_transaction() as session:
        session['mail'] = 'test@example.com'
        session['password'] = 'hashed_password'
        
    response = client.get('/user/sign_up_execute',follow_redirects = True)
    
    assert response.status_code == 200



@pytest.fixture
def new_user():
    with app.app_context():  # アプリケーションコンテキストを確保
        # テスト用のユーザーデータを準備
        salt = "random_salt"
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256', 'password123'.encode('utf-8'), salt.encode('utf-8'), 1000
        ).hex()

        user = HealthUsers(
            email="test2@example.com",
            hashed_password=hashed_password,
            salt=salt,
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )

        db.session.add(user)
        db.session.commit()

        yield user  # フィクスチャとしてユーザーを返す

        # テスト終了後、データベースから削除
        db.session.delete(user)
        db.session.commit()

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'ログイン' in response.data.decode('utf-8')

def test_login_valid_user(client, new_user):
    response = client.post('/login', data={
        'email': 'test2@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_invalid_user(client):
    response = client.post('/login', data={
        'email': 'invalid2@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_invalid_password(client, new_user):
    response = client.post('/login', data={
        'email': 'test2@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_logout(client, new_user):
    client.post('/login', data={
        'email': 'test2@example.com',
        'password': 'password123'
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'ログイン' in response.data.decode('utf-8')

def test_logged_in_user(client, new_user):
    with client.session_transaction() as session:
        session['user_id'] = new_user.user_id
    response = client.get('/user_top')
    assert response.status_code == 302
    

def test_profile_page(client):
    response = client.get('/user/profile')
    assert response.status_code == 200
    assert 'プロフィール管理' in response.data.decode('utf-8')
    

def test_profile_confirm_page(client):
    response = client.post('/user/profile_confirm', data = {
        "birthday": "2000-01-01",
        "height": 170.5,
        "weight": 65.2,
        "target_weight": 60.0,
        "target_sleep": 8.0,
        "daily_excercise": 1.5
    },follow_redirects = True)
    assert response.status_code == 200
    assert b"170.5" in response.data

def test_profile_excecute(client):
    with client.session_transaction() as session:
        session['birthday'] =  "2000-01-01",
        session['height'] = 170.5,
        session['weight'] = 65.2,
        session['target_weight'] = 60.0,
        session['target_sleep'] = 8.0
        session['daily_excercise'] = 1.5
        
    response = client.get('user/profile_execute',follow_redirects = True)
    assert response.status_code == 200