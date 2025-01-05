import pytest
from flask import session, url_for
from app import app
import db

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
    assert "登録が完了しました" in response.data.decode('utf-8')  # 完了画面にメッセージが表示される
