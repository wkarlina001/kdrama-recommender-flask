from flask import Flask, request, render_template
import pickle
import os
from bing_image_downloader import downloader
from PIL import Image

app = Flask(__name__)
movies = pickle.load(open('app/movie_list.pkl','rb'))
similarity = pickle.load(open('app/similarity.pkl','rb'))
img = Image.new("RGB", (800, 1280), (255, 255, 255))
img.save("app/static/image.png", "PNG")

@app.route("/", methods=['GET', 'POST'])
def main():
    movie_list = sorted(movies['Drama_Name'].values)
    return render_template('index.html', movie_list=movie_list)


@app.route("/recommend", methods =['GET','POST'])
def recommend():
    if request.method == 'POST':
        text = request.form['movie_list']
        recommend_movies, movie_poster = make_recommendation(text)  

        return render_template('recommend.html',movie = text, recommend=recommend_movies, movie_poster = movie_poster)
    else:
        return render_template('index.html')

def fetch_poster(title):
    downloader.download("korean-drama-"+title, limit=1, output_dir='static', \
        adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    return 0

def make_recommendation(title):
    movie_index = movies[movies.Drama_Name == title]["index"].values[0]
    similar_movies = list(enumerate(similarity[movie_index])) #accessing the row corresponding to given movie to find all the 

    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:5]
    similar_movies = []
    movies_poster = []

    for element in sorted_similar_movies:
        title = movies[movies.index == element[0]]["Drama_Name"].values[0]
        similar_movies.append(title)
        
        try:
            os.listdir('app/static/korean-drama-'+title)
        except:
            fetch_poster(title)
        
        try:
            image = os.listdir('app/static/korean-drama-'+title)[0]
            path = 'static/korean-drama-'+title+'/'+image
            movies_poster.append(path)
        except:
            path = "static/image.png"
            movies_poster.append(path)

    return similar_movies, movies_poster

if __name__ == '__main__':
    app.run()