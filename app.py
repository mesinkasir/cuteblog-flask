from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
content = [
    {
        'title': 'Pembuatan Aplikasi Android',
		  }
]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cute.db'

db = SQLAlchemy(app)

class Cutepost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    cover = db.Column(db.Text)

@app.route('/')
def index():
    posts = Cutepost.query.order_by(Cutepost.date_posted.desc()).all()
    return render_template('index.html', 
	posts=posts,
	title='Cute Blog 🥳', 
    description='A modern web blog template for flask with auto SEO from cuteblog',
    cover='https://www.python.org/static/opengraph-icon-200x200.png'
	)
	
	
	
	
@app.route('/cutelist')
def cutelist():
    posts = Cutepost.query.order_by(Cutepost.date_posted.desc()).all()
    return render_template('cutelist.html', 
	posts=posts,
	title='Cute List Blog 🥳', 
    description='A modern web blog template for flask with auto SEO from cuteblog',
    cover='https://www.python.org/static/opengraph-icon-200x200.png'
	)
	
	
	

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Cutepost.query.filter_by(id=post_id).one()
    return render_template('post.html', 
	post=post
	)
	
@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = Cutepost.query.get_or_404(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/cutelist')
    except:
        return "There was a problem deleting data."



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = Cutepost.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.author = request.form['author']
        post.content = request.form['content']
        post.cover = request.form['cover']

        try:
            db.session.commit()
            return redirect('/cutelist')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        subtitle = "Update Data"
        author = "Update Data"
        content = "Update Data"
        cover = "Update Data"
        return render_template('update.html', title=title, subtitle=subtitle, author=author, content=content, cover=cover, post=post)


@app.route('/cute')
def add():
    return render_template('cute.html')

@app.route('/cutepost', methods=['POST'])
def cutepost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    cover = request.form['cover']

    post = Cutepost(title=title, subtitle=subtitle, author=author, content=content, cover=cover, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('cutelist'))

if __name__ == '__main__':
    app.run(debug=True)