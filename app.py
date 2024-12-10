from flask import Flask, render_template , redirect, url_for,session
import string,random
from user import user_bp

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

app.register_blueprint(user_bp)

@app.route('/')
def top():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)