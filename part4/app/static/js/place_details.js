import { apiGet } from "./api.js";
import { isAuthenticated, authHeader } from "./auth.js";

// -------------------------
// Helpers
// -------------------------

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function getCurrentUser() {
    const token = getCookie('token');
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return { id: payload.sub, is_admin: payload.is_admin };
}

// -------------------------
// Display Functions
// -------------------------

function displayPlaceDetails(place) {

    // Image
    const placeImage = document.getElementById("place-image");
    if (place.image_url) {
        placeImage.src = place.image_url;
    } else {
        placeImage.src = "assets/default_place.png";
    }

    // Title, description, price, owner, location
    document.getElementById('place-title').textContent = place.title;
    document.getElementById('place-description').textContent = place.description;
    document.getElementById('place-price').textContent = place.price;
    // Owner
    const owner = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : "Unknown";
    document.getElementById('place-owner').textContent = owner;
    // Location
    const location = `Lat ${place.latitude}, Lng ${place.longitude}`;
    document.getElementById('place-location').textContent = location;

    // Amenities
    const amenitiesList = document.getElementById('amenities-list');
    amenitiesList.innerHTML = "";
    if (place.amenities?.length > 0) {
        place.amenities.forEach(a => {
            const li = document.createElement('li');
            li.textContent = a.name;
            amenitiesList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = "No amenities listed";
        amenitiesList.appendChild(li);
    }

    // Reviews
    displayReviews(place.reviews);
}

function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-container');
    reviewsContainer.innerHTML = "";
    const currentUser = getCurrentUser();

    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
        return;
    }

    reviews.forEach(r => {
        const div = document.createElement('div');
        div.className = 'review-card';

        div.innerHTML = `
            <p><strong>${r.user ? r.user.first_name + " " + r.user.last_name : "Unknown"}</strong></p>
            <p>${r.text}</p>
            <small>${r.rating} ★</small>
            <div class="review-actions"></div>
        `;

        const actions = div.querySelector(".review-actions");

        // Delete button: owner of review or admin
        if (currentUser && (currentUser.is_admin || r.user_id === currentUser.id)) {
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Supprimer";
            deleteBtn.classList.add("btn-danger");
            deleteBtn.addEventListener("click", () => deleteReview(r.id));
            actions.appendChild(deleteBtn);
        }

        // Edit button: only owner
        if (currentUser && r.user_id === currentUser.id) {
            const editBtn = document.createElement("button");
            editBtn.textContent = "Modifier";
            editBtn.classList.add("btn-edit");
            editBtn.addEventListener("click", () => editReview(r, getPlaceIdFromURL()));
            actions.appendChild(editBtn);
        }

        reviewsContainer.appendChild(div);
    });
}

// -------------------------
// Actions
// -------------------------

async function deleteReview(reviewId) {
    if (!confirm("Supprimer cet avis ?")) return;

    try {
        const response = await fetch(`/api/v1/reviews/${reviewId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                ...authHeader()
            }
        });

        if (!response.ok) throw new Error("Erreur " + response.status);

        alert("Avis supprimé !");
        location.reload();
    } catch (error) {
        console.error("Erreur delete review:", error);
        alert("❌ Impossible de supprimer l'avis !");
    }
}

function editReview(review, placeId) {
    // Rediriger vers add_review.html en mode édition si besoin
    window.location.href = `add_review.html?id=${placeId}&edit=${review.id}`;
}

// -------------------------
// Main
// -------------------------

document.addEventListener("DOMContentLoaded", async () => {
    const placeId = getPlaceIdFromURL();
    const addReviewBtn = document.getElementById("add-review-btn");

    if (!placeId) {
        alert("ID du lieu manquant. Retour à l'accueil.");
        window.location.href = "index.html";
        return;
    }

    try {
        const place = await apiGet(`/places/${placeId}`, authHeader());
        displayPlaceDetails(place);

        const currentUser = getCurrentUser();

        // Afficher bouton Add Review seulement pour users non propriétaires
        if (!isAuthenticated() || currentUser.id === place.owner_id) {
            addReviewBtn.style.display = "none";
        } else {
            addReviewBtn.addEventListener("click", () => {
                window.location.href = `add_review.html?id=${placeId}`;
            });
        }
    } catch (error) {
        console.error("❌ Impossible de charger le lieu :", error);
        alert("Erreur lors du chargement du lieu.");
    }
});
