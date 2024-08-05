# day64_100

# Movie Database App
This project is a Flask-based web application that allows users to manage a personal movie database. The app leverages SQLAlchemy for database interactions and integrates with The Movie Database (TMDB) API to fetch and display movie details.

## Features

- __Movie Management:__ Users can add, edit, and delete movies from their collection. The app dynamically updates rankings based on movie ratings.
- __TMDB API Integration:__ Fetches detailed movie information, including titles, release years, descriptions, and poster images, directly from the TMDB API.
- __Responsive Design:__ Built with Flask and Bootstrap to provide a responsive and user-friendly interface.

## Project Structure

- __Database Setup:__ Utilizes SQLAlchemy to create and manage a SQLite database for storing movie information, including fields like title, year, description, rating, ranking, and review.
- __Dynamic Movie Ranking:__ Movies are automatically ranked based on their ratings, ensuring that the top-rated films are prominently displayed.
- __Form Handling:__ Uses Flask-WTF for form management, enabling users to easily add and update movie details.

## Usage

- __Home Page:__ Displays the list of movies sorted by their ranking. Click on any movie to view its details.
- __Add a Movie:__ Use the "Add Movie" button to search for a movie by title and select it from the search results to add to your database.
- __Edit Movie Details:__ Click on a movie's "Edit" button to update its rating and review.
- __Delete a Movie:__ Click the "Delete" button to remove a movie from your collection.

## Future Enhancements
- __User Authentication:__ Add user accounts to personalize movie collections.
- __Search Functionality:__ Implement advanced search features to filter movies based on various criteria.
- __Improved UI:__ Enhance the visual design for a more engaging user experience.

### Demo

![](https://github.com/AlvinChin1608/day64_100/blob/main/gif_demo/ScreenRecording2024-08-02at22.08.13-ezgif.com-video-to-gif-converter.gif)
