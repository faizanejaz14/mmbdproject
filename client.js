const REMOTEIT_URL = 'tcp://http://proxy60.rt3.io:37732';
let socket;
let map;

function initMap() {
  // Your existing initMap code goes here...

  // Connect to the server using the provided remoteit URL
  socket = new WebSocket(REMOTEIT_URL.replace('tcp', 'ws'));

  socket.onopen = () => {
    console.log('Connected to server');
  };

  socket.onmessage = (event) => {
    // Handle incoming messages from the server
    const currentCoordinates = JSON.parse(event.data);
    console.log('Received current coordinates:', currentCoordinates);

    // Update your UI or perform any necessary actions with the received coordinates
    updateCurrentCoordinates(currentCoordinates);
  };

  socket.onclose = (event) => {
    console.log('Connection closed:', event);
  };
}

function updateCurrentCoordinates(coordinates) {
  // Update your UI with the received coordinates
  const srcCordsLabel = document.getElementById('src_cords');
  srcCordsLabel.innerText = Latitude: ${coordinates.latitude.toPrecision(8)}, Longitude: ${coordinates.longitude.toPrecision(8)};
}

function sendDestinationCoordinates(destination) {
  // Send destination coordinates to the server
  socket.send(JSON.stringify(destination));
}

// Add any additional functions or event handlers as needed...

// Initialize the map and WebSocket connection
window.initMap = initMap;
