import { apiGet, apiDelete } from "./api.js";
import { authHeader, getCurrentUserId, isAuthenticated } from "./auth.js";

const urlParams = new URLSearchParams(window.location.search);
const placeId = urlParams.get("id");

// helper : safe set textContent if element exists
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? "";
}

// helper : get boolean isAdmin from stored user (no need to export from auth)
function isAdminLocal() {
    try {
        const user = JSON.parse(localStorage.getItem("user"));
        return !!(user && user.is_admin);
    } catch {
        return false;
    }
}

async function fetchPlaceDetails() {
    try {
        const place = await apiGet(`/places/${placeId}`, authHeader());
        if (!place) throw new Error("Place introuvable");

        displayPlace(place);
        displayOwnerActions(place);
        await fetchAndDisplayReviews();
        // show/hide upload form if owner
        const currentUser = getCurrentUserId();
        const uploadForm = document.getElementById("upload-image-form");
        if (uploadForm) {
            uploadForm.style.display = (isAuthenticated() && place.owner_id === currentUser) ? "block" : "none";
        }
    } catch (e) {
        console.error("Erreur GET place:", e);
        const info = document.getElementById("place-info") || document.getElementById("place-description");
        if (info) info.innerHTML = "<p style='color:red;'>Impossible de charger les détails du lieu.</p>";
    }
}

function displayPlace(place) {
    // safe updates (ne plante pas si l'élément est manquant)
    setText("place-title", place.title ?? "Untitled");
    setText("place-description", place.description ?? "No description");
    setText("place-price", place.price ? `${place.price} € / nuit` : "Prix non renseigné");
    setText("place-rating", place.average_rating ? `Rating: ${Number(place.average_rating).toFixed(1)}` : "No rating yet");

    const img = document.getElementById("place-image");
    if (img) {
        // backend peut renvoyer image, image_url ou image
        img.src = place.image_url || place.image || "/assets/default_place.png";
    }

    // amenities: try to render into #amenities-list if present
    const amList = document.getElementById("amenities-list");
    if (amList) {
        amList.innerHTML = "";
        const amenities = place.amenities ?? [];
        if (amenities.length === 0) {
            const li = document.createElement("li");
            li.textContent = "No amenities listed.";
            amList.appendChild(li);
        } else {
            amenities.forEach(a => {
                const li = document.createElement("li");
                // amenity may be string or object
                li.textContent = (typeof a === "string") ? a : (a.name ?? a.title ?? JSON.stringify(a));
                amList.appendChild(li);
            });
        }
    }
}

function displayOwnerActions(place) {
    const actions = document.getElementById("place-actions");
    if (!actions) return;
    actions.innerHTML = ""; // reset

    if (!isAuthenticated()) return;

    const userId = getCurrentUserId();
    const admin = isAdminLocal();

    // Delete button (owner or admin)
    if (place.owner_id === userId || admin) {
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "❌ Supprimer le lieu";
        deleteBtn.classList.add("btn", "btn-danger");
        deleteBtn.addEventListener("click", async () => {
            if (!confirm("Voulez-vous vraiment supprimer ce lieu ?")) return;
            try {
                const resp = await apiDelete(`/places/${placeId}`, authHeader());
                // apiDelete should throw on non-ok or return response — handle both
                alert("Lieu supprimé");
                window.location.href = "/index.html";
            } catch (e) {
                console.error("Erreur DELETE :", e);
                alert("Erreur lors de la suppression : " + (e.message || e));
            }
        });
        actions.appendChild(deleteBtn);
    }

    // Edit button (owner only)
    if (place.owner_id === userId) {
        const editBtn = document.createElement("button");
        editBtn.textContent = "✏️ Modifier le lieu";
        editBtn.classList.add("btn");
        // TODO: ajouter la navigation vers la page d'édition si tu l'as
        editBtn.addEventListener("click", () => {
            window.location.href = `/edit_place.html?id=${placeId}`;
        });
        actions.appendChild(editBtn);
    }
}

