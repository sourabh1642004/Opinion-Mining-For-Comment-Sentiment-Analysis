// script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const spinner = document.getElementById('loading-spinner');

    form.addEventListener('submit', function() {
        spinner.style.display = 'block';
    });

    window.addEventListener('load', function() {
        spinner.style.display = 'none';
    });
});