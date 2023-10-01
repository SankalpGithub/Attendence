const form = document.getElementById("registrationForm");
const registerButton = document.getElementById("registerButton");
const serverResponse = document.getElementById("serverResponse");

// Add a click event listener to the Register button
registerButton.addEventListener("click", function () {
  // Get values from the form inputs
  // const name = document.getElementById("fullname").value;
  // const email = document.getElementById("email").value;
  // const password = document.getElementById("password").value;

  // // Display the values in HTML
  // document.getElementById("displayFullName").textContent = "Full Name: " + name;
  // document.getElementById("displayEmail").textContent = "Email: " + email;
  // document.getElementById("displayPassword").textContent = "Password: " + password;

  window.location.herf="otp.html"

    

  // Send a POST request with the data
  // await fetch('http://localhost:2700/signup', {
  //     method: 'POST',

  //     body: JSON.stringify({name, email, password }),
  // })




  // let dataToSend = {
  //   email
  // };
  // await fetch("http://localhost:2700/signup", {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify(dataToSend),
  // })
  //   .then((response) => response.json())
  //   .then((data) => {
  //     console.log(data);
  //     serverResponse.innerHTML = data.message;
  //   })
  //   .catch((error) => {
  //     console.log(error);
  //   });

  //   window.location.href = 'otp.html';

  //   await fetch("http://localhost:2700/getAllUsers", { method: "GET" })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       // Handle the response from the server
  //       console.log(data);
  //       const myList = document.createElement("ul");
  //       data.map((user) => {
  //         // Create a <ul> (unordered list) element

  //         // Create list items ( <li> elements) and append them to the <ul>
  //         const listItem1 = document.createElement("li");
  //         listItem1.textContent = user.email;
  //         myList.appendChild(listItem1)
  //     });
  //     serverResponse.appendChild(myList);
  //       // serverResponse.textContent = d;
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
});
