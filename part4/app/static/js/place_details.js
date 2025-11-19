import { apiGet } from "./api.js";
import { isAuthenticated, authHeader } from "./auth.js";

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

const placeId = getPlaceIdFromURL();
const addReviewSection = document.getElementById('add-review');

document.addEventListener("DOMContentLoaded", async () => {

    // Affichage ou non de la section pour ajouter un avis
    addReviewSection.style.display = isAuthenticated() ? 'block' : 'none';

    try {
        const place = await apiGet(`/places/${placeId}`, authHeader());
        displayPlaceDetails(place);

    } catch (error) {
        console.error("❌ Impossible de charger le lieu :", error);
        document.getElementById('place-details').innerHTML =
            "<p style='color:red;'>Erreur lors du chargement des détails du lieu.</p>";
    }
});


function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = "";  // Nettoyage avant affichage

    const nameEl = document.createElement('h2');
    nameEl.textContent = place.name;

    const descEl = document.createElement('p');
    descEl.textContent = place.description;

    const priceEl = document.createElement('p');
    priceEl.textContent = `Price: ${place.price_by_night} € per night`;

    const amenitiesEl = document.createElement('ul');
    amenitiesEl.innerHTML = "<strong>Amenities:</strong>";
    place.amenities?.forEach(a => {
        const li = document.createElement('li');
        li.textContent = a.name;
        amenitiesEl.appendChild(li);
    });

    const reviewsEl = document.createElement('div');
    reviewsEl.innerHTML = "<h3>Reviews:</h3>";
    place.reviews?.forEach(r => {
        const p = document.createElement('p');
        p.textContent = `⭐ ${r.rating}/5 - ${r.text}`;
        reviewsEl.appendChild(p);
    });

    detailsSection.append(nameEl, descEl, priceEl, amenitiesEl, reviewsEl);
}
