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
                const response = await fetch('', {
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