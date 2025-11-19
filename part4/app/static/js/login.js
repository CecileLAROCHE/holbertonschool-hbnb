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
            const data = await login(email, password);

            // Sauvegarder les infos utilisateur pour le header
            localStorage.setItem("user", JSON.stringify(data.user));

            updateUserNav(); // Mettre à jour le header directement

            // Redirection vers la page principale
            window.location.href = "index.html";

        } catch (error) {
            alert("Identifiants incorrects !");
            console.error(error);
        }
    });
});
