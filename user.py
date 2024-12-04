from flask import Flask, render_template , redirect, url_for,Blueprint
import string,random
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length,EqualTo

user_bp = Blueprint('user',__name__,url_prefix='/user')

class SignupForm(FlaskForm):
    mail = StringField(
        'メールアドレス',
        validators=[DataRequired(message='メールアドレスが未入力です'),
                    Email(message='メールアドレスの形式が正しくありません')
                    ])
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(message='パスワードが未入力です'),
        Length(min=6,message='パスワードは6文字以上で入力してください')])
    
    password_confirm = PasswordField(
        'パスワード(確認用)',
        validators=[
            DataRequired(message='パスワードが未入力です'),
            EqualTo('password',messag="パスワードが一致しません")
        ]
    )
    submit = SubmitField('登録')
    
    

@user_bp.route('/sign_up',methods=['GET','POST'])
def sign_up():
    return render_template('user/sign_up.html')