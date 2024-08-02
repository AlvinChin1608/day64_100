from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv("./vars/.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

TMDB_API_KEY = os.getenv("API_KEY")
TMDB_API_URL = os.getenv("API_URL")
TMDB_IMAGE_URL = os.getenv("IMAGE_URL")
TMDB_INFO_URL = os.getenv("INFO_URL")

# CREATE DB
class Base(DeclarativeBase):
    pass

# Create the movie db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# ## After adding the new_movie the code needs to be commented out/deleted.
# ## So you are not trying to add the same movie twice. The db will reject non-unique movie titles.
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.drop_all()  # Deletes all tables in the database
#     db.create_all()  # Recreates the tables
#     db.session.add(new_movie)
#     db.session.add(second_movie)
#     db.session.commit()

class EditMovieForm(FlaskForm):
    rating = StringField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

# New Find Movie Form
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    # Query and order movies by rating in descending order
    result = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    )
    all_movies = result.scalars().all()  # Convert ScalarResult to Python list

    # Update rankings based on the sorted order
    for rank, movie in enumerate(all_movies, start=1):
        movie.ranking = rank

    # Commit changes to the database
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditMovieForm()  # Create an instance of the form
    movie_id = request.args.get('id')
    movie_to_update = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():  # Automatically validate form submission
        # Update movie details using form data
        movie_to_update.rating = float(form.rating.data)
        movie_to_update.review = form.review.data

        # Commit changes to the database
        db.session.commit()

        # Redirect back to the home page
        return redirect(url_for('home'))

    # Pre-populate the form with existing data
    form.rating.data = movie_to_update.rating
    form.review.data = movie_to_update.review

    # Handle GET request to render the edit form
    return render_template("edit.html", movie=movie_to_update, form=form)


# New Add Route
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        api_key = TMDB_API_KEY
        response = requests.get(
            TMDB_API_URL,
            params={"api_key": api_key, "query": movie_title}
        )
        data = response.json().get("results", [])
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{TMDB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": TMDB_API_KEY})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            img_url=f"{TMDB_IMAGE_URL}{data['poster_path']}",
            description=data['overview']
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)