document.addEventListener('DOMContentLoaded', function() {
    const navbarToggle = document.getElementById('navbar-toggle');
    const navbarLinks = document.getElementById('navbar-links');

    navbarToggle.addEventListener('click', function() {
        navbarLinks.classList.toggle('active');
    });
});


function redirectDiscord() {
    window.location.href = "https://www.example.com";
}