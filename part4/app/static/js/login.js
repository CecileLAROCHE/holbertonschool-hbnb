// part4/app/static/js/login.js
import { login, updateUserNav } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        try {
            // Login via auth.js (cookie + localStorage)
            await login(email, password);

            // Mise à jour du header
            updateUserNav();

            // Redirection vers l'accueil
            window.location.href = "index.html";

        } catch (error) {
            console.error("Login error:", error);
            document.getElementById("error-message").textContent =
                "Email ou mot de passe incorrect";
        }
    });
});
