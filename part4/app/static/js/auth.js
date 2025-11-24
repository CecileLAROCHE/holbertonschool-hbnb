// part4/app/static/js/auth.js
import { API_BASE_URL } from "./api.js";

// -------------------------
// LOGIN
// -------------------------
export async function login(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Login failed.");
    }

    // Stocker le token et l'utilisateur dans le localStorage et cookie
    document.cookie = `token=${data.access_token}; path=/;`;
    if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
    }

    return data;
}

// -------------------------
// COOKIE UTILS
// -------------------------
export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

export function isAuthenticated() {
    return !!getCookie("token");
}

export function authHeader() {
    const token = getCookie("token");
    if (!token) return {};
    return { "Authorization": `Bearer ${token}` };
}

// -------------------------
// LOGOUT
// -------------------------
export function logout() {
    document.cookie = "token=; Max-Age=0; path=/";
    localStorage.removeItem("user");
}

// -------------------------
// GET CURRENT USER ID
// -------------------------
export function getCurrentUserId() {
    const user = JSON.parse(localStorage.getItem("user"));
    return user ? user.id : null;
}

// -------------------------
// UPDATE HEADER NAV
// -------------------------
export function updateUserNav() {
    const user = JSON.parse(localStorage.getItem("user"));
    const token = getCookie("token");

    const authLinks = document.getElementById("auth-links");
    const userInfo = document.getElementById("user-info");
    const userName = document.getElementById("user-name");
    const logoutBtn = document.getElementById("logout-btn");

    if (!authLinks || !userInfo || !userName) return;

    if (!token || !user) {
        // Non connecté
        authLinks.style.display = "block";
        userInfo.style.display = "none";
        return;
    }

    // Connecté
    authLinks.style.display = "none";
    userInfo.style.display = "block";
    userName.textContent = `👋 Bienvenue ${user.first_name} ${user.last_name}`;

    if (logoutBtn) {
        logoutBtn.onclick = () => {
            logout();
            updateUserNav(); // Met à jour le header après logout
        };
    }
}

// --- Patch pour anciens comptes ---
document.addEventListener("DOMContentLoaded", () => {
    const userStr = localStorage.getItem("user");
    if (!userStr) return; // pas d'utilisateur connecté

    let user;
    try {
        user = JSON.parse(userStr);
    } catch {
        console.warn("Ancien user corrompu, suppression...");
        localStorage.removeItem("user");
        return;
    }

    let changed = false;

    // Vérifie que chaque champ existe, sinon on complète
    if (!user.id) {
        user.id = "unknown-id"; // ou mettre l'id correct si tu le connais
        changed = true;
    }
    if (user.is_admin === undefined) {
        user.is_admin = false; // assume false pour anciens comptes
        changed = true;
    }
    if (!user.first_name) {
        user.first_name = "User";
        changed = true;
    }
    if (!user.last_name) {
        user.last_name = "";
        changed = true;
    }

    // si on a modifié, on réécrit dans localStorage
    if (changed) {
        localStorage.setItem("user", JSON.stringify(user));
        console.log("Patch appliqué sur ancien compte:", user);
    }
});

// Patch pour anciens comptes dans le localStorage
document.addEventListener("DOMContentLoaded", () => {
    const userStr = localStorage.getItem("user");
    if (!userStr) return; // pas d'utilisateur stocké

    let user;
    try {
        user = JSON.parse(userStr);
    } catch {
        console.warn("Ancien user corrompu, suppression...");
        localStorage.removeItem("user");
        return;
    }

    let changed = false;

    // Champs essentiels
    if (!user.id) {
        user.id = "unknown-id"; // ou mettre l'ID correct si possible
        changed = true;
    }
    if (user.is_admin === undefined) {
        user.is_admin = false;
        changed = true;
    }
    if (!user.first_name) {
        user.first_name = "User";
        changed = true;
    }
    if (!user.last_name) {
        user.last_name = "";
        changed = true;
    }

    // Stocke de nouveau si modifié
    if (changed) {
        localStorage.setItem("user", JSON.stringify(user));
        console.log("Patch appliqué sur ancien compte:", user);
    }
});

// -------------------------
// SYNC USER FROM API IF MISSING
// -------------------------
async function syncUserFromAPI() {
    const userStr = localStorage.getItem("user");
    if (!userStr) {  // si user non stocké
        try {
            const res = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: authHeader()
            });
            if (res.ok) {
                const user = await res.json();
                localStorage.setItem("user", JSON.stringify(user));
                console.log("localStorage.user synchronisé depuis /me :", user);
            }
        } catch (err) {
            console.warn("Impossible de synchroniser user:", err);
        }
    }
}

// Appel au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    syncUserFromAPI();
});
