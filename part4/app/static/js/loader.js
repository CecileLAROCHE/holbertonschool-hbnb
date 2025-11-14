document.addEventListener("DOMContentLoaded", () => {
    // Charger le header
    fetch("header.html")
        .then(res => res.text())
        .then(html => document.getElementById("header").innerHTML = html);

    // Charger la nav
    fetch("nav.html")
        .then(res => res.text())
        .then(html => document.getElementById("header").innerHTML += html);

    // Charger le footer
    fetch("footer.html")
        .then(res => res.text())
        .then(html => document.getElementById("footer").innerHTML = html);
});
