import pytest
class UserRegistration:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password, email):
        if username in self.users:
            return False
        if not self._is_valid_email(email):
            return False
        if not self._is_strong_password(password):
            return False
        self.users[username] = {
            'password': password,
            'email': email
        }
        return True

    def _is_valid_email(self, email):
        # 簡単なメールアドレスのバリデーション
        return "@" in email

    def _is_strong_password(self, password):
        # 簡単なパスワードの強度チェック
        return len(password) >= 6
    
@pytest.fixture
def user_registration():
    return UserRegistration()

def test_successful_registration(user_registration):
    result = user_registration.register_user("testuser", "password123", "testuser@example.com")
    assert result, "Registration failed"
    assert "testuser" in user_registration.users, "User not found in the registration list"

def test_registration_with_existing_username(user_registration):
    user_registration.register_user("testuser", "password123", "testuser@example.com")
    result = user_registration.register_user("testuser", "newpassword", "newemail@example.com")
    assert not result, "Registration with an existing username should fail"
    assert "testuser" in user_registration.users, "User should still be in the registration list"

def test_registration_with_invalid_email(user_registration):
    result = user_registration.register_user("testuser", "password123", "invalid-email")
    assert not result, "Registration with an invalid email should fail"

def test_registration_with_weak_password(user_registration):
    result = user_registration.register_user("testuser", "123", "testuser@example.com")
    assert not result, "Registration with a weak password should fail"
