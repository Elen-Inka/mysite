from flask import Flask, render_template, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import dns.resolver
#import smtplib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users1.db'  # Задайте URI для вашей БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
#smtp_server.starttls()
#smtp_server.login("")#Настройка почты, с которой будет отправляться почта. Обязательно почта существующая!

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Временная метка



# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')


# Маршрут для обработки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    email = request.form['textInput']

    ##
    if (email.count("@")==1) and (email.count(".")==1) and ((email[-3:]==".ru") or (email[-4:]==".com")):
        if email.count(" ")>=1:
            while email.count(" ")>=1:
                email = email.replace(" ","",1) # относительный путь прописывается через 2 точки! - Это для практической 22 ноября.
                check_mx_record(email)#
        email=email.lower()
        new_user = User(email=email)
        #check_mx_record(email)#
        # Добавляем запись в базу данных
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is not None:
            new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return "Error!"
            
            
    #else:

def check_mx_record(email): # Не забыть объявить для проверки.
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NoAnswer:
        return False




    # Создаем новую запись
    #new_user = User(email=email)
    
    
    
    # Перенаправляем на главную страницу или другую страницу
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
