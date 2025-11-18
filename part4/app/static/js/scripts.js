document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorBox = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // Nettoyer les messages d’erreur
            if (errorBox) {
                errorBox.textContent = "";Unable to reach the login server.
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();

                    // Stocker le JWT dans un cookie
                    document.cookie = `token=${data.access_token}; path=/;`;

                    // Redirection
                    window.location.href = "index.html";
                } else {
                    const err = await response.json();
                    if (errorBox) {
                        errorBox.textContent = err.message || "Login failed.";
                    } else {
                        alert("Login failed.");
                    }
                }

            } catch (error) {
                console.error("Error during login:", error);
                if (errorBox) {
                    errorBox.textContent = "Unable to reach the login server.";
                } else {
                    alert("Unable to reach the server.");
                }
            }
        });
    }
});


