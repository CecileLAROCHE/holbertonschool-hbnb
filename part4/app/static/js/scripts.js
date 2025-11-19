document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const errorBox = document.getElementById("error-message");
    const welcomeBox = document.getElementById("welcome-message");

    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        // Nettoyage messages
        if (errorBox) errorBox.textContent = "";
        if (welcomeBox) welcomeBox.textContent = "";

        try {
            const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            // ❗ Correction : ton API renvoie "error", pas "message"
            if (!response.ok) {
                if (errorBox) errorBox.textContent = data.error || "Login failed.";
                return;
            }

            // 🔥 Affiche le message de bienvenue
            if (welcomeBox) {
                welcomeBox.textContent = `Bienvenue ${data.user.first_name} ${data.user.last_name}`;
            }

            // Stocker le JWT (OK)
            document.cookie = `token=${data.access_token}; path=/;`;

            // Redirection différée
            setTimeout(() => {
                window.location.href = "index.html";
            }, 1000);

        } catch (error) {
            console.error("Login error:", error);
            if (errorBox) errorBox.textContent = "Unable to reach the login server.";
        }
    });
});
