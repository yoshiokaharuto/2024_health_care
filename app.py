from flask import Flask, render_template , redirect, url_for
import string,random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

@app.route('/')
def top():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)