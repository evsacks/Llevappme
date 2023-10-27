function initMap() {
    var mapContainer = document.getElementById('map');

    if (mapContainer) {
        var latInicial = parseFloat(mapContainer.getAttribute('data-lat-inicial'));
        var lngInicial = parseFloat(mapContainer.getAttribute('data-lng-inicial'));
        var latFinal = parseFloat(mapContainer.getAttribute('data-lat-final'));
        var lngFinal = parseFloat(mapContainer.getAttribute('data-lng-final'));

        if (!isNaN(latInicial) && !isNaN(lngInicial) && !isNaN(latFinal) && !isNaN(lngFinal)) {
            var pointA = new google.maps.LatLng(latInicial, lngInicial);
            var pointB = new google.maps.LatLng(latFinal, lngFinal);
            var myOptions = {
                zoom: 7,
                center: pointA,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControl: false
            };

            var map = new google.maps.Map(mapContainer, myOptions);

            var directionsService = new google.maps.DirectionsService();
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

            calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB);
        } else {
            console.log('La solicitud falló debido a un valor erróneo en Latitud o Longitud');
        }
    } else {
        console.log('No hay mapa para mostrar');
    }
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

function autocompletar(id) {
    var autocomplete = document.getElementById(id);
    const search = new google.maps.places.Autocomplete(autocomplete);
    console.log(search)
}

window.initMap = initMap;