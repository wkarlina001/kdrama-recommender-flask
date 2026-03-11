from flask import Flask, request, render_template
import pickle
import os
from bing_image_downloader import downloader
from PIL import Image

app = Flask(__name__)

# --- DATA LOADING ---
# Loading the pre-computed movie list and similarity matrix
# movies: DataFrame containing 'Drama_Name' and 'index'
# similarity: 2D array/matrix of cosine similarity scores
movies = pickle.load(open('app/movie_list.pkl', 'rb'))
similarity = pickle.load(open('app/similarity.pkl', 'rb'))

# --- HELPER FUNCTIONS ---

def fetch_poster(title):
    """
    Downloads a single poster image from Bing based on the drama title.
    Saves to: app/static/korean-drama-<title>/
    """
    try:
        downloader.download(
            f"korean-drama-{title}", 
            limit=1, 
            output_dir='app/static',
            adult_filter_off=True, 
            force_replace=False, 
            timeout=60, 
            verbose=False
        )
    except Exception as e:
        print(f"Error downloading poster for {title}: {e}")

def make_recommendation(title):
    """
    Main logic: Finds similar dramas and handles image pathing/downloads.
    """
    # 1. Get the index of the selected drama
    movie_index = movies[movies.Drama_Name == title]["index"].values[0]
    
    # 2. Get similarity scores for this drama and sort them (highest first)
    # [1:5] excludes the drama itself (index 0) and takes the next 4
    similar_indices = sorted(
        list(enumerate(similarity[movie_index])), 
        key=lambda x: x[1], 
        reverse=True
    )[1:5]

    recommended_titles = []
    recommended_posters = []

    for i in similar_indices:
        # Get the name of the recommended drama
        rec_title = movies[movies.index == i[0]]["Drama_Name"].values[0]
        recommended_titles.append(rec_title)
        
        # Define the folder path where the image should be
        folder_name = f'korean-drama-{rec_title}'
        full_path = os.path.join('app/static', folder_name)

        # 3. Check if image exists; if not, download it
        if not os.path.exists(full_path) or not os.listdir(full_path):
            fetch_poster(rec_title)
        
        # 4. Attempt to grab the image file path for the frontend
        try:
            # Grab the first file in the downloaded folder
            image_filename = os.listdir(full_path)[0]
            path = f'static/{folder_name}/{image_filename}'
            recommended_posters.append(path)
        except (IndexError, FileNotFoundError):
            # Fallback: Create a white placeholder image if download failed
            placeholder_path = 'app/static/placeholder.png'
            if not os.path.exists(placeholder_path):
                img = Image.new("RGB", (800, 1280), (240, 240, 240))
                img.save(placeholder_path, "PNG")
            recommended_posters.append('static/placeholder.png')

    return recommended_titles, recommended_posters

# --- ROUTES ---

@app.route("/", methods=['GET', 'POST'])
def main():
    """Renders the homepage with a dropdown list of all dramas."""
    movie_list = sorted(movies['Drama_Name'].values)
    return render_template('index.html', movie_list=movie_list)

@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    """Handles the form submission and displays recommendations."""
    if request.method == 'POST':
        # Get selected drama from the form
        selected_movie = request.form.get('movie_list')
        
        # Generate recommendations and poster paths
        recommend_names, recommend_posters = make_recommendation(selected_movie)  

        return render_template(
            'recommend.html',
            movie=selected_movie, 
            recommend=recommend_names, 
            movie_poster=recommend_posters
        )
    # Redirect back to home if accessed via GET
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure static directory exists
    if not os.path.exists('app/static'):
        os.makedirs('app/static')
    app.run(debug=True)
