# Robotic Car Controller Project

## Overview
This project involves controlling a 4-wheel robotic car using a Raspberry Pi 3 as its controller. The car is equipped with a USB webcam for live streaming and a NEO 6M GPS module to record its current coordinates. These modules are connected to the Raspberry Pi. The car transmits this data to a cloud server for further processing.

## Hardware
The hardware setup includes:
- Raspberry Pi 3 as the controller
- USB webcam for live streaming
- NEO 6M GPS module for recording coordinates

## Website
A locally hosted website has been developed for this project. It utilizes the Google Maps API to display and generate the path and direction the car will take based on the GPS coordinates. The website also hosts the live stream from the NGROCK server. Additionally, the override controls are integrated into this website in case GPS navigation fails.

## Cloud Services
The project utilizes the following cloud services:
- **NGROCK:** Used for live streaming
- **RemoteIT:** Utilized for sending GPS coordinates. RemoteIT employs a duplex TCP service to transmit manual override and navigation instructions to the robotic car.

## Usage
To use this project:
1. Clone the repository.
2. Set up the Raspberry Pi with the necessary modules and connections.
3. Run the locally hosted website to control and monitor the car's movements.

## Contributors

- [Zakria Mehmood](https://github.com/ZakriaComputerEngineer):
  - Implemented live camera streaming functionality
  - Developed socket communication
  - Configured and managed cloud services

- [Faizan Ijaz](https://github.com/faizanejaz14):
  - Integrated the web interface
  - Collaborated on overall system integration

- [Irtaza Hyder](https://github.com/SyedMIrtazaHyder):
  - Worked on navigation functionality
  - Configured Google Direction APIs for integration

## Contribution
Contributions to enhance and improve this project are welcome. Fork the repository, make your changes, and create a pull request with details about your modifications.

## TODO
- Break JS file into smaller related scripts
- Web Socket for sending and receiving data from cloud services (Webhost --> RX => GPS, TX => Directions)
- Decrypt JS file on Pi to start moving.

## References
- NEO 6M with Raspberry Pi: GPS: https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
- Raspberry Pi 3: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
- Google Maps: 
    - Generating JSON: https://developers.google.com/maps/documentation/directions/get-directions
    - Embedded Google Maps: https://developers.google.com/maps/documentation/javascript/adding-a-google-map
    - Map Markers: https://developers.google.com/maps/documentation/javascript/advanced-markers/overview
    - Direction Service: https://developers.google.com/maps/documentation/javascript/examples/directions-simple & https://developers.google.com/maps/documentation/javascript/directions