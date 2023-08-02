document.addEventListener("DOMContentLoaded", function() {
    const sellForm = document.getElementById("sell-form");
    const buyForm = document.getElementById("buy-form");
    const sellSharesInput = document.getElementById("sell-shares"); // Change "sharesInput" to "sellSharesInput"
    const buySharesInput = document.getElementById("buy-shares"); // Add this variable for the buy form
    const sellErrorMessage = document.getElementById("sell-error-message"); // Change "errorMessage" to "sellErrorMessage"
    const buyErrorMessage = document.getElementById("buy-error-message"); // Add this variable for the buy form

    // Function to display the error message for the sell form
    function displaySellError(message) {
        sellErrorMessage.textContent = message;
        sellErrorMessage.style.display = "block";
    }

    // Function to hide the error message for the sell form
    function hideSellError() {
        sellErrorMessage.textContent = "";
        sellErrorMessage.style.display = "none";
    }

    // Function to display the error message for the buy form
    function displayBuyError(message) {
        buyErrorMessage.textContent = message;
        buyErrorMessage.style.display = "block";
    }

    // Function to hide the error message for the buy form
    function hideBuyError() {
        buyErrorMessage.textContent = "";
        buyErrorMessage.style.display = "none";
    }

    // Event listener for the sell form
    sellForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const sharesToSell = parseInt(sellSharesInput.value);
        const stockSymbol = document.getElementById("sell-symbol").value; // Change "symbol" to "sell-symbol"

        // ... Add your sell form specific error handling code here ...

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
                displaySellError(data.error); // Call the function to display the error message
            } else {
                hideSellError(); // Call the function to hide the error message
            }
        })
        .catch(error => {
            console.error('Error occurred:', error);
        });
    });

    // Event listener for the buy form
    buyForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const sharesToBuy = parseInt(buySharesInput.value); // Change "sharesToSell" to "sharesToBuy"
        const stockSymbol = document.getElementById("buy-symbol").value; // Change "symbol" to "buy-symbol"

        // ... Add your buy form specific error handling code here ...

        fetch('/buy', {
            method: 'POST',
            body: new URLSearchParams({
                'symbol': stockSymbol,
                'shares': sharesToBuy // Change "sharesToSell" to "sharesToBuy"
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                // Handle successful form submission here - redirect to home page
                console.log('Shares bought successfully.');
                alert('Shares bought successfully.');
                window.location.href = '/'; // Redirect to the homepage after successful buy
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data.error) {
                displayBuyError(data.error); // Call the function to display the error message
            } else {
                hideBuyError(); // Call the function to hide the error message
            }
        })
        .catch(error => {
            console.error('Error occurred:', error);
        });
    });

    // ... Rest of your JavaScript code ...
});
