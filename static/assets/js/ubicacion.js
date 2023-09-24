function obtenerYGuardarUbicacion() {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var latitud = position.coords.latitude;
        var longitud = position.coords.longitude;
  
        // Enviar los datos al servidor
        enviarUbicacionAlServidor(latitud, longitud);
  
        // Programar la próxima actualización después de 5 segundos
        setTimeout(obtenerYGuardarUbicacion, 5000);
      });
    } else {
      console.log("El navegador no admite la geolocalización.");
    }
  }
  
  function enviarUbicacionAlServidor(latitud, longitud) {
    // Realizar una solicitud AJAX al servidor para guardar los datos
    // Puedes usar fetch o XMLHttpRequest para esto
    // Ejemplo de cómo usar fetch:
    fetch("/viaje/guardarUbicacion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ latitud, longitud }),
    })
      .then(function(response) {
        if (response.ok) {
          console.log("Ubicación guardada con éxito en el servidor.");
        } else {
          console.error("Error al guardar la ubicación en el servidor.");
        }
      })
      .catch(function(error) {
        console.error("Error al realizar la solicitud al servidor: " + error);
      });
  }
  
  // Iniciar el proceso de obtención y guardado de ubicación
  obtenerYGuardarUbicacion();