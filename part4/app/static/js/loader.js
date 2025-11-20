import { updateUserNav } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {

    // Charger le header
    fetch("./header.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("header").innerHTML = html;
            updateUserNav(); // 🔥 mettre à jour l'affichage utilisateur
        })
        .catch(err => console.error("Erreur chargement header:", err));

    // Charger le footer
    fetch("./footer.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("footer").innerHTML = html;
        })
        .catch(err => console.error("Erreur chargement footer:", err));
});
