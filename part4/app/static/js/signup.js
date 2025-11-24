// part4/app/static/js/signup.js
import { apiPost } from "./api.js";
import { login, updateUserNav } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const first_name = document.getElementById("first_name").value.trim();
        const last_name = document.getElementById("last_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        try {
            // 1️⃣ Création de l'utilisateur
            await apiPost("/users", {
                first_name,
                last_name,
                email,
                password,
                is_admin: false
            });

            // 2️⃣ Login automatique
            await login(email, password); // stocke cookie et localStorage correctement

            // 3️⃣ Mise à jour du header
            updateUserNav();

            // 4️⃣ Redirection vers l'accueil
            window.location.href = "index.html";

        } catch (error) {
            console.error("Sign up error:", error);
            const errorEl = document.getElementById("error-message");
            if (errorEl) {
                errorEl.textContent =
                    "Erreur : utilisateur déjà existant ou données invalides";
            }
        }
    });
});
