import { apiGet } from "./api.js";
import { isAuthenticated, authHeader } from "./auth.js";

// Récupère l'ID du lieu depuis l'URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// Récupère l'ID de l'utilisateur courant depuis le JWT
function getCurrentUserId() {
    const token = getCookie('token');
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub;
}

// Vérifie si l'utilisateur est admin
function checkIfAdmin() {
    const token = getCookie('token');
    if (!token) return false;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.is_admin;
}

// Helper cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
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
        const li = document.createElement('li');
        li.textContent = "No amenities listed.";
        amenitiesEl.appendChild(li);
    }

    detailsSection.append(nameEl, descEl, priceEl, amenitiesEl);

    // Bouton delete si owner ou admin
    const currentUserId = getCurrentUserId();
    const isAdmin = checkIfAdmin();
    if (currentUserId === place.owner_id || isAdmin) {
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = "Supprimer le lieu";
        deleteBtn.classList.add('btn', 'btn-danger');
        deleteBtn.style.marginTop = "10px";

        deleteBtn.addEventListener('click', async () => {
            if (!confirm("Voulez-vous vraiment supprimer ce lieu ?")) return;

            try {
                const response = await fetch(`/api/v1/places/${place.id}`, {
                    method: 'DELETE',
                    headers: { ...authHeader() },
                    credentials: 'include'
                });

                let data = {};
                try {
                    data = await response.json();
                } catch (_) {}

                if (!response.ok) {
                    console.error("Erreur DELETE backend:", data);
                    throw new Error(data.message || `Erreur ${response.status}`);
                }

                alert("Lieu supprimé !");
                window.location.href = "index.html";

            } catch (error) {
                console.error("❌ Impossible de supprimer le lieu :", error);
                alert("❌ Impossible de supprimer le lieu : " + error.message);
            }
        });

        detailsSection.appendChild(deleteBtn);
    }

    const reviewsEl = document.getElementById('reviews');
    reviewsEl.innerHTML = "<h3>Reviews:</h3>";
    if (place.reviews?.length > 0) {
        place.reviews.forEach(r => {
            const p = document.createElement('p');
            p.textContent = `⭐ ${r.rating}/5 - ${r.text}`;
            reviewsEl.appendChild(p);
        });
    } else {
        const p = document.createElement('p');
        p.textContent = "No reviews yet.";
        reviewsEl.appendChild(p);
    }
}

// Script principal
document.addEventListener("DOMContentLoaded", async () => {
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (!placeId) {
        document.getElementById('place-details').innerHTML =
            "<p style='color:red;'>ID du lieu manquant dans l'URL.</p>";
        return;
    }

    try {
        const place = await apiGet(`/places/${placeId}`, authHeader());
        displayPlaceDetails(place);

        const currentUserId = getCurrentUserId();

        if (!isAuthenticated()) {
            addReviewSection.style.display = 'none';
        } else if (currentUserId === place.owner_id) {
            addReviewSection.innerHTML = "<p>Vous êtes le propriétaire de ce lieu, vous ne pouvez pas laisser d’avis.</p>";
            addReviewSection.style.display = 'block';
        } else {
            addReviewSection.style.display = 'block';
            const reviewForm = document.getElementById('review-form');

            if (reviewForm) {
                reviewForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const rating = reviewForm.querySelector('input[name="rating"]').value;
                    const text = reviewForm.querySelector('textarea[name="review-text"]').value;

                    try {
                        const response = await fetch(`/api/v1/places/${placeId}/reviews/`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', ...authHeader() },
                            body: JSON.stringify({ rating, text })
                        });

                        if (!response.ok) throw new Error(`Erreur ${response.status}`);

                        const updatedPlace = await apiGet(`/places/${placeId}`, authHeader());
                        displayPlaceDetails(updatedPlace);
                        reviewForm.reset();

                    } catch (error) {
                        console.error("❌ Impossible d'ajouter l'avis :", error);
                        alert("❌ Impossible d'ajouter l'avis : " + error.message);
                    }
                });
            }
        }

    } catch (error) {
        console.error("❌ Impossible de charger le lieu :", error);
        document.getElementById('place-details').innerHTML =
            "<p style='color:red;'>Erreur lors du chargement des détails du lieu.</p>";
    }
});
