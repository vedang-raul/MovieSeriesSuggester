// --- 1. Get references to our HTML elements ---
const searchBtn = document.getElementById('searchBtn');
const titleInput = document.getElementById('titleInput');
const resultsDiv = document.getElementById('results');
const loader= document.getElementById('loader');
const errorMessageDiv = document.getElementById('error-message');
const modalContainer = document.getElementById('modal-container');
const searchTypeToggle = document.getElementById('search-type-toggle'); // The new toggle switch


// const BaseUrl = "http://localhost:8000"   // For local testing, uncomment it when youre locally testing
// const BaseUrl =  "https://cinematch-ptzm.onrender.com"; // for live deployment
const BaseUrl="https://movieseriessuggester.onrender.com"
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
searchBtn.addEventListener('click', searchtitles);

// Allow pressing 'Enter' in the input field to trigger a search
titleInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        searchtitles();
    }
});


// --- 3. The main function to fetch and display movies ---
async function searchtitles() {
    const query = titleInput.value.trim();

    // Don't search if the input is empty
    if (query === "") {
        showErr('Please enter a title to search.');
        return;
    }
    
    // Show a loading spinner
    resultsDiv.innerHTML = '<div class="loader"></div>';

    try {
        // Construct the URL for our FastAPI backend, encoding the title to handle spaces and special characters
        const searchType = searchTypeToggle.checked ? 'tv' : 'movie';
        const url = `${BaseUrl}/api/search/${searchType}/${encodeURIComponent(query)}`;
        
        console.log('Fetching URL:', url);
        const response = await fetch(url);

        // Check if the server responded with an error (like 404 or 503)
        if (!response.ok) {
            const errorData = await response.json();
            // Use the detail message from our FastAPI error
            throw new Error(errorData.detail || 'Something went wrong on the server.');
        }

        const data = await response.json();
        displayResults(data.results,searchType);

    } catch (error) {
        console.error('Fetch error:', error);
        // Display a user-friendly error message on the page
        showErr(`Oops !${error.message}`);    
    } finally {
        loader.style.display = 'none'; // Hide loader when done
    }
}
async function Pop_movies(){
    loader.style.display = 'block';
    resultsDiv.innerHTML = '';
    try
    {
    const url = `${BaseUrl}/api/popular`;
    const response= await fetch(url);
    if(!response.ok){
         const errorData = await response.json();
        // Use the detail message from our FastAPI error
        throw new Error(errorData.detail || 'Something went wrong on the server.');
  
    }
    const data = await response.json();
    // Call the display function with the fetched data
    displayResults(data.results,searchType='movie');
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
function displayResults(titles,searchType) {
    // Clear previous results or loading spinner
    resultsDiv.innerHTML = '';

    if (titles.length === 0) {
        resultsDiv.innerHTML = '<p>No movies found for that title.</p>';
        return;
    }

    // The base URL for all TMDB poster images
    const posterBaseUrl = 'https://image.tmdb.org/t/p/w500';

    titles.forEach(item => {
        // Create a new div for each movie
        const titleCard = document.createElement('div');
        titleCard.className = 'title-card';
        // Pull out the specific data we want from the movie object
        const title = item.title || item.original_name
        const releaseDate = item.release_date || item.first_air_date || 'N/A';
        const overview = item.overview ? item.overview.substring(0, 150) + '...' : 'No overview available.';
        
        // Build the full poster URL. Use a placeholder if no poster is available.
        const posterUrl = item.poster_path 
            ? posterBaseUrl + item.poster_path 
            : 'https://placehold.co/500x750/1e1e1e/bb86fc?text=No+Image';

        // Populate the card with movie info, including the poster image
        titleCard.innerHTML = `
            <img src="${posterUrl}" alt="Poster for ${title}">
            <h2>${title}</h2>
            <p><strong>Release Date:</strong> ${releaseDate}</p>
            <p>${overview}</p>
        `;

        // Add the new card to the results div
        titleCard.addEventListener('click', () => fetchtitleDetails(item.id,searchType));
        resultsDiv.appendChild(titleCard);
    });
}
async function fetchtitleDetails(titleId, searchType) {
    loader.style.display = 'block';
    resultsDiv.style.display = 'none'; // Hide results while modal is potentially loading

    try {
        const detailsUrl = `${BaseUrl}/api/${searchType}/${titleId}`;
        const creditsUrl = `${BaseUrl}/api/${searchType}/${titleId}/credits`;
        const watchtitleurl= `${BaseUrl}/api/${searchType}/watch/${titleId}`;

        // Use Promise.all to fetch both endpoints at the same time
        const [detailsResponse, creditsResponse,watchresponse] = await Promise.all([
            fetch(detailsUrl),
            fetch(creditsUrl),
            fetch(watchtitleurl)
        ]);

        if (!detailsResponse.ok || !creditsResponse.ok || !watchresponse.ok) {
            throw new Error('Could not fetch all details for this title.');
        }

        const details = await detailsResponse.json();
        const credits = await creditsResponse.json();
        const watchproviders = await watchresponse.json();
        
        // Pass all data to the modal
        displayModal(details, credits,searchType,watchproviders.providers); 
    } catch (error) {
        console.error('Fetch details error:', error);
        showErr(error.message);
    } finally {
        loader.style.display = 'none';
        resultsDiv.style.display = 'grid'; // Show results again
    }
}
function displayModal(details,credits,searchType,watchproviders) {
    const posterUrl = details.poster_path || 'https://placehold.co/500x750/1e1e1e/86fccb?text=No+Image';
    const posterAreaHtml = `
        <div class="modal-poster-area">
            <img src="${posterUrl}" alt="Poster for ${details.title || details.original_name}">
            ${details.tagline ? `<p class="tagline"><em><b>"${details.tagline}"</b></em></p>` : ''}
        </div>
    `;

    let detailsHtml = '';
    

    if (searchType === 'movie') {
        detailsHtml = `
            <p><strong>Genres:</strong> ${details.genres}</p>
            <p><strong>Runtime:</strong> ${details.runtime}</p>
            <p><strong>Budget:</strong> ${details.budget}</p>
            <p><strong>Revenue:</strong> ${details.revenue}</p>
        `;
    } else { // It's a TV show
        detailsHtml = `
            <p><strong>Genres:</strong> ${details.genres}</p>
            <p><strong>First Aired:</strong> ${details.first_air_date}</p>
            <p><strong>Last Aired:</strong> ${details.last_air_date}</p>
            <p><strong>Seasons:</strong> ${details.number_of_seasons}</p>
            <p><strong>Episodes:</strong> ${details.number_of_episodes}</p>
            <p><strong>Status:</strong> ${details.status}</p>
            <p><strong>Created By:</strong> ${details.creators}</p>

        `;
    }
    let triviaHtml = '';
    if (details.tagline){
        triviaHtml = `
        <divclass="trivia">
        <p><em>"${details.tagline}"</em></p>
        </div>
        `;
    }
    
    let creditsHtml = '';
    let castList = credits; // Assume it's a proper array by default

    // FIX: Check if 'cast' is a string that looks like an array, and if so, parse it.
    if (typeof castList === 'string' && castList.startsWith('[')) {
        try {
            castList = JSON.parse(castList);
        } catch (e) {
            console.error("Could not parse cast string:", e);
            castList = []; // Default to empty array on parsing error
        }
    }

    // Final safety check to ensure castList is an array
    if (!Array.isArray(castList)) {
        castList = [];
    }
    if (castList.length > 0) {
        creditsHtml += '<div class="cast-section"><h3>Top Cast</h3><ul class="cast-list">';
        castList.forEach(member => {
            creditsHtml += `<li>${member}</li>`;
        });
        creditsHtml += '</ul></div>';
    }
    let watchHtml = '';
    if (watchproviders && watchproviders.length > 0) {
        watchHtml += '<div class="watch-section"><h3>Where to Watch</h3><div class="provider-list">';
        watchproviders.forEach(provider => {
            watchHtml += `
                <div class="provider-item">
                    <img src="https://image.tmdb.org/t/p/w92${provider.logo_path}" alt="${provider.name} logo" title="${provider.name}">
                </div>
            `;
        });
        watchHtml += '</div></div>';
    } else {
        watchHtml = '<div class="watch-section"><p>Not available for streaming in this region.</p></div>';
    }


    modalContainer.innerHTML = `
        <div class="modal-backdrop">
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                ${posterAreaHtml}
                
                <div class="modal-info">
                
                    <h2>${details.title || details.original_name}</h2>
                   
                    <p>${details.overview || 'No overview available.'}</p>
                    
                    <div class="trivia">
                        ${detailsHtml}
                    </div>
                    ${creditsHtml}
                    ${watchHtml}
                </div>
            </div>
        </div>
    `;


    // Add event listeners to close the modal
    const closeModal = () => modalContainer.innerHTML = '';
    modalContainer.querySelector('.modal-close').addEventListener('click', closeModal);
    modalContainer.querySelector('.modal-backdrop').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) closeModal();
    });
}
async function fetchSurprise() {
    loader.style.display = 'block';
    resultsDiv.innerHTML = '';
    errorMessageDiv.innerHTML = '';

    try {
        const searchType = searchTypeToggle.checked ? 'tv' : 'movie';
        const url = `${BaseUrl}/api/surprise/${searchType}`;
        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Could not get a surprise.');
        }
        const surpriseData = await response.json();
        // A surprise result is a single item, so we directly fetch its details
        fetchtitleDetails(surpriseData.id, surpriseData.media_type);
    } catch (error) {
        console.error('Surprise fetch error:', error);
        showErr(error.message);
        loader.style.display = 'none';
    }
}
document.addEventListener('DOMContentLoaded', Pop_movies); 
