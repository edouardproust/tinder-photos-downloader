import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, flash, url_for, Markup, request
import config as c
from helpers import scrap, download, string
import datetime
import random

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET')
app.config["TEMPLATES_AUTO_RELOAD"] = True # Ensure templates are auto-reloaded

# Templates variables & filters
app.jinja_env.globals['sitename'] = c.SITE_NAME
app.jinja_env.globals['today'] = datetime.date.today()
app.jinja_env.globals['author'] = {
    "name": c.AUTHOR_NAME,
    "url": c.AUTHOR_URL,
    "email": c.AUTHOR_EMAIL,
    "social": { "github": c.AUTHOR_GITHUB, "linkedin": c.AUTHOR_LINKEDIN, "stackoverflow": c.AUTHOR_STACKOVERFLOW }
}


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.errorhandler(404)
def not_found(e):
    """404 Error page"""
    return render_template("404.html")


@app.route("/", methods=["GET", "POST"])
def index():

    data = {}
    photos_paths = []

    # POST request
    if request.method == "POST":
        isValidForm = True
        for key in ["user_id", "photos_dimensions", "consent"]:
            value = request.form.get(key)
            if not value:
                isValidForm = False
                flash(Markup(f'Field <i>{string.slug_to_str(key)}</i> is mandatory.'))
            else:
                data[key] = value
        if isValidForm:
            scrapping = scrap.get_photos_urls(data["user_id"], data["photos_dimensions"])
            if 'alert' in scrapping:
                # Display alert 
                flash(Markup(scrapping["alert"]))
            if 'photos' in scrapping:
                # Save photos on saver temporarly
                photos_urls = scrapping["photos"]
                download.save_all(photos_urls)
                # Get relative path for response
                photos_paths = download.get_relative_paths(photos_urls)

    # Get request
    return render_template("index.html", 
        photos_dimensions=c.PHOTOS_DIMENSIONS,
        photos_default_dimension=c.PHOTOS_DEFAULT_DIMENSION,
        data=data,
        photos_paths=photos_paths,
        random_user_id = random.choice(c.USER_ID_EXAMPLES)
    )

if __name__ == '__main__':
    app.run(debug=False)