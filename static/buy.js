document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("buy-form");
    const sharesInput = document.getElementById("shares");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const sharesToBuy = parseInt(sharesInput.value);
        const stockSymbol = document.getElementById("symbol").value;

        fetch('/buy', {
            method: 'POST',
            body: new URLSearchParams({
                'symbol': stockSymbol,
                'shares': sharesToBuy
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                
                console.log('Shares bought successfully.');
                alert('Shares bought successfully.');
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