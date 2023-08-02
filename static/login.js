document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("login-form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const username = usernameInput.value; 
        const password = passwordInput.value; 

        fetch('/login', {
            method: 'POST',
            body: new URLSearchParams({
                'username': username,
                'password': password
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Login Successful.');
                alert('Login Successful.');
                window.location.href = '/';
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data.error) {
                errorMessage.textContent = data.error;
                errorMessage.style.display = "block";
            } else {
                errorMessage.style.display = "none";
            }
        })
        .catch(error => {
            console.error('Error occurred:', error);
        });
    });
});
