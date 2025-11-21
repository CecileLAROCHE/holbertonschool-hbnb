import { apiPost } from "./api.js";
import { updateUserNav } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Récupération des valeurs du formulaire
        const first_name = document.getElementById("first_name").value.trim();
        const last_name = document.getElementById("last_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        try {
            // Appel de l'API pour créer l'utilisateur
            const newUser = await apiPost("/users", {
                first_name,
                last_name,
                email,
                password,
                is_admin: false
            });

            alert("Compte créé avec succès !");

            // Sauvegarde du nouvel utilisateur pour le header
            localStorage.setItem("user", JSON.stringify(newUser));

            // Mise à jour du header
            updateUserNav();

            // Redirection vers la page principale
            window.location.href = "index.html";

        } catch (error) {
            document.getElementById("error-message").textContent =
                "Erreur : utilisateur déjà existant ou données invalides";
            console.error("Sign up error:", error);
        }
    });
});
