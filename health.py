from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash
import db, string, random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_login import login_required
from flask_login import current_user

health_bp = Blueprint('health',__name__,url_prefix='/health')

class FoodRecord(FlaskForm):
    date = DateField(
        '日付',
        validators=[DataRequired(message='日付が未入力です。')],
        format='%Y-%m-%d'
    )
    meal_type = SelectField(
        '食事の種類',
        choices=[("", "選択してください"),("1", "朝食"), ("2", "昼食"), ("3", "夕食")],
        validators=[DataRequired()]   
    )
    meal_detail = StringField(
        '食事内容',
        validators=[DataRequired(message='食事内容が未入力です')]
    )
    submit = SubmitField('記録')
    

@health_bp.route('/food_record',methods=['GET','POST'])
def food_record():
    form = FoodRecord()
    return render_template('health/food_record.html',form=form)