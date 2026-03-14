/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
      const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Get form values
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Clear any previous error message
            const errorDiv = document.getElementById('error-message');
            if (errorDiv) errorDiv.textContent = '';

            try {
                // Send login request to your API
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Store the JWT token in a cookie (expires in 1 day)
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Strict`;
                    
                    // Redirect to main page
                    window.location.href = 'index.html';
                } else {
                    // Display error message
                    const message = data.message || 'Login failed. Please check your credentials.';
                    if (errorDiv) {
                        errorDiv.textContent = message;
                    } else {
                        alert(message);
                    }
                }
            } catch (error) {
                console.error('Login error:', error);
                const errorMsg = 'Network error. Please try again.';
                if (errorDiv) {
                    errorDiv.textContent = errorMsg;
                } else {
                    alert(errorMsg);
                }
            }
        });
    }
  });

  /* 
  This script handles:
  - Authentication check (show/hide login link)
  - Fetching and displaying places
  - Price filter functionality
*/

document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');
    const placesList = document.getElementById('places-list');

    // Helper to get cookie value
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // Check authentication
    const token = getCookie('token');
    if (!token) {
        // No token: show login link (it's visible by default, but ensure)
        if (loginLink) loginLink.style.display = 'inline-block'; // or 'block'
        // Optionally display a message
        placesList.innerHTML = '<p>Please log in to view places.</p>';
    } else {
        // Token exists: hide login link
        if (loginLink) loginLink.style.display = 'none';
        // Fetch and display places
        fetchPlaces(token);
    }

    // Populate price filter dropdown with options
    function populatePriceFilter() {
        const options = [10, 50, 100, 'All'];
        priceFilter.innerHTML = ''; // Clear existing
        options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt === 'All' ? 'all' : opt;
            option.textContent = opt === 'All' ? 'All' : `$${opt}`;
            priceFilter.appendChild(option);
        });
    }
    populatePriceFilter();

    // Fetch places from API
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch places: ${response.status}`);
            }

            const places = await response.json();
            displayPlaces(places);
        } catch (error) {
            console.error('Error fetching places:', error);
            placesList.innerHTML = '<p>Error loading places. Please try again later.</p>';
        }
    }

    // Display places as cards
    function displayPlaces(places) {
        placesList.innerHTML = ''; // Clear previous content

        if (!places || places.length === 0) {
            placesList.innerHTML = '<p>No places available.</p>';
            return;
        }

        places.forEach(place => {
            // Create place card container
            const card = document.createElement('div');
            card.className = 'place-card';
            card.dataset.price = place.price; // Store price for filtering

            // Image (use placeholder if no image provided)
            const image = document.createElement('img');
            image.src = place.image_url || 'images/placeholder.jpg';
            image.alt = place.name;
            image.className = 'place-image';
            card.appendChild(image);

            // Info container
            const info = document.createElement('div');
            info.className = 'place-info';

            // Name
            const name = document.createElement('h3');
            name.textContent = place.name;
            info.appendChild(name);

            // Price
            const price = document.createElement('p');
            price.className = 'price';
            price.innerHTML = `Price per night: <span>$${place.price}</span>`;
            info.appendChild(price);

            // View Details button
            const button = document.createElement('button');
            button.className = 'details-button';
            button.textContent = 'View Details';
            button.onclick = () => {
                window.location.href = `place.html?id=${place.id}`;
            };
            info.appendChild(button);

            card.appendChild(info);
            placesList.appendChild(card);
        });
    }

    // Price filter event listener
    priceFilter.addEventListener('change', (event) => {
        const selected = event.target.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseInt(card.dataset.price, 10);
            if (selected === 'all') {
                card.style.display = 'block';
            } else {
                const maxPrice = parseInt(selected, 10);
                if (price <= maxPrice) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });
});