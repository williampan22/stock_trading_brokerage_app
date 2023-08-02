document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("register-form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const username = usernameInput.value; 
        const password = passwordInput.value; 
        const confirmPassword = confirmPasswordInput.value;

        fetch('/register', {
            method: 'POST',
            body: new URLSearchParams({
                'username': username,
                'password': password,
                'confirm_password': confirmPassword
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                
                console.log('Registered Successfully.');
                alert('Registered Successfully.');
                window.location.href = '/login'; 
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