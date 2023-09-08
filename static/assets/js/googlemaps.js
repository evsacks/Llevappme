function initMap() {
    lat_inicial = parseFloat(document.getElementById('lat_inicial').innerHTML);
    lng_inicial = parseFloat(document.getElementById('lng_inicial').innerHTML);
    lat_final = parseFloat(document.getElementById('lat_final').innerHTML);
    lng_final = parseFloat(document.getElementById('lng_final').innerHTML);
    console.log(lat_inicial, lng_inicial);
    console.log(lat_final, lng_final);

    var pointA = new google.maps.LatLng(lat_inicial, lng_inicial),
        pointB = new google.maps.LatLng(lat_final, lng_final),
        myOptions = {
            zoom: 7,
            center: pointA
        },
       
        map = new google.maps.Map(document.getElementById('map'), myOptions),
        // Instantiate a directions service.
        directionsService = new google.maps.DirectionsService,
        directionsDisplay = new google.maps.DirectionsRenderer({
            map: map
        }),
        markerA = new google.maps.Marker({
            position: pointA,
            title: "Origen",
            map: map
        }),
        markerB = new google.maps.Marker({
            position: pointB,
            title: "Destino",
            map: map
        });

        // get route from A to B
    calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB);

}

function calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB) {
    directionsService.route({
        origin: pointA,
        destination: pointB,
        avoidTolls: true,
        avoidHighways: false,
        travelMode: google.maps.TravelMode.DRIVING
    }, function (response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

window.initMap = initMap;