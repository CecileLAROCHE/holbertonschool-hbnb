import { apiGet, apiPost } from "./api.js";
import { authHeader, getUserId, isAuthenticated } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    // Vérifier que l'utilisateur est connecté
    if (!isAuthenticated()) {
        window.location.href = "/index.html";
        return;
    }

    const form = document.getElementById("add-place-form");
    const placesContainer = document.getElementById("places-list");

    // Ajouter un message quand aucune place n'existe
    const noPlacesMsg = document.createElement("p");
    noPlacesMsg.id = "no-places-msg";
    noPlacesMsg.textContent = "Vous n'avez encore aucune place.";
    noPlacesMsg.style.display = "none";
    placesContainer.appendChild(noPlacesMsg);

    // Ajouter une nouvelle place
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            title: document.getElementById("name").value,
            description: document.getElementById("description").value,
            latitude: parseFloat(document.getElementById("latitude").value),
            longitude: parseFloat(document.getElementById("longitude").value),
            price: parseFloat(document.getElementById("price").value),
            owner_id: getUserId() // Assure que l'API sait quel user crée la place
        };

        try {
            await apiPost("/places/", data, authHeader());
            // Refresh de la liste des places
            loadPlaces();
            form.reset();
        } catch (err) {
            console.error("Erreur lors de l'ajout de la place:", err);
            alert("Erreur lors de l'ajout de la place. Vérifiez vos données.");
        }
    });

    // Fonction pour afficher les infos du user
    async function loadUserInfo() {
        try {
            const userId = getUserId();
            const user = await apiGet(`/users/${userId}`, authHeader());
            document.getElementById("user-info").textContent = 
                `Email: ${user.email} - Nom: ${user.first_name} ${user.last_name}`;
        } catch (err) {
            console.error("Erreur lors du chargement des infos utilisateur:", err);
        }
    }

    // Fonction pour afficher les places du user
    async function loadPlaces() {
        try {
            const userId = getUserId();
            const places = await apiGet(`/users/${userId}/places`, authHeader());
            
            // Vider le container sauf le message
            placesContainer.querySelectorAll(".place-card").forEach(el => el.remove());

            if (places.length === 0) {
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
                    `;
                    placesContainer.appendChild(div);
                });
            }
        } catch (err) {
            console.error("Erreur lors du chargement des places:", err);
        }
    }

    // Initialisation
    loadUserInfo();
    loadPlaces();
});
