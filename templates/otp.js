const verifyButton = document.getElementById("verifyotp");


// Add a click event listener to the Register button
verifyButton.addEventListener("click", async function () {
  // Get values from the form inputs
  const otp = document.getElementById("otp").value;

  let dataToSend = {
        "name": "sankalp",
        "email": "22co17@aiktc.ac.in",
        "user_otp" : 584517,
        "password": "sankalp2004"
  };
  await fetch("http://localhost:2700/addUser", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataToSend),
  })
    .then((response) => response.json())
    .then((data) => {
        document.getElementById("message").textContent = data;
    })
    .catch((error) => {
      console.log(error);
    });

        // Get references to the floating message and close button
const floatingMessage = document.getElementById('floating-message');
const closeButton = document.getElementById('close-button');

// Function to show the floating message
function showFloatingMessage() {
    floatingMessage.style.display = 'block';
}

// Function to hide the floating message
function hideFloatingMessage() {
    floatingMessage.style.display = 'none';
}

// Event listener for closing the message
closeButton.addEventListener('click', hideFloatingMessage);

// Example usage: Show the message after 2 seconds
setTimeout(showFloatingMessage, 2000);
});
