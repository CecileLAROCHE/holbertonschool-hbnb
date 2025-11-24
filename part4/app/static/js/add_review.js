function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        alert("Vous devez être connecté pour ajouter un avis.");
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function getCurrentUserId(token) {
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub;
}

async function submitReview(token, placeId, userId, reviewText, ratingValue) {
    try {
        const response = await fetch(`/api/v1/reviews/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: ratingValue,
                place_id: placeId,
                user_id: userId
            })
        });
        await handleResponse(response, placeId);
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Erreur réseau lors de la soumission de la review.");
    }
}

async function handleResponse(response, placeId) {
    if (response.ok) {
        alert("Review soumise avec succès !");
        window.location.href = `place.html?id=${placeId}`;
    } else {
        try {
            const data = await response.json();
            alert("Erreur: " + (data.error || data.message || "Impossible de soumettre la review"));
        } catch (e) {
            alert("Erreur lors de la soumission de la review");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const token = checkAuthentication();
    if (!token) return;

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert("ID du lieu manquant. Retour à l'accueil.");
        window.location.href = "index.html";
        return;
    }

    const userId = getCurrentUserId(token);
    const reviewForm = document.getElementById("review-form");
    if (!reviewForm) return;

    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById("review").value.trim();
        const ratingValue = parseInt(document.getElementById("rating").value, 10);

        if (!reviewText) {
            alert("Veuillez écrire un commentaire avant de soumettre !");
            return;
        }

        if (!ratingValue || ratingValue < 1 || ratingValue > 5) {
            alert("Veuillez sélectionner une note valide !");
            return;
        }

        const submitButton = reviewForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        await submitReview(token, placeId, userId, reviewText, ratingValue);

        submitButton.disabled = false;
    });
});
