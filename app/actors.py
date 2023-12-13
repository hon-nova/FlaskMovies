import requests
import json
from flask import Flask, render_template, request
import os

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
def write_actors_to_file(actors):
   with open("actors.json","w") as file:
      json.dump(actors,file,indent=2)

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
   
@app.route('/fetch-actors',methods=['GET'])
def fetch_actors():
     api_key = os.getenv('MOVIE_KEY')
     url=f'https://api.themoviedb.org/3/person/popular?api_key={api_key}&language=en-CA'

     try:
         response =requests.get(url)
         response.raise_for_status()     

         actors_fetch =response.json()
         actors_file=load_actors_from_file()
         
         actors_old=set((actor['original_name'],actor['profile_path']) for actor in actors_file)

         count=0
        
         for actor in actors_fetch['results']:
            known_for_array=[]
            for eachmovie in actor.get('known_for',[]):
                  known_for = {
                    'backdrop_path': eachmovie.get('backdrop_path',''),
                    'title': eachmovie.get('title',''),
                    'overview': eachmovie.get('overview',''),
                    'poster_path': eachmovie.get('poster_path',''),
                    'release_date': eachmovie.get('release_date','')
                }
                  known_for_array.append(known_for)

            actor_info ={
                'original_name': actor['original_name'],
                'id': actor['id'],
                'profile_path':actor['profile_path'],
                'known_for':known_for_array}                 
           
            if (actor_info['original_name'],actor_info['profile_path']) not in actors_old:
               actors_file.append(actor_info)
               count+=1
            actors_old.add((actor_info['original_name'],actor_info['profile_path']))


         print(f'count actors: {count}')
         print(f'length actors: {len(actors_file)}')
         write_actors_to_file(actors_file)
         return actors_file
     except requests.exceptions.RequestException as e:
      print(f'Error fetching movies, reason: {e}')

if __name__ == '__main__':
   app.run(debug=True)
   