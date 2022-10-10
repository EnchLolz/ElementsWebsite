from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Words_Into_Elements import ConvertToElements

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Converter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Word %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        word_content = request.form['word']
        new_word = Converter(name=word_content)
        return render_template('index.html', words=new_word, elements=ConvertToElements(word_content, [[]]))
        # try:
        #     db.session.add(new_word)
        #     db.session.commit()
        #     return redirect('/')
        # except:
        #     return "There was an issue adding your word"
    else:
        words = Converter.query.order_by(Converter.date_created).order_by(Converter.date_created.desc()).first()
        return render_template('index.html', words=words, elements=ConvertToElements(words.name, [[]]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)

