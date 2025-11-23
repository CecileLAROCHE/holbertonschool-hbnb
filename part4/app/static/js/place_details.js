import { apiGet } from "./api.js";
import { isAuthenticated, authHeader } from "./auth.js";

// Helper cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Récupère place_id depuis l'URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

// Récupère l'utilisateur courant depuis le JWT
function getCurrentUserId() {
    const token = getCookie('token');
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub;
}

function checkIfAdmin() {
    const token = getCookie('token');
    if (!token) return false;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.is_admin;
}

// Affiche les détails du lieu
function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = "";

    const nameEl = document.createElement('h2');
    nameEl.textContent = place.title;

    const descEl = document.createElement('p');
    descEl.textContent = place.description;

    const priceEl = document.createElement('p');
    priceEl.textContent = `Price: ${place.price} € per night`;

    const amenitiesEl = document.createElement('ul');
    amenitiesEl.innerHTML = "<strong>Amenities:</strong>";

    if (place.amenities?.length > 0) {
        place.amenities.forEach(a => {
            const li = document.createElement('li');
            li.textContent = a.name;
            amenitiesEl.appendChild(li);
        });
    } else {
        amenitiesEl.innerHTML += "<li>No amenities listed.</li>";
    }

    detailsSection.append(nameEl, descEl, priceEl, amenitiesEl);

    // Reviews
    const reviewsEl = document.getElementById('reviews');
    reviewsEl.innerHTML = "<h3>Reviews:</h3>";

    if (place.reviews?.length > 0) {
        place.reviews.forEach(r => {
            const p = document.createElement('p');
            p.textContent = `⭐ ${r.rating}/5 - ${r.text}`;
            reviewsEl.appendChild(p);
        });
    } else {
        reviewsEl.innerHTML += "<p>No reviews yet.</p>";
    }
}

// Main
document.addEventListener("DOMContentLoaded", async () => {
    const placeId = getPlaceIdFromURL();
    const addReviewBtn = document.getElementById("add-review-btn");
    const addReviewSection = document.getElementById("add-review");

    if (!placeId) {
        document.getElementById('place-details').innerHTML =
            "<p style='color:red;'>ID du lieu manquant dans l'URL.</p>";
        return;
    }

    try {
        const place = await apiGet(`/places/${placeId}`, authHeader());
        displayPlaceDetails(place);

        const currentUserId = getCurrentUserId();

        // Gestion affichage formulaire selon user
        if (!isAuthenticated()) {
            addReviewSection.style.display = 'none';
        } else if (currentUserId === place.owner_id) {
            addReviewSection.innerHTML = "<p>Vous êtes le propriétaire, vous ne pouvez pas laisser d’avis.</p>";
        } else {
            addReviewBtn.addEventListener("click", () => {
                window.location.href = `/add_review.html?id=${placeId}`;
            });
        }
    } catch (error) {
        console.error("❌ Impossible de charger le lieu :", error);
        document.getElementById('place-details').innerHTML =
            "<p style='color:red;'>Erreur lors du chargement du lieu.</p>";
    }
});
