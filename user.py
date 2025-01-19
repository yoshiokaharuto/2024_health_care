from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash
import db, string, random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField,FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

user_bp = Blueprint('user', __name__, url_prefix='/user')

class SignupForm(FlaskForm):
    email = StringField(
        'メールアドレス',
        validators=[DataRequired(message='メールアドレスが未入力です'),
                    Email(message='メールアドレスの形式が正しくありません')
                    ])
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(message='パスワードが未入力です'),
        Length(min=6, message='パスワードは6文字以上で入力してください')])
    
    password_confirm = PasswordField(
        'パスワード(確認用)',
        validators=[
            DataRequired(message='パスワードが未入力です'),
            EqualTo('password', message="パスワードが一致しません")
        ]
    )
    submit = SubmitField('確認')

class ProfileForm(FlaskForm):
    birthday = DateField(
        '生年月日',
        validators=[DataRequired(message='生年月日が未入力です')],
        format='%Y-%m-%d'
    )
    height = FloatField(
        '身長',
        validators=[DataRequired(message='身長が未入力です'),NumberRange(min=0)]
    )
    weight = FloatField(
        '体重',
        validators=[DataRequired(message='体重が未入力です'),NumberRange(min=0)]
    )
    target_weight = FloatField(
        '目標体重',
        validators=[DataRequired(message='目標体重が未入力です'),NumberRange(min=0)]
    )
    target_sleep = FloatField(
        '目標睡眠時間',
        validators=[DataRequired(message='目標睡眠時間が未入力です'),NumberRange(min=0,max=24)]
    )
    daily_excercise = FloatField(
        '1日の運動時間',
        validators=[DataRequired(message='1日の運動時間が未入力です'),NumberRange(min=0,max=24)]
    )
    submit = SubmitField('プロフィールを更新')
    

@user_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if 'mail' in session:
        email = session['mail']
    else:
        email = None 
    return render_template('user/sign_up.html', form=form, email=email)

@user_bp.route('/sign_up_confirm', methods=['POST'])
def sign_up_confirm():
    form = SignupForm()
    session['mail'] = form.email.data
    email = session['mail']

    if form.validate_on_submit():
        password = form.password.data
        salt = db.get_salt()
        hashed_pw = db.get_hash(password, salt)
        session['salt'] = salt
        session['password'] = hashed_pw
        return render_template('user/sign_up_confirm.html', email=email)
    else:
        return render_template('user/sign_up.html', form=form, email=email)
    
@user_bp.route('/sign_up_execute')
def sign_up_execute():
    form = SignupForm()
    mail = session.get('mail')
    pw = session.get('password')
    salt = session.get('salt')
    count = db.user_register(mail, pw,salt)
    
    if count == 1:
        flash('登録が完了しました')
        return redirect(url_for('top'))
    else:
        return render_template('user/sign_up.html', form=form)

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    return render_template('user/profile.html', form=form)