from flask import Flask, render_template,session,redirect, url_for, request
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
from flask_bcrypt import Bcrypt
import os
from flask import flash
import uuid
import json
import numpy

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

login_manager = LoginManager(app)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
bcrypt=Bcrypt(app)

class User(UserMixin):
    def __init__(self,id,username,email,password):
        self.id = id
        self.username =username
        self.email= email
        self.password=password

    @property
    def is_active(self):
        return True

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username =request.form['username']
        email =request.form['email']
        password =request.form['password']
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

        new_uuid=uuid.uuid4()
        uuid_str= str(new_uuid)

        new_user=User(uuid_str,username,email,hashed_password)
      
        print(f' --{username} -- {hashed_password}')

        if(uuid_str,username,email,hashed_password) not in load_users():
            save_user(new_user)
            
            return redirect(url_for('login'))
    return render_template('register.html')


def save_user(user):
    with open("users.txt","a") as file:
        file.write(f'{user.id};{user.username};{user.email};{user.password}\n')
    
def load_users():
    with open("users.txt","r") as file:
        lines =file.readlines()
        return [line.strip().split(';') for line in lines]
    
def load_user_by_username_password(username,password):
    with open("users.txt","r") as file:
        for user in file:
            user_id,stored_username,stored_email,stored_hashed_password = user.strip().split(';')
            # id_str=str(user_id)

            if stored_username ==username and bcrypt.check_password_hash(stored_hashed_password,password):
                return User(id=str(user_id),username=stored_username,email=stored_email,password=stored_hashed_password)
    return None
            

@login_manager.user_loader
def load_user(user_id):   
    users = load_users()
    for user in users:
        if user[0] == user_id:
            return User(id=user[0], username=user[1], email=user[2], password=user[3])

    return None

@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        user = load_user_by_username_password(username,password)
        if user:
            login_user(user)
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Incorrect username/password. Please try again.', 'warning')

    return render_template('login.html')

def read_movies_from_file():
    try:
        with open("movies.json","r",encoding="utf-8") as file:
            file_contents = file.read()
           
            movies=json.loads(file_contents)
            print(f'length: {len(movies)}')
        return movies
    except FileNotFoundError as e:
        print(f'Find not found, reason: {e}')
        return []

    except json.JSONDecodeError:
        print("Error: Unable to decode JSON from movies.json.")
        return []

@app.route('/home',methods=['GET','POST'])
@login_required
def home():   
    movies=read_movies_from_file()      
    year =[]    
     # x=numpy.array(list) and then use numpy.unique(x) 
    for movie in movies:
        year_str =movie.get('release_date').strip().split('-')[0]
        year.append(year_str)
        year_x = numpy.array(year)
        y = numpy.unique(year_x)

    selected_year=request.args.get('selected_year',default='all')
    if selected_year != 'all':
         filtered_movies = [movie for movie in movies if movie.get('release_date', '').startswith(selected_year)]
         return render_template('home.html',user=current_user,movies=filtered_movies,years=y,selected_year=selected_year)
    
    return render_template('home.html',user=current_user,movies=movies,years=y,selected_year='all')


@app.route('/save/<original_title>',methods=['POST'])
def save(original_title=None):
    if request.method=='POST' and current_user.is_authenticated:
        print(original_title)
        user_identifier =current_user.id
        user_record=f'{user_identifier};{current_user.username};{current_user.email};{current_user.password}'

        components = user_record.split(';')
        current_movie_titles = set(components[4:])
        print(f'current_movie_title:  {current_movie_titles}')

        if len(current_movie_titles)<3 and original_title not in current_movie_titles:
            
            with open("users.txt","a",encoding='utf-8') as file:
                delimiter = ';' 
                file.write(f'{delimiter}{original_title}')

            print("Saved successfully")
            redirect(url_for('home'))
        else:
            print("User already has three movies saved. Cannot add more.")
            return redirect(url_for('home'))
    return redirect(url_for('home'))

def load_actors_from_file():
   try:
      with open("actors.json","r",encoding="utf-8") as file:
         file_contents =file.read()
         actors_data =json.loads(file_contents)
      return actors_data
   except FileNotFoundError as e:
        print(f'Find not found, reason: {e}')
        return []

   except json.JSONDecodeError:
        print("Error: Unable to decode JSON from actors.json.")
        return []
@app.route('/actors',methods=['GET','POST'])
def actors():
  
    actors_file=load_actors_from_file()
    return render_template('actors.html',user=current_user,actors=actors_file)

def load_actor_by_id(id):
    with open("actors.json","r",encoding="utf-8") as file:
        actors_file =json.load(file) #NO `s` in `load`
        # print("All actors:", actors_file)
    for actor in actors_file:
        print(f'actor id in loop: {actor["id"]}')
        actor_id=str(actor.get("id",""))
        if actor_id == id:
            print(f'actor id in IF: {actor_id}')
            return actor

    return None

@app.route('/actor-movies/<actor_id_pass>')
def actor_movies(actor_id_pass):
    actor =load_actor_by_id(actor_id_pass)
    print(f'load_by_id {actor}')
    return render_template('actor-movies.html',actor_id_pass=actor_id_pass,user=current_user,actor=actor)


@app.route('/profile')
def profile():
    return render_template('profile.html',user=current_user)


@app.route('/logout',methods=['POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
