
document.addEventListener('DOMContentLoaded', () => {
    // ---------- Helper: get cookie ----------
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return null;
    }

    // ---------- Login form handling (only on login page) ----------
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error-message');

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    const msg = data.message || 'Login failed. Check credentials.';
                    if (errorDiv) errorDiv.textContent = msg;
                    else alert(msg);
                }
            } catch (error) {
                console.error('Login error:', error);
                const msg = 'Network error. Please try again.';
                if (errorDiv) errorDiv.textContent = msg;
                else alert(msg);
            }
        });
    }

    // ---------- Index page handling (list of places) ----------
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');
    const placesList = document.getElementById('places-list');

    if (loginLink || priceFilter || placesList) {
        const token = getCookie('token');

        // Show/hide login link
        if (loginLink) {
            loginLink.style.display = token ? 'none' : 'inline-block';
        }

        // If token exists and we have a places list, fetch places
        if (token && placesList) {
            fetchPlaces(token);
        } else if (!token && placesList) {
            placesList.innerHTML = '<p>Please log in to view places.</p>';
        }

        // Populate price filter dropdown
        if (priceFilter) {
            const options = [10, 50, 100, 'All'];
            priceFilter.innerHTML = '';
            options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt === 'All' ? 'all' : opt;
                option.textContent = opt === 'All' ? 'All' : `$${opt}`;
                priceFilter.appendChild(option);
            });
        }

        // Fetch places function
        async function fetchPlaces(token) {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const places = await response.json();
                displayPlaces(places);
            } catch (error) {
                console.error('Fetch error:', error);
                placesList.innerHTML = `<p>Error loading places: ${error.message}</p>`;
            }
        }

        // Display places as cards (using 'title' from API)
        function displayPlaces(places) {
            placesList.innerHTML = '';

            if (!places || places.length === 0) {
                placesList.innerHTML = '<p>No places available.</p>';
                return;
            }

            places.forEach(place => {
                const card = document.createElement('div');
                card.className = 'place-card';
                card.dataset.price = place.price;

                // Placeholder image (API has no image field)
                const img = document.createElement('img');
                img.src = 'images/placeholder.jpg';
                img.alt = place.title;
                img.className = 'place-image';
                img.onerror = () => { img.src = 'images/placeholder.jpg'; };
                card.appendChild(img);

                const info = document.createElement('div');
                info.className = 'place-info';

                const name = document.createElement('h3');
                name.textContent = place.title;
                info.appendChild(name);

                const price = document.createElement('p');
                price.className = 'price';
                price.innerHTML = `Price per night: <span>$${place.price}</span>`;
                info.appendChild(price);

                const btn = document.createElement('button');
                btn.className = 'details-button';
                btn.textContent = 'View Details';
                btn.onclick = () => { window.location.href = `place.html?id=${place.id}`; };
                info.appendChild(btn);

                card.appendChild(info);
                placesList.appendChild(card);
            });
        }

        // Price filter event listener
        if (priceFilter) {
            priceFilter.addEventListener('change', (e) => {
                const selected = e.target.value;
                const cards = document.querySelectorAll('.place-card');
                cards.forEach(card => {
                    const price = parseInt(card.dataset.price, 10);
                    if (selected === 'all' || price <= parseInt(selected, 10)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
    }

    // ---------- Place details page handling ----------
    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');
        const addReviewSection = document.getElementById('add-review');

        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        } else {
            placeDetailsSection.innerHTML = '<p>Invalid place ID.</p>';
        }
    }

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });

            if (!response.ok) {
                throw new Error(`Failed to fetch place details: ${response.status}`);
            }

            const place = await response.json();
            displayPlaceDetails(place);

            // Fetch reviews for this place
            fetchReviews(placeId, token);
        } catch (error) {
            console.error('Error fetching place details:', error);
            placeDetailsSection.innerHTML = `<p>Error loading place details: ${error.message}</p>`;
        }
    }

    function displayPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        // API provides: id, title, description, price, latitude, longitude, owner_id
        // No host name or amenities; we show what's available.
        const hostDisplay = place.owner_id ? `Owner ID: ${place.owner_id}` : 'Unknown host';
        const amenitiesDisplay = 'Not provided'; // Amenities not in API

        placeDetails.innerHTML = `
            <h1>${place.title}</h1>
            <div class="place-info">
                <p><strong>Host:</strong> ${hostDisplay}</p>
                <p><strong>Price per night:</strong> $${place.price}</p>
                <p><strong>Description:</strong> ${place.description || 'No description'}</p>
                <p><strong>Amenities:</strong> ${amenitiesDisplay}</p>
            </div>
        `;
    }

    async function fetchReviews(placeId, token) {
        try {
            const headers = {};
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}`, { headers });

            if (!response.ok) {
                if (response.status === 404) {
                    displayReviews([]);
                    return;
                }
                throw new Error(`Failed to fetch reviews: ${response.status}`);
            }

            const reviews = await response.json();
            displayReviews(reviews);
        } catch (error) {
            console.error('Error fetching reviews:', error);
            const reviewsSection = document.getElementById('reviews');
            if (reviewsSection) {
                reviewsSection.innerHTML = '<h2>Reviews</h2><p>Error loading reviews.</p>';
            }
        }
    }

    function displayReviews(reviews) {
        const reviewsSection = document.getElementById('reviews');
        if (!reviewsSection) return;

        reviewsSection.innerHTML = '<h2>Reviews</h2>';

        const reviewsList = document.createElement('div');
        reviewsList.className = 'reviews-list';

        if (!reviews || reviews.length === 0) {
            reviewsList.innerHTML = '<p>No reviews yet.</p>';
        } else {
            reviews.forEach(review => {
                const card = document.createElement('div');
                card.className = 'review-card';

                // API returns: id, text, user_id, place_id
                // We need to display comment, user name, and rating.
                // Since rating is missing from your model, we use a default (0).
                // You must add rating to your review model and include it in the response.
                const reviewText = review.text || '';
                const userId = review.user_id || 'Anonymous';
                const rating = review.rating || 0;  // Assume rating exists; if not, 0 stars.

                // Optional: fetch user name by user_id if you have a user endpoint
                // For now, show user_id as identifier.
                card.innerHTML = `
                    <p class="review-text">${reviewText}</p>
                    <p class="review-user"><strong>User ID: ${userId}</strong></p>
                    <p class="review-rating">${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</p>
                `;
                reviewsList.appendChild(card);
            });
        }
        reviewsSection.appendChild(reviewsList);
    }
});