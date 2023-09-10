function initMap() {
    var lat_inicial = parseFloat(document.getElementById('lat_inicial').textContent);
    var lng_inicial = parseFloat(document.getElementById('lng_inicial').textContent);
    var lat_final = parseFloat(document.getElementById('lat_final').textContent);
    var lng_final = parseFloat(document.getElementById('lng_final').textContent);

    var pointA = new google.maps.LatLng(lat_inicial, lng_inicial);
    var pointB = new google.maps.LatLng(lat_final, lng_final);
    var myOptions = {
        zoom: 7,
        center: pointA
    };

    var map = new google.maps.Map(document.getElementById('map'), myOptions);

    // Instantiate a directions service.
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer({
        map: map
    });

    var markerA = new google.maps.Marker({
        position: pointA,
        title: "Origen",
        map: map
    });
    
    var markerB = new google.maps.Marker({
        position: pointB,
        title: "Destino",
        map: map
    });

    // Obtener la ruta desde A hasta B
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
            window.alert('La solicitud de direcciones falló debido a ' + status);
        }
    });
}

window.initMap = initMap;