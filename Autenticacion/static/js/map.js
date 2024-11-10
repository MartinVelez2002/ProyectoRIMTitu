let map;
let geocoder;
let marker; 

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -2.13396, lng: -79.59337 },
        zoom: 14,
    });

    geocoder = new google.maps.Geocoder();
    
    map.addListener("click", (event) => {
        const latLng = event.latLng;
        
        placeMarker(latLng);

        geocodeLatLng(latLng);
    });
}

function placeMarker(latLng) {
    if (marker) {
        marker.setMap(null);
    }
    
    marker = new google.maps.Marker({
        position: latLng,
        map: map,
        title: "Ubicación seleccionada"
    });
    
    map.setCenter(latLng);
}

function geocodeLatLng(latLng) {
    geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                const addressComponents = results[0].address_components;
                const place = results[0];
                let sector = "";
                let callePrincipal = "";
                
                console.log("Address Components:", place.address_components);

                // Extraer sector y calle principal
                addressComponents.forEach((component) => {
                    const types = component.types;

                    if (types.includes("sublocality") || types.includes("neighborhood")) {
                        sector = component.long_name;
                    }
                    if (types.includes("route")) {
                        if (!callePrincipal) {
                            callePrincipal = component.long_name;
                        }
                    }
                });

                // Llenar los campos con la información obtenida
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
