// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

//For loading markers: const { AdvancedMarkerElement } = await google.maps.importLibrary("marker") as google.maps.MarkerLibrary;
let map, infoWindow, socket, table;
//let staticMapURL = https://maps.googleapis.com/maps/api/staticmap?size=400x400&maptype=roadmap&markers=color:blue%7Clabel:S%7C11211%7C11206%7C11222&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0&signature=Intzeger

let url = ""

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
  //Image size can be changed via these params
  carImg.height = 30;
  carImg.width = 30;
  carImg.src = "car.png"

  //Initializing a  marker
  let src_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },
    content: carImg,
  });

  let dest_marker = new AdvancedMarkerElement({
    map,
    position: { lat: 33.621955642487734, lng: 72.95814350678089 },//saves destination value, but initially null
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
    //Updating destination marker when click on map.
    dest_marker = new AdvancedMarkerElement({
      map,
      position: { lat: mapsMouseEvent.latLng.lat(), lng: mapsMouseEvent.latLng.lng() },//saves desintation value, but initially null
      content: pinBackground.element,//pinBackground.element,
    });

    dest_cords.innerText = `Latitude: ${dest_marker.position.lat.toPrecision(8)}
    Longitude: ${dest_marker.position.lng.toPrecision(8)}`;
    //Computing shortest path to new destination.
    calculateAndDisplayRoute(directionsService, directionsRenderer, src_marker.position, dest_marker.position);
    
    //opening URL to get the encoded polyline points
    // const json_polyline_overview = "https://maps.googleapis.com/maps/api/directions/json?origin=" + src_marker.position.lat + ",%20" + src_marker.position.lng + 
    // "&destination=" + dest_marker.position.lat + ",%20" + dest_marker.position.lng + "&mode=driving&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0";

    // window.open(json_polyline_overview);
    // //end goal: https://maps.googleapis.com/maps/api/staticmap?size=200x200&path=enc:wxelEish|LH`BXtEB?&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0

    // //Getting data from JSON
    //Setting sidebar to display directions
    directionsRenderer.setPanel(document.getElementById("sidebar"));
    const control = document.getElementById("floating-panel");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);
  
    //Sending the current destination to server
  });

  //Getting directions to move
  //sends repeated data but is manageable, will use the latest data received
  const observer = new MutationObserver(mutationsList => {
    for (let mutation of mutationsList) {
      if (mutation.type === 'childList' && mutation.target === document.getElementById("sidebar")) {
        // The innerHTML has changed, so read the new content
        let directions_data = "";
        table = document.getElementsByClassName("adp-directions")[0]

        for (var r = 0, n = table.rows.length; r < n; r++) {
          for (var c = 2, m = table.rows[r].cells.length; c < m; c+=3) {
              //getting direction
              //const boldWords = Array.from(table.rows[r].cells[c].innerHTML).map(bold => bold.textContent)
              const boldContentRegex = /<b>(.*?)<\/b>/i;
              // Extract content within the <b> tags using match and filter
              const extractedBoldContent = table.rows[r].cells[c].innerHTML.match(boldContentRegex);
              //Getting distance
              const distanceRegex = /\b(\d+(\.\d+)?) (km|m)\b/g;
              // Extract numbers and units using match and filter
              const extractedDistances = table.rows[r].cells[c+1].innerHTML.match(distanceRegex);

              directions_data += extractedBoldContent[1] + "," + extractedDistances + "\n"; //Can be viewed as queued data
          }
        }
        console.log(directions_data) //SEND TO SOCKET
        fetch(url + '/data', { //python server to fetch from
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(directions_data),
        })
        .then(response => response.json())
        .then(data => {
          console.log('Response from Python:', data);
          // Process the response from Python as needed
        })
        .catch(error => {
          console.error('Error:', error);
        });

      }
    }
  });

  // Configuration for the observer
  const observerConfig = {
    attributes: false,
    childList: true,
    subtree: true
  };
  
  // Start observing the changes in the content element
  observer.observe(document.getElementById("sidebar"), observerConfig);

  
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

  setInterval(() => {
    fetchDataFromPython(src_marker);
  }, 5000);
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

// function updateCurrentCoordinates(coordinates) {
//   // Update your UI with the received coordinates
//   const srcCordsLabel = document.getElementById('src_cords');
//   srcCordsLabel.innerText = `Latitude: ${coordinates.latitude.toPrecision(8)}
//   Longitude: ${coordinates.longitude.toPrecision(8)}`;
//   const src_marker = new AdvancedMarkerElement({
//     map,
//     position: { lat: coordinates.latitude, lng: coordinates.longitude },
//     content: carImg,
//   });
//   return src_marker;
// }

function sendDestinationCoordinates(destination) {
  console.log(destination)
  socket.send(JSON.stringify(destination)); //Changed WebSocket HERE
  //writeDirectionToFile(destination);
}


async function fetchDataFromPython(src_marker) {  
  fetch("http://127.0.0.1:5000/sendDataToJS")
  .then(response => response.json())
  .then(data => {
    console.log(data);
    const coords = data.split(',');
    const src_cords = document.getElementById('src_cords');
    const slat = parseFloat(coords[0]); const slng = parseFloat(coords[1]);
    if (slat == 0 || slng == 0){
      return;
    }
    src_cords.innerText = `Latitude {slat}\nLongitude: {slng}`;

    //displaying marker
    //Initializing a  marker
    // src_marker = new AdvancedMarkerElement({
    //   map,
    //   position: { lat: slat, lng: slng},//saves desintation value, but initially null
    //   content: carImg,//pinBackground.element,
    // });

    src_marker.position = new google.maps.LatLng(slat, slng);
    console.log(src_marker.position);
    // Process the received data from Python as needed
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

//calling both async functions in parallel
// async function runInParallel(){
//   try{
//     const { Map } = await google.maps.importLibrary("maps");
//     map = new Map(document.getElementById("map"), {
//       //EME Barber Shop Location: 33.621955642487734, 72.95814350678089
//       center: { lat: 33.621955642487734, lng: 72.95814350678089 },//need to get this cords from raspberry pi
//       zoom: 18,
//       //for getting map with desired features only
//       mapId: "a9053d1e13164e6b",
//     });
  
//     //const result = await Promise.all([initMap, fetchDataFromPython()])
//     window.initMap = initMap;
//     //initMap();
//     fetchDataFromPython();
//   }
//   catch{
//     console.error('Error: ', error);
//   }
// }
window.initMap = initMap;
// Call the function to fetch data from Python
//https://th.bing.com/th/id/R.990b116b8856614c043d7aa70efff5be?rik=r%2fPnJO4xnpTLwA&riu=http%3a%2f%2fwww.clker.com%2fcliparts%2fh%2f7%2fU%2fU%2fm%2fo%2fgreen-flag-hi.png&ehk=pwvlDIRSQTwOve4cd0q5m4geh4jLJp2Usbe%2bWkxgDEw%3d&risl=&pid=ImgRaw&r=0
/*"https://maps.googleapis.com/maps/api/staticmap?size=1000x1000\
&markers=size:small%7Ccolor:blue%7Clabel:S%7C" + src_marker.position.lat + ", " + src_marker.position.lng + 
"&markers=size:small%7Ccolor:0xFFFF00%7Clabel:D%7C" + dest_marker.position.lat + ", " + dest_marker.position.lng +
"&key=AIzaSyCCB7UocJCGGZO4BxsxQ24TCtTNJTujGN0"*/