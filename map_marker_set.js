// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

//For loading markers: const { AdvancedMarkerElement } = await google.maps.importLibrary("marker") as google.maps.MarkerLibrary;
let map, infoWindow, socket;
const REMOTEIT_URL = 'tcp://proxy61.rt3.io:36072';
//let staticMapURL = https://maps.googleapis.com/maps/api/staticmap?size=400x400&maptype=roadmap&markers=color:blue%7Clabel:S%7C11211%7C11206%7C11222&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0&signature=Intzeger

async function initMap() {
  //setting an initial point on the map
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
  const src_cords = document.getElementById('src_cords');
  const dest_cords = document.getElementById('dest_cords');
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();

  map = new Map(document.getElementById("map"), {
    //EME Barber Shop Location: 33.621955642487734, 72.95814350678089
    center: { lat: 33.621955642487734, lng: 72.95814350678089 },//need to get this cords from raspberry pi
    zoom: 18,
    //for getting map with desired features only
    mapId: "a9053d1e13164e6b",
  });
  directionsRenderer.setMap(map);

  infoWindow = new google.maps.InfoWindow();
  
  //---------------------------Marker Initializatin and Customization------------------------
  // Optional: subscribe to map capability changes.
  map.addListener('mapcapabilities_changed', () => {
    const mapCapabilities = map.getMapCapabilities();
    if (!mapCapabilities.isAdvancedMarkersAvailable) {
      // Advanced markers are not available, add a fallback.
      console.log("Incompatible with map capability changes");
    }
  });

  //Customizing marker
  // Change the background color.
  // For marking destination
  const pinBackground = new PinElement({
    background: "#FBBC04",
    borderColor: "#0947f6",
    glyphColor: "#0947f6",
  });

  //Adding custom image instead of default marker
  // A marker with a with a URL pointing to a PNG.
  const carImg = document.createElement("img");

  //where to take img from
  carImg.src ="car.png"
  //Image size can be changed via these params
  carImg.height = 30;
  carImg.width = 30;

  //Initializing a  marker
  let src_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },
    content: carImg,
  });

  let dest_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },//saves desintation value, but initially null
    content: pinBackground.element,//pinBackground.element,
  });


  const locationButton = document.createElement("button");
  src_cords.innerText = `Latitude: ${src_marker.position.lat.toPrecision(8)}
  Longitude: ${src_marker.position.lng.toPrecision(8)}`;

  //to remove marker
  //dest_marker.map = null;

  locationButton.textContent = "Config Map";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  //Clicking on Map
  // Configure the click listener.
  map.addListener("click", (mapsMouseEvent) => {  
    dest_marker = new AdvancedMarkerElement({
      map,
      position: { lat: mapsMouseEvent.latLng.lat(), lng: mapsMouseEvent.latLng.lng() },//saves desintation value, but initially null
      content: pinBackground.element,//pinBackground.element,
    });

    dest_cords.innerText = `Latitude: ${dest_marker.position.lat.toPrecision(8)}
    Longitude: ${dest_marker.position.lng.toPrecision(8)}`;
    calculateAndDisplayRoute(directionsService, directionsRenderer, src_marker.position, dest_marker.position);
    //We also need to generate a static map which we will take as image to navigate in
    
    //opening URL to get the encoded polyline points
    // const json_polyline_overview = "https://maps.googleapis.com/maps/api/directions/json?origin=" + src_marker.position.lat + ",%20" + src_marker.position.lng + 
    // "&destination=" + dest_marker.position.lat + ",%20" + dest_marker.position.lng + "&mode=driving&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0";

    // window.open(json_polyline_overview);
    // //end goal: https://maps.googleapis.com/maps/api/staticmap?size=200x200&path=enc:wxelEish|LH`BXtEB?&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0

    // //Getting data from JSON
    // downloadJSONFile(json_polyline_overview, "google_directions.json");
    directionsRenderer.setPanel(document.getElementById("sidebar"));

    const control = document.getElementById("floating-panel");
  
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);
    
    var direction_table = document.getElementsByClassName("adp-directions")[0]
    console.log(direction_table)
    //Sending the current destination to server
    sendDestinationCoordinates({"latitude": dest_marker.position.lat.toPrecision(8),
                                "longitude": dest_marker.position.lng.toPrecision(8)})
  });

  //Clicking on config button
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
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
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  //tcp connection
  socket = new WebSocket(REMOTEIT_URL.replace('tcp', 'ws'));

  socket.onopen = () => {
   console.log('Connected to server');
  };
  
  socket.onmessage = (event) => {
    const currentCoordinates = JSON.parse(event.data);
    console.log('Received current coordinates:', currentCoordinates);
    src_marker = updateCurrentCoordinates(currentCoordinates);
    calculateAndDisplayRoute(directionsService, directionsRenderer, src_marker.position, dest_marker.position)
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
  console.log(destination)
  socket.send(JSON.stringify(destination));
}

window.initMap = initMap;

//https://th.bing.com/th/id/R.990b116b8856614c043d7aa70efff5be?rik=r%2fPnJO4xnpTLwA&riu=http%3a%2f%2fwww.clker.com%2fcliparts%2fh%2f7%2fU%2fU%2fm%2fo%2fgreen-flag-hi.png&ehk=pwvlDIRSQTwOve4cd0q5m4geh4jLJp2Usbe%2bWkxgDEw%3d&risl=&pid=ImgRaw&r=0
/*"https://maps.googleapis.com/maps/api/staticmap?size=1000x1000\
&markers=size:small%7Ccolor:blue%7Clabel:S%7C" + src_marker.position.lat + ", " + src_marker.position.lng + 
"&markers=size:small%7Ccolor:0xFFFF00%7Clabel:D%7C" + dest_marker.position.lat + ", " + dest_marker.position.lng +
"&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0"*/
