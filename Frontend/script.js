// --- 1. Get references to our HTML elements ---
const searchBtn = document.getElementById('searchBtn');
const movieInput = document.getElementById('movieInput');
const resultsDiv = document.getElementById('results');
const loader= document.getElementById('loader');


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
        resultsDiv.innerHTML = '<p class="error-message">Please enter a movie title.</p>';
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
        resultsDiv.innerHTML = `<p class="error-message">Oops! ${error.message}</p>`;
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
        resultsDiv.innerHTML = `<p class="error-message">Oops! ${error.message}</p>`;
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
        resultsDiv.appendChild(movieCard);
    });
}
document.addEventListener('DOMContentLoaded', Pop_movies); 
