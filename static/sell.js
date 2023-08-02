document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("sell-form");
    const sharesInput = document.getElementById("shares");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const sharesToSell = parseInt(sharesInput.value);
        const stockSymbol = document.getElementById("symbol").value;

        fetch('/sell', {
            method: 'POST',
            body: new URLSearchParams({
                'symbol': stockSymbol,
                'shares': sharesToSell
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                // Handle successful form submission here - redirect to home page
                console.log('Shares sold successfully.');
                alert('Shares sold successfully.');
                window.location.href = '/'; // Redirect to the homepage after successful sell
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