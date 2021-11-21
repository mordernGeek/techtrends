from logging import Logger
import sqlite3
#from typing import get_args

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id): 
     
    post = get_post(post_id)

    if post is None:
        app.logger.warning('404 Not found error')
        return render_template('404.html'), 404
      
    else:
        app.logger.info('post was found')
        return render_template('post.html', post=post)
      
# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us retrieved successfully')
    return render_template('about.html')
    

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            #app.logger.info('New Article ' + title  + ' is created!')
            connection.commit()
            connection.close()
            
            return redirect(url_for('index'))

    else:
        
        title = request.form['title']
        content = request.form['content']

        connection = get_db_connection()
        connection.execute('SELECT FROM posts (title) VALUES (?)',
                         (title))
            #app.logger.info('New Article ' + title  + ' is retrieved!')
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('create.html')

# adding the /healthz endpoint

@app.route('/healthz')
def healthz():  #def healthcheck():
    response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
   
    )
    app.logger.info('Healthz endpoint request successful')
    
    return response


# adding the metrics endpoint
@app.route('/metrics')
def metrics():
    counter = 0
    connection = get_db_connection()
    counter = counter + 1
    posts = connection.execute('SELECT * FROM posts')

    connection.close()
    response = app.response_class(
        response=json.dumps({"status":"success","data":{"db_connection_count":counter,"post_count":posts}}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Metrics request successful')
    return response


# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
