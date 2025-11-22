import { apiGet } from "./api.js";
import { authHeader, isAuthenticated } from "./auth.js";

// -------------------------
//     FETCH PLACES
// -------------------------
async function fetchPlaces() {
    try {
        const places = await apiGet("/places/", authHeader());
        window.allPlaces = places;
        displayPlaces(places);
    } catch (error) {
        console.error("Error fetching places:", error);
    }
}

// -------------------------
//     DISPLAY PLACES
// -------------------------
function displayPlaces(places) {
    const list = document.getElementById("places-container");
    list.innerHTML = "";

    places.forEach(place => {
        const placeDiv = document.createElement("div");
        placeDiv.classList.add("place-card");
        placeDiv.dataset.price = place.price;

        placeDiv.innerHTML = `
            <img src="${place.image_url || '../assets/default_place.png'}" 
                alt="${place.title}" 
                class="place-image">
            <h3>${place.title || "No name"}</h3>
            <p>${place.description}</p>
            <p><strong>Price:</strong> ${place.price}</p>
            <p><strong>Location:</strong> Lat ${place.latitude}, Lng ${place.longitude}</p>
            <a href="place.html?id=${place.id}" class="details-btn">View details</a>
        `;

        list.appendChild(placeDiv);
    });
}

// -------------------------
//     PRICE FILTER
// -------------------------
document.getElementById("price-filter").addEventListener("change", (event) => {
    const selected = event.target.value;
    const items = document.querySelectorAll(".place-card");

    items.forEach(item => {
        const price = parseFloat(item.dataset.price);

        if (selected === "all" || price <= parseFloat(selected)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
});

// -------------------------
//     INIT ON LOAD
// -------------------------
document.addEventListener("DOMContentLoaded", fetchPlaces);
