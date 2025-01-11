from flask import Flask, render_template, redirect, url_for, session
import string, random,hashlib,db
from user import user_bp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_login import current_user


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(user_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'top'

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9981@localhost/postgres'
db.init_app(app)

class UserLogin(FlaskForm):
    email = StringField(
        'メールアドレス',
        validators = [DataRequired(message='メールアドレスが未入力です'),
                      Email(message='メールアドレスの形式が正しくありません')
                      ])
    password = PasswordField(
        'パスワード',
        validators = [DataRequired(message='パスワードが未入力です'),
                      Length(min=6,message='パスワードは6文字以上で入力してください')])  
    submit = SubmitField('ログイン') 

class HealthUsers(db.Model,UserMixin):
    user_id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)
    salt = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    
    def get_id(self):
        return str(self.user_id)
    
    def verify_password(self,password) -> bool:
        salt_str = self.salt
        input_hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt_str.encode('utf-8'),1000).hex()
        return input_hash == self.hashed_password

@login_manager.user_loader
def load_user(user_id):
    return HealthUsers.query.get(user_id)

@app.route('/',methods=['GET','POST'])
def top():
    form = UserLogin()
    if 'mail' in session:
        session.pop('mail')
    
    return render_template('index.html',form=form)

@app.route('/login',methods=['POST'])
def login():
    form = UserLogin()
    email = form.email.data
    password = form.password.data        
    user = HealthUsers.query.filter_by(email=email).first()
    if form.validate_on_submit():
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('user_top'))
    
    return render_template('index.html',form=form)

@app.route('/user_top',methods=['GET'])
@login_required
def user_top():
    return render_template('user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('top'))

if __name__ == '__main__':
    app.run(debug=True)