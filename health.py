from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash
import db, string, random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField,SelectField,FieldList,FloatField
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
        validators=[DataRequired(message='種類を選択してください')]   
    )
    meal_detail = FieldList(
        StringField('食事内容',
        validators=[DataRequired()]), 
        min_entries=1
    )
    submit = SubmitField('記録')

class ExerciseRecord(FlaskForm):
    date = DateField(
        '日付',
        validators=[DataRequired(message='日付が未入力です。')],
        format='%Y-%m-%d'
    )
    exercise_time = FloatField(
        '運動時間(分)',
        validators=[DataRequired(message='1日の運動時間が未入力です'),NumberRange(min=0)]
    )
    exercise_detail = StringField(
        '運動内容',
        validators=[DataRequired()])
    
    submit = SubmitField('記録')

class HealthRecord(FlaskForm):
    date = DateField(
        '日付',
        validators=[DataRequired(message='日付が未入力です。')],
        format='%Y-%m-%d'
    )
    sleep_time = FloatField(
        '睡眠時間(時間)',
        validators=[DataRequired(message='睡眠時間が未入力です'),NumberRange(min=0)]
    )
    weight = FloatField(
        '体重(kg)',
        validators=[DataRequired(message='体重が未入力です'),NumberRange(min=0)]
    )
    water_intake = FloatField(
        '水分摂取量(ml)',
        validators=[DataRequired(message='水分摂取量が未入力です'),NumberRange(min=0)]
    )
    submit = SubmitField('記録')

class MealSearch(FlaskForm):
    meal_date = DateField(
        '日付',
        format='%Y-%m-%d'
    )
    submit = SubmitField('検索')

@health_bp.route('/food_record',methods=['GET','POST'])
def food_record():
    form = FoodRecord()
    return render_template('health/food_record.html',form=form)

@health_bp.route('/food_record_confirm', methods=['POST'])
def food_record_confirm():
    form = FoodRecord()
    
    if form.validate_on_submit():
        session['date'] = form.date.data
        session['meal_type'] = form.meal_type.data
        session['meal_detail'] = list(form.meal_detail.data)
        print("Session data:", session['meal_detail'])
        return render_template('health/food_record_confirm.html', form=form)
    
    return render_template('health/food_record.html', form=form)
    

@health_bp.route('/food_record_execute')
@login_required
def food_record_execute():
    date = session.get('date')
    meal_type = session.get('meal_type')
    meal_details = session.get('meal_detail')
    user_id = current_user.get_id()

    meal_id = db.insert_meal(user_id, date, meal_type)

    if not meal_id:
        return redirect(url_for('health.food_record'))

    for detail in meal_details:
        success = db.insert_meal_item(meal_id,detail)
        if not success:
            flash("食事記録に失敗しました。", "error")
            return redirect(url_for('health.food_record'))  # 失敗時に戻る

    flash("食事記録が完了しました！", "success")
    return redirect(url_for('user_top'))

@health_bp.route('/exercise_record',methods=['GET','POST'])
def exercise_record():
    form=ExerciseRecord()
    return render_template('health/exercise_record.html',form=form)

@health_bp.route('/exercise_record_confirm',methods=['post'])
def exercise_record_confirm():
    form=ExerciseRecord()
    
    if form.validate_on_submit():
        session['exercise_date'] = form.date.data
        session['exercise_time'] = form.exercise_time.data
        session['exercise_detail'] = form.exercise_detail.data
        return render_template('health/exercise_record_confirm.html')
    else:
        return render_template('health/exercise_record.html',form=form)
    

@health_bp.route('/exercise_record_execute')
def exercise_record_execute():
    form= ExerciseRecord()
    date = session.get('exercise_date')
    exercise_time = session.get('exercise_time')
    exercise_detail = session.get('exercise_detail')
    user_id = current_user.get_id()
    
    count = db.insert_exercise_record(user_id, date, exercise_time, exercise_detail)

    if count == 1:
        flash("運動内容を記録しました",)
        return redirect(url_for('user_top'))
    else:
        return render_template('health/exercise_record.html',form=form)
    
@health_bp.route('/health_record',methods=['GET','POST'])
def health_record():
    form=HealthRecord()
    return render_template('health/health_record.html',form=form)

@health_bp.route('/health_record_confirm',methods=['post'])
def health_record_confirm():
    form=HealthRecord()
    
    if form.validate_on_submit():
        session['health_date'] = form.date.data
        session['sleep_time'] = form.sleep_time.data
        session['weight'] = form.weight.data
        session['water_intake'] = form.water_intake.data
        return render_template('health/health_record_confirm.html')
    else:
        return render_template('health/health_record.html',form=form)

@health_bp.route('/health_record_execute')
def health_record_execute():
    form= HealthRecord()
    date = session.get('health_date')
    sleep_time = session.get('sleep_time')
    weight = session.get('weight')
    water_intake=session.get('water_intake')
    user_id = current_user.get_id()
    
    count = db.insert_health_record(user_id, date, sleep_time, weight,water_intake)

    if count == 1:
        flash("健康を記録しました",)
        return redirect(url_for('user_top'))
    else:
        return render_template('health/health_record.html',form=form)

@health_bp.route('/meal_search',methods=['GET','POST'])
def meal_search():
    form = MealSearch()
    user_id = current_user.get_id()
    
    if request.method == "GET":
        meal_list = db.meal_list(user_id)
    else:
        meal_date = form.meal_date.data
        print(meal_date)
        meal_list = db.meal_search(user_id,meal_date)
        
    return render_template('health/health_search.html',result = meal_list,form=form)