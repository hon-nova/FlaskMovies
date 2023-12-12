import requests
import json
from flask import Flask, render_template, request
import os

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()


def write_movies_to_file(movies):
   with open("movies.json","w") as file:
      json.dump(movies,file,indent=2)

def load_movies_from_file():
   #  try:
   #      with open("movies.json", 'r') as file:
   #          data = file.read()
   #          if data:
   #              return json.loads(data)
   #          else:
   #              return []
   #  except FileNotFoundError as err:
   #      print(err)
   #      return []
   #  except json.JSONDecodeError as err:
   #      print(f"Error decoding JSON: {err}")
   #      return []
   try:
      with open("movies.json","r",encoding="utf-8") as file:
         file_contents = file.read()
         movies_data=json.loads(file_contents)
      return movies_data
   
   except FileNotFoundError as e:
        print(f'Find not found, reason: {e}')
        return []

   except json.JSONDecodeError:
        print("Error: Unable to decode JSON from movies.json.")
        return []

@app.route('/fetch-movies',methods=['GET'])
def fetch_movies():
   api_key = os.getenv('MOVIE_KEY')
   # url=f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-CA'
   url2=f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'
   url3=f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=peace'
   try:
      response = requests.get(url3)
      response.raise_for_status()

      movies_fetch =response.json()
      

      movies_file = load_movies_from_file()
      movies_old = set((movie['original_title'], movie['release_date']) for movie in movies_file)
      count=0
      for movie in movies_fetch['results']:
         movie_info ={
            # 'backdrop_path': movie['backdrop_path'],
            'backdrop_path':movie['poster_path'],
            'original_title': movie['title'],
            'release_date':movie['release_date'],
            'overview':movie['overview']
         }
         
         if (movie_info['original_title'], movie_info['release_date']) not in movies_old:
               
               movies_file.append(movie_info)
               count+=1
               # Add the new movie to the movies_old set to keep track of existing records
               movies_old.add((movie_info['original_title'], movie_info['release_date']))

      print(f'count: {count}')
      print(f'length movies_file: {len(movies_file)}')

      #write to file
      with open("movies.json", "w", encoding="utf-8") as file:
         json.dump(movies_file, file, indent=2)

      return movies_file
         
   except requests.exceptions.RequestException as e:
      print(f'Error fetching movies, reason: {e}')

   
if __name__ == '__main__':
   app.run(debug=True)
      
