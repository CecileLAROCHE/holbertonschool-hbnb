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
            const user = await apiGet(`/users/me`, authHeader());
            document.getElementById("user-info").textContent =
                `${user.first_name} ${user.last_name}`;
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
                        Latitude: ${place.latitude}, Longitude: ${place.longitude}<br>
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
    if (form) {
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
                await loadPlaces();
            } catch (err) {
                console.error("Erreur lors de l'ajout de la place:", err);
                alert("Erreur lors de l'ajout de la place. Vérifiez vos données.");
            }
        });
    }

    // -----------------------------
    // Fetch user reviews (/reviews/me)
    // -----------------------------
    async function fetchUserReviews() {
        const container = document.getElementById("review-list");
        const emptyMsg = document.getElementById("no-reviews-msg");

        if (!container) return; // page sans reviews

        try {
            const reviews = await apiGet("/reviews/me", authHeader());
            displayUserReviews(reviews);
        } catch (error) {
            console.error("Erreur lors de la récupération des reviews :", error);
            container.innerHTML = `<p class="error">Erreur lors de la récupération des avis.</p>`;
        }
    }

    // -----------------------------
    // Display reviews
    // -----------------------------
    function displayUserReviews(reviews) {
        const container = document.getElementById("review-list");
        const emptyMsg = document.getElementById("no-reviews-msg");

        if (!reviews || reviews.length === 0) {
            emptyMsg.style.display = "block";
            container.innerHTML = "";
            return;
        }

        emptyMsg.style.display = "none";
        container.innerHTML = "";

        reviews.forEach((review) => {
            const div = document.createElement("div");
            div.classList.add("review-card");

            div.innerHTML = `
                <h3>Place: ${review.place_title || "Unknown"}</h3>
                <p><strong>Rating:</strong> ${review.rating}/5</p>
                <p>${review.text}</p>
            `;

            container.appendChild(div);
        });
    }

    // -----------------------------
    // Initialisation
    // -----------------------------
    loadUserInfo();
    loadPlaces();
    fetchUserReviews();  // charge les reviews si la page en contient
});
