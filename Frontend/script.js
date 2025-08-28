// --- 1. Get references to our HTML elements ---
const searchBtn = document.getElementById('searchBtn');
const movieInput = document.getElementById('movieInput');
const resultsDiv = document.getElementById('results');
const loader= document.getElementById('loader');
const errorMessageDiv = document.getElementById('error-message');
const modalContainer = document.getElementById('modal-container');


function showErr(message) {
    errorMessageDiv.innerHTML = `
        <div class="error">
            <div class="error__icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" viewBox="0 0 24 24" height="24" fill="none">
                    <path fill="#393a37" d="m13 13h-2v-6h2zm0 4h-2v-2h2zm-1-15c-1.3132 0-2.61358.25866-3.82683.7612-1.21326.50255-2.31565 1.23915-3.24424 2.16773-1.87536 1.87537-2.92893 4.41891-2.92893 7.07107 0 2.6522 1.05357 5.1957 2.92893 7.0711.92859.9286 2.03098 1.6651 3.24424 2.1677 1.21325.5025 2.51363.7612 3.82683.7612 2.6522 0 5.1957-1.0536 7.0711-2.9289 1.8753-1.8754 2.9289-4.4189 2.9289-7.0711 0-1.3132-.2587-2.61358-.7612-3.82683-.5026-1.21326-1.2391-2.31565-2.1677-3.24424-.9286-.92858-2.031-1.66518-3.2443-2.16773-1.2132-.50254-2.5136-.7612-3.8268-.7612z"></path>
                </svg>
            </div>
            <div class="error__title">${message}</div>
            <div class="error__close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" viewBox="0 0 20 20" height="20">
                    <path fill="#393a37" d="m15.8333 5.34166-1.175-1.175-4.6583 4.65834-4.65833-4.65834-1.175 1.175 4.65833 4.65834-4.65833 4.6583 1.175 1.175 4.65833-4.6583 4.6583 4.6583 1.175-1.175-4.6583-4.6583z"></path>
                </svg>
            </div>
        </div>
    `;
    // Add the event listener to the close button
    const closeBtn = errorMessageDiv.querySelector('.error__close');
    closeBtn.addEventListener('click', () => {
        errorMessageDiv.innerHTML = '';
    });
}


// --- 2. Add an event listener for the button click ---
searchBtn.addEventListener('click', searchMovies);

// Allow pressing 'Enter' in the input field to trigger a search
movieInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        searchMovies();
    }
});


// --- 3. The main function to fetch and display movies ---
async function searchMovies() {
    const movieTitle = movieInput.value.trim();

    // Don't search if the input is empty
    if (movieTitle === "") {
        showErr('Please enter a movie title to search.');
        return;
    }
    
    // Show a loading spinner
    resultsDiv.innerHTML = '<div class="loader"></div>';

    try {
        // Construct the URL for our FastAPI backend, encoding the title to handle spaces and special characters
        const url = `http://127.0.0.1:8000/api/search/${encodeURIComponent(movieTitle)}`;
        
        const response = await fetch(url);

        // Check if the server responded with an error (like 404 or 503)
        if (!response.ok) {
            const errorData = await response.json();
            // Use the detail message from our FastAPI error
            throw new Error(errorData.detail || 'Something went wrong on the server.');
        }

        const data = await response.json();
        displayResults(data.results);

    } catch (error) {
        console.error('Fetch error:', error);
        // Display a user-friendly error message on the page
        showErr(`Oops !${error.message}`);    
    }
}
async function Pop_movies(){
    loader.style.display = 'block';
    resultsDiv.innerHTML = '';
    try
    {
    const url = `http://127.0.0.1:8000/api/popular`;
    const response= await fetch(url);
    if(!response.ok){
         const errorData = await response.json();
        // Use the detail message from our FastAPI error
        throw new Error(errorData.detail || 'Something went wrong on the server.');
  
    }
    const data = await response.json();
    // Call the display function with the fetched data
    displayResults(data.results);
}catch (error) {
        console.error('Fetch error:', error);
        // Display a user-friendly error message on the page
        showErr(`Oops !${error.message}`);
    }
    finally {
        loader.style.display = 'none';
    }
}

// --- 4. Function to display the results in the resultsDiv ---
function displayResults(movies) {
    // Clear previous results or loading spinner
    resultsDiv.innerHTML = '';

    if (movies.length === 0) {
        resultsDiv.innerHTML = '<p>No movies found for that title.</p>';
        return;
    }

    // The base URL for all TMDB poster images
    const posterBaseUrl = 'https://image.tmdb.org/t/p/w500';

    movies.forEach(movie => {
        // Create a new div for each movie
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';

        // Pull out the specific data we want from the movie object
        const title = movie.title;
        const releaseDate = movie.release_date || 'N/A';
        const overview = movie.overview ? movie.overview.substring(0, 150) + '...' : 'No overview available.';
        
        // Build the full poster URL. Use a placeholder if no poster is available.
        const posterUrl = movie.poster_path 
            ? posterBaseUrl + movie.poster_path 
            : 'https://placehold.co/500x750/1e1e1e/bb86fc?text=No+Image';

        // Populate the card with movie info, including the poster image
        movieCard.innerHTML = `
            <img src="${posterUrl}" alt="Poster for ${title}">
            <h2>${title}</h2>
            <p><strong>Release Date:</strong> ${releaseDate}</p>
            <p>${overview}</p>
        `;

        // Add the new card to the results div
        movieCard.addEventListener('click', () => fetchMovieDetails(movie.id));
        resultsDiv.appendChild(movieCard);
    });
}
async function fetchMovieDetails(movieId) {
    loader.innerHTML = '<div class="loading-spinner"></div>';
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/movie/${movieId}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Could not fetch details.');
        }
        const details = await response.json();
        displayModal(details); // Call the function to show the pop-up
    } catch (error) {
        console.error('Fetch details error:', error);
        showErr(error.message);
    } finally {
        loader.innerHTML = '';
    }
}
function displayModal(details) {
    const posterBaseUrl = 'https://image.tmdb.org/t/p/w500';
    const posterUrl = details.poster_path ? posterBaseUrl + details.poster_path : 'https://placehold.co/500x750/1e1e1e/86fccb?text=No+Image';

    modalContainer.innerHTML = `
        <div class="modal-backdrop">
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                <img src="${posterUrl}" alt="Poster for ${details.title}">
                <div class="modal-info">
                    <h2>${details.title}</h2>
                    <p class="tagline"><em>${details.tagline || ''}</em></p>
                    <p>${details.overview || 'No overview available.'}</p>
                    <div class="trivia">
                        <p><strong>Genres:</strong> ${details.genres}</p>
                        <p><strong>Runtime:</strong> ${details.runtime}</p>
                        <p><strong>Budget:</strong> ${details.budget}</p>
                        <p><strong>Revenue:</strong> ${details.revenue}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add event listeners to close the modal
    const closeModal = () => modalContainer.innerHTML = '';
    modalContainer.querySelector('.modal-close').addEventListener('click', closeModal);
    modalContainer.querySelector('.modal-backdrop').addEventListener('click', (e) => {
        // Only close if the click is on the backdrop itself, not the content
        if (e.target === e.currentTarget) closeModal();
    });
}
document.addEventListener('DOMContentLoaded', Pop_movies); 
