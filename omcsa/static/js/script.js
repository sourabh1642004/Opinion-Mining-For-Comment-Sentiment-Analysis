// script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const spinner = document.getElementById('loading-spinner');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        spinner.style.display = 'block';

        const formData = new FormData(form);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const taskId = data.task_id;
            checkTaskStatus(taskId);
        });
    });

    function checkTaskStatus(taskId) {
        fetch(`/task_status/${taskId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'SUCCESS') {
                spinner.style.display = 'none';
                // Handle the result here
                console.log(data.result);
            } else {
                setTimeout(() => checkTaskStatus(taskId), 1000);
            }
        });
    }

    window.addEventListener('load', function() {
        spinner.style.display = 'none';
    });
});