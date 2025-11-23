import { apiGet, apiPost } from "./api.js";
import { authHeader, isAuthenticated } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    // Vérifier que l'utilisateur est connecté
    if (!isAuthenticated()) {
        window.location.href = "/index.html";
        return;
    }

    const form = document.getElementById("add-place-form");
    const placesContainer = document.getElementById("places-list");
    const noPlacesMsg = document.getElementById("no-places-msg");

    // -----------------------------
    // Charger les infos utilisateur
    // -----------------------------
    async function loadUserInfo() {
        try {
            const user = await apiGet(`/users/me`, authHeader()); // optionnel si tu veux afficher l'email
            document.getElementById("user-info").textContent = 
                `${user.first_name} ${user.last_name} `;
        } catch (err) {
            console.error("Erreur lors du chargement des infos utilisateur:", err);
        }
    }

    // -----------------------------
    // Charger les places de l'utilisateur
    // -----------------------------
    async function loadPlaces() {
        try {
            const places = await apiGet(`/users/me/places`, authHeader());

            // Vider le container sauf le message
            placesContainer.querySelectorAll(".place-card").forEach(el => el.remove());

            if (!places || places.length === 0) {
                noPlacesMsg.style.display = "block";
            } else {
                noPlacesMsg.style.display = "none";

                places.forEach(place => {
                    const div = document.createElement("div");
                    div.className = "place-card";
                    div.innerHTML = `
                        <strong>${place.title}</strong><br>
                        ${place.description || ''}<br>
                        Prix: €${place.price.toFixed(2)}<br>
                        Latitude: ${place.latitude}, Longitude: ${place.longitude}
                        <a href="place.html?id=${place.id}">Voir détails</a>
                    `;
                    placesContainer.appendChild(div);
                });
            }
        } catch (err) {
            console.error("Erreur lors du chargement des places:", err);
            noPlacesMsg.textContent = "Erreur lors de la récupération des places.";
            noPlacesMsg.style.display = "block";
        }
    }

    // -----------------------------
    // Ajouter une nouvelle place
    // -----------------------------
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            title: document.getElementById("name").value,
            description: document.getElementById("description").value,
            latitude: parseFloat(document.getElementById("latitude").value),
            longitude: parseFloat(document.getElementById("longitude").value),
            price: parseFloat(document.getElementById("price").value)
        };

        try {
            await apiPost("/places/", data, authHeader());
            form.reset();
            await loadPlaces(); // rafraîchir la liste après ajout
        } catch (err) {
            console.error("Erreur lors de l'ajout de la place:", err);
            alert("Erreur lors de l'ajout de la place. Vérifiez vos données.");
        }
    });

    // -----------------------------
    // Initialisation
    // -----------------------------
    loadUserInfo();
    loadPlaces();
});
