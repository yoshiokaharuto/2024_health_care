from flask import Flask, render_template , redirect, url_for,Blueprint

user_bp = Blueprint('user',__name__,url_prefix='/user')

@user_bp.route('/sign_up',methods=['GET','POST'])
def sign_up():
    return render_template('sign_up.html')