function initMap() {
    
    var mapContainer = document.getElementById('map');
    var latInicial = parseFloat(mapContainer.getAttribute('data-lat-inicial'));
    var lngInicial = parseFloat(mapContainer.getAttribute('data-lng-inicial'));
    var latFinal = parseFloat(mapContainer.getAttribute('data-lat-final'));
    var lngFinal = parseFloat(mapContainer.getAttribute('data-lng-final'));


    var pointA = new google.maps.LatLng(latInicial, lngInicial);
    var pointB = new google.maps.LatLng(latFinal, lngFinal);
    var myOptions = {
        zoom: 7,
        center: pointA,
        mapTypeId: google.maps.MapTypeId.ROADMAP, // Establece el tipo de mapa predeterminado a ROADMAP
        mapTypeControl: false, // Deshabilita el control de tipo de mapa
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