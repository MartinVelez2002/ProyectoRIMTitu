function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -2.13396, lng: -79.59337 },
        zoom: 14,
    });

    
    geocoder = new google.maps.Geocoder();
    // Escuchar clics en el mapa
    map.addListener("click", (event) => {
        const latLng = event.latLng;
        geocodeLatLng(latLng);
        obtenerInterseccionAlternativa(latLng);
    });


}


function geocodeLatLng(latLng) {
    geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {

                const addressComponents = results[0].address_components;
                const place = results[0];
                let sector = "";
                let callePrincipal = "";
                let interseccion = "";
                console.log("Address Components:", place.address_components);
                
               
                addressComponents.forEach((component) => {
                    const types = component.types;

                    if (types.includes("sublocality") || types.includes("neighborhood")) {
                        sector = component.long_name;
                    }
                    if (types.includes("route")) {
                        if (!callePrincipal) {
                            callePrincipal = component.long_name;
                        } else if (!interseccion) {
                            interseccion = component.long_name;
                        }
                    }
                });

              
                document.getElementById("sector_input").value = sector;
                document.getElementById("calle_principal_input").value = callePrincipal;
               
                console.log(`Sector: ${sector}`);
                console.log(`Calle Principal: ${callePrincipal}`);
            } else {
                console.log("No se encontraron resultados");
            }
        } else {
            console.log("Geocoding falló: " + status);
        }
    });
}
function obtenerInterseccionAlternativa(latLng) {
    const offsetLatLng = {
        lat: latLng.lat() + 0.001,
        lng: latLng.lng() + 0.001
    };

    geocoder.geocode({ location: offsetLatLng }, (results, status) => {
        if (status === "OK" && results[0]) {
       
            const interseccionPlace = results[0];
            const interseccion = interseccionPlace.address_components.find(
                (component) => component.types.includes("route")
            );

            if (interseccion) {
                document.querySelector("#input-interseccion").value = interseccion.long_name;
                console.log("Intersección (calle cercana) asignada:", interseccion.long_name);
            }
        }
    });
}
