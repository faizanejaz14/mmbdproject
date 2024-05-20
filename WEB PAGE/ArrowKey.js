// const arrowButtons = document.querySelectorAll('.arrows button');

// // Add click event listeners to each button
// arrowButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         const direction = button.id; // Get the button's ID (which represents the direction)
//         console.log(`Clicked: ${direction.split('-')[0]}`);
//     });
// });

const serverAddress = "https://compeccwebsite.z29.web.core.windows.net/"; // Replace with your actual Azure server address

const socket = new WebSocket(`https://${serverAddress}`); // Use ws:// for unsecured connection (for development)

document.addEventListener("keydown", function(event) {
  const keyName = event.key;
  let direction;

  if (keyName === "ArrowUp") {
    direction = "Up";
  } else if (keyName === "ArrowDown") {
    direction = "Down";
  } else if (keyName === "ArrowLeft") {
    direction = "Left";
  } else if (keyName === "ArrowRight") {
    direction = "Right";
  }

  if (direction) {
    console.log("Checking if socket open for communication")
    socket.onopen = function(event) {
        console.log("Socket Open Sending Message")
      socket.send(direction); // Send the direction when the socket opens
    };
  }
});
