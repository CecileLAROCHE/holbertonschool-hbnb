import { updateUserNav } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    
    // Charger le header
    fetch("part4/app/templates/header.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("header").innerHTML = html;
            updateUserNav(); // 🔥 mettre à jour l'affichage utilisateur
        });

    // Charger la nav
    fetch("part4/app/templates/nav.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("nav").innerHTML = html;
        });

    // Charger le footer
    fetch("part4/app/templates/footer.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("footer").innerHTML = html;
        });
});
