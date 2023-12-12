from flask import Flask, render_template,session,redirect, url_for, request,jsonify
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
    with open("users.txt","a", errors='ignore') as file:
        file.write(f'{user.id};{user.username};{user.email};{user.password}\n')
    
def load_users():
    with open("users.txt","r", errors='ignore') as file:
        lines =file.readlines()
        return [line.strip().split(';') for line in lines]
    
def load_user_by_username_password(username,password):
    with open("users.txt","r",encoding="utf-8",errors="ignore") as file:
        for user in file:
            # user_id,stored_username,stored_email,stored_hashed_password = user.strip().split(';')
            components = user.strip().split(";")
            if len(components) >= 4:
                user_id = components[0]
                stored_username = components[1]
                stored_email = components[2]
                stored_hashed_password = components[3]
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
        with open("movies.json","r",encoding="utf-8", errors='ignore') as file:
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


@app.route('/save/<original_title>', methods=['POST'])
def save(original_title=None):
    if request.method == 'POST' and current_user.is_authenticated:
        user_identifier = current_user.id        

        with open("users.txt", "r", encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        print(f'All files:: {lines}')

        # Find and update the correct user's record
        for i, line in enumerate(lines):
            if user_identifier in line:
                components = line.split(';')
                print(f'components array: {components}')
                current_movie_titles = set(components[4:])
                if len(current_movie_titles) < 3 and original_title not in current_movie_titles:
                    lines[i] = f'{line.rstrip()};{original_title}\n'
                    with open("users.txt", "w", encoding='utf-8', errors='ignore') as file:
                        file.writelines(lines)

                    print("Saved successfully")
                    return redirect(url_for('home'))
                else:
                    print("User already has three movies saved. Cannot add more.")
                    flash('User already has three movies saved. Cannot add more.', 'warning')
                    return redirect(url_for('home'))

        print("User not found in the file.")
        return redirect(url_for('home'))

    return redirect(url_for('home'))

def load_actors_from_file():
   try:
      with open("actors.json","r",encoding="utf-8", errors='ignore') as file:
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
    with open("actors.json","r",encoding="utf-8", errors='ignore') as file:
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


@app.route('/profile',methods=['GET'])
def profile():
    if request.method == 'GET' and current_user.is_authenticated:
        
        user_identifier =current_user.id
        with open("users.txt","r",encoding="utf-8",errors="ignore") as file:
            lines =file.readlines()

        for line in lines:
            if user_identifier in line:
                components=line.split(';')
                u_movies=set(components[4:])

        session['user_movies'] = list(u_movies)        

        return render_template('profile.html',user=current_user,user_movies=u_movies)
    return render_template('login.html')

@app.route('/delete/<user_m>',methods=['POST'])
def delete(user_m):
    if request.method == 'POST' and current_user.is_authenticated:
        user_identifier = current_user.id
        user_movies = session.get('user_movies',[])

        if user_m in user_movies:
            user_movies.remove(user_m)

            session['user_movies']= user_movies
            return jsonify({'success': True, 'movie': user_m})
        
        # Read the file content
        with open("users.txt", "r", encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()

        # Find and update the correct user's record
        for i, line in enumerate(lines):
            if user_identifier in line:
                components = line.split(';')
                user_movies = set(components[4:])

                if user_m in user_movies:
                    user_movies.remove(user_m)
                    lines[i] = f'{components[0]};{components[1]};{components[2]};{components[3]};{";".join(user_movies)}\n'

                    # Write the updated content back to the file
                    with open("users.txt", "w", encoding='utf-8', errors='ignore') as file:
                        file.writelines(lines)

                    flash('Movie deleted successfully.', 'success')
                    return redirect(url_for('profile'))

        
    return jsonify({'success': False})


@app.route('/logout',methods=['POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
