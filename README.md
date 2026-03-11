# K-Drama Recommender System
Content-based Recommender system - Web App deployed using Flask and Python 
A Flask-based web application that recommends Korean Dramas based on user selection. The system utilizes content-based filtering and dynamically fetches movie posters from the web.

🚀 Features
Smart Recommendations: Suggests 4 similar dramas based on a selected title using a cosine similarity matrix.

Dynamic Poster Fetching: Automatically downloads drama posters using bing-image-downloader if they aren't available in the local cache.

Local Caching: Stores downloaded images in a static directory to reduce API calls and improve load times.

Fallback Mechanism: Generates a placeholder image if a poster cannot be found or downloaded.

🛠️ Tech Stack
Backend: Flask (Python)

Data Handling: Pandas, Pickle

Image Processing: PIL (Pillow)

Scraping: Bing Image Downloader

Frontend: HTML/Jinja2 templates

📂 Project Structure
Plaintext
.
├── app/
│   ├── static/               # Downloaded posters & placeholder images
│   ├── templates/            # HTML files (index.html, recommend.html)
│   ├── movie_list.pkl        # Pickled DataFrame containing drama metadata
│   └── similarity.pkl        # Pickled similarity matrix
├── main.py                   # Flask application script
└── requirements.txt          # Project dependencies
⚙️ Installation & Setup
Clone the repository:

Bash
git clone <your-repo-link>
cd <repo-folder>
Install dependencies:

Bash
pip install flask pillow bing-image-downloader
Prepare the Models:
Ensure movie_list.pkl and similarity.pkl are located inside the app/ directory. These files contain the drama database and the mathematical "distance" between shows.

Run the application:

Bash
python main.py
Access the app:
Open your browser and navigate to http://127.0.0.1:5000.

🧠 How It Works
Selection: The user selects a drama from the dropdown menu on the homepage.

Vector Search: The app looks up the index of the selected drama and identifies the top 4 most similar items from the similarity.pkl matrix.

Poster Check: * It checks app/static/ for an existing folder with the drama's name.

If missing, it triggers downloader.download() to fetch one from Bing.

Display: The recommend.html page renders the titles and their respective images.
![Screenshot 2022-01-05 at 11 04 44 PM](https://user-images.githubusercontent.com/45416893/148239832-68a174fd-39c4-49cb-a33e-5e7dbe554ffe.png)
