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
