let map, infoWindow, socket;
const REMOTEIT_URL = 'tcp://proxy61.rt3.io:37338';

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
  const src_cords = document.getElementById('src_cords');
  const dest_cords = document.getElementById('dest_cords');
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();

  map = new Map(document.getElementById("map"), {
    center: { lat: 33.621955642487734, lng: 72.95814350678089 },
    zoom: 18,
    mapId: "a9053d1e13164e6b",
  });
  directionsRenderer.setMap(map);

  infoWindow = new google.maps.InfoWindow();

  const pinBackground = new PinElement({
    background: "#FBBC04",
    borderColor: "#0947f6",
    glyphColor: "#0947f6",
  });

  const carImg = document.createElement("img");
  carImg.src ="car.png"
  carImg.height = 30;
  carImg.width = 30;

  let src_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },
    content: carImg,
  });

  let dest_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },
    content: pinBackground.element,
  });

  const locationButton = document.createElement("button");
  src_cords.innerText = `Latitude: ${src_marker.position.lat.toPrecision(8)}
  Longitude: ${src_marker.position.lng.toPrecision(8)}`;

  locationButton.textContent = "Config Map";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  map.addListener("click", (mapsMouseEvent) => {  
    dest_marker = new AdvancedMarkerElement({
      map,
      position: { lat: mapsMouseEvent.latLng.lat(), lng: mapsMouseEvent.latLng.lng() },
      content: pinBackground.element,
    });

    dest_cords.innerText = `Latitude: ${dest_marker.position.lat.toPrecision(8)}
    Longitude: ${dest_marker.position.lng.toPrecision(8)}`;
    calculateAndDisplayRoute(directionsService, directionsRenderer, src_marker.position, dest_marker.position);
    
    directionsRenderer.setPanel(document.getElementById("sidebar"));
  });

  locationButton.addEventListener("click", () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        },
      );
    } else {
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  // WebSocket connection
  socket = new WebSocket(REMOTEIT_URL.replace('tcp', 'wss'));
  
  socket.onopen = () => {
    console.log('Connected to server');
  };
  
  socket.onmessage = (event) => {
    const currentCoordinates = JSON.parse(event.data);
    console.log('Received current coordinates:', currentCoordinates);
    src_marker = updateCurrentCoordinates(currentCoordinates);
    calculateAndDisplayRoute(directionsService, directionsRenderer, src_marker.position, dest_marker.position);
  };
  
  socket.onclose = (event) => {
    console.log('Connection closed:', event);
  };
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, srcLatLng, destLatLng) {
  directionsService
    .route({
      origin: srcLatLng,
      destination: destLatLng,
      travelMode: google.maps.TravelMode.DRIVING,
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + status));
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation.",
  );
  infoWindow.open(map);
}
function updateCurrentCoordinates(coordinates) {
    // Update your UI with the received coordinates
    const srcCordsLabel = document.getElementById('src_cords');
    srcCordsLabel.innerText = `Latitude: ${coordinates.latitude.toPrecision(8)}
    Longitude: ${coordinates.longitude.toPrecision(8)}`;
    const src_marker = new AdvancedMarkerElement({
      map,
      position: { lat: coordinates.latitude, lng: coordinates.longitude },
      content: carImg,
    });
    return src_marker;
  }
  
  function sendDestinationCoordinates(destination) {
    console.log(destination);
    socket.send(JSON.stringify(destination));
  }
  
  window.initMap = initMap;