async function fetchAndDisplayReviews() {
    try {
        const reviews = await apiGet(`/places/${placeId}/reviews/`, authHeader());
        displayReviews(reviews || []);
    } catch (e) {
        console.error("Erreur GET reviews:", e);
        const container = document.getElementById("reviews-container");
        if (container) container.innerHTML = "<p style='color:red;'>Impossible de charger les avis.</p>";
    }
}

// ---------------------- Reviews UI ----------------------
function displayReviews(reviews) {
    const container = document.getElementById("reviews-container") || document.getElementById("reviews-list");
    if (!container) return;
    container.innerHTML = "";

    if (!reviews || reviews.length === 0) {
        container.innerHTML = "<p>No reviews yet.</p>";
        return;
    }

    const userId = getCurrentUserId();
    const admin = isAdminLocal();

    reviews.forEach(review => {
        const div = document.createElement("div");
        div.classList.add("review-item");

        // tolerate backend field differences
        const rating = review.rating ?? review.rate ?? "N/A";
        const text = review.text ?? review.comment ?? "";
        const created = review.created_at ?? review.createdAt ?? review.created ?? null;
        const userObj = review.user ?? null;
        const userName = userObj ? (userObj.first_name ? `${userObj.first_name} ${userObj.last_name ?? ""}` : (userObj.username ?? userObj.email ?? "User")) : (review.user_name ?? review.user_name ?? "Unknown");

        div.innerHTML = `
            <p><strong>${escapeHtml(userName)}</strong> <small>${created ? new Date(created).toLocaleDateString() : ""}</small></p>
            <p>⭐ ${rating}</p>
            <p>${escapeHtml(text)}</p>
        `;

        // actions
        if (review.user_id === userId || admin) {
            const actions = document.createElement("div");
            actions.classList.add("review-actions");

            // delete
            const deleteR = document.createElement("button");
            deleteR.textContent = "🗑️";
            deleteR.title = "Supprimer";
            deleteR.addEventListener("click", async () => {
                if (!confirm("Supprimer cet avis ?")) return;
                try {
                    await apiDelete(`/places/${placeId}/reviews/${review.id}`, authHeader());
                    await fetchAndDisplayReviews();
                } catch (e) {
                    console.error("Erreur suppression review:", e);
                    alert("Impossible de supprimer l'avis");
                }
            });
            actions.appendChild(deleteR);

            // edit if owner
            if (review.user_id === userId) {
                const editR = document.createElement("button");
                editR.textContent = "✏️";
                editR.title = "Modifier";
                editR.addEventListener("click", () => openEditReviewUI(review));
                actions.appendChild(editR);
            }

            div.appendChild(actions);
        }

        container.appendChild(div);
    });
}

// small helper to avoid XSS
function escapeHtml(unsafe) {
    if (unsafe == null) return "";
    return String(unsafe)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

// placeholder edit UI (simple prompt); you can replace with modal
function openEditReviewUI(review) {
    const newText = prompt("Modifier votre commentaire :", review.text ?? review.comment ?? "");
    if (newText == null) return;
    const newRating = prompt("Nouvelle note (1-5) :", review.rating ?? review.rate ?? 5);
    // call API to update review if you have endpoint, example:
    (async () => {
        try {
            // assuming a PUT /reviews/<id> exists
            await fetch(`/api/v1/reviews/${review.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json", ...authHeader() },
                body: JSON.stringify({ rating: Number(newRating), text: newText })
            });
            await fetchAndDisplayReviews();
        } catch (e) {
            console.error("Erreur updating review:", e);
            alert("Erreur lors de la modification");
        }
    })();
}

// init
fetchPlaceDetails();

// --- Add Review Button ---
const addReviewBtn = document.getElementById("add-review-btn");
if (addReviewBtn) {
    addReviewBtn.addEventListener("click", () => {
        // Redirige vers add_review.html en passant l'ID du lieu
        window.location.href = `/add_review.html?place_id=${placeId}`;
    });
}

