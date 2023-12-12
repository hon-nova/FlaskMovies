import json
import os
import requests

from dotenv import load_dotenv
load_dotenv()


def read_from_file():
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

api_key = os.getenv('MOVIE_KEY')
url =f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-CA'

try:
   response = requests.get(url)
   response.raise_for_status()

   movies_fetch =response.json()
   

   movies_file = read_from_file()
   movies_old = set((movie['original_title'], movie['release_date']) for movie in movies_file)

   for movie in movies_fetch['results']:
      movie_info ={
         'backdrop_path': movie['backdrop_path'],
         'original_title': movie['original_title'],
         'release_date':movie['release_date'],
         'overview':movie['overview']
      }
      
      if (movie_info['original_title'], movie_info['release_date']) not in movies_old:
            
            movies_file.append(movie_info)
            # Add the new movie to the movies_old set to keep track of existing records
            movies_old.add((movie_info['original_title'], movie_info['release_date']))

   print(f'length movies_file: {len(movies_file)}')

   #write to file
   with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(movies_file, file, indent=2)

except requests.exceptions.RequestException as e:
   print(f'Error fetching movies, reason: {e}')

def display_movies():
    movies = read_from_file()
    for movie in movies:     
        print(f'{movie}')
display_movies()

