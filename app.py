from flask import Flask, render_template, redirect, url_for, session
import string, random
from user import user_bp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(user_bp)

class UserLogin(FlaskForm):
    email = StringField(
        'メールアドレス',
        validators = [DataRequired(message='メールアドレスが未入力です'),
                      Email(message='メールアドレスの形式が正しくありません')
                      ])
    password = PasswordField(
        'パスワード',
        validators = [DataRequired(message='パスワードが未入力です'),
                      Length(mi=6,message='パスワードは6文字以上で入力してください')])  
    submit = SubmitField('ログイン') 

@app.route('/')
def top():
    
    if 'mail' in session:
        session.pop('mail')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)