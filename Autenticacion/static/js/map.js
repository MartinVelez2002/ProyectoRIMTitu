let map;
let drawingManager;
let selectedShape; // Forma seleccionada
let shapeLabel; // Etiqueta visible asociada a la figura
let geocoder; // Geocodificador

function initMap() {
    // Inicializa el mapa
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -2.13396, lng: -79.59337 },
        zoom: 14,
    });

    geocoder = new google.maps.Geocoder();

    // Configura el Drawing Manager
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON, // Polígono por defecto
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ["polygon", "rectangle"], // Permite polígonos y rectángulos
        },
        polygonOptions: {
            fillColor: "#FF0000",
            fillOpacity: 0.5,
            strokeWeight: 2,
            clickable: true,
            editable: true, // Permite editar la forma
        },
    });

    // Muestra las herramientas de dibujo
    drawingManager.setMap(map);

    // Escucha cuando se termina de dibujar
    google.maps.event.addListener(drawingManager, "overlaycomplete", (event) => {
        if (selectedShape) {
            selectedShape.setMap(null); // Borra la forma anterior si existe
            if (shapeLabel) shapeLabel.setMap(null); // Elimina la etiqueta anterior
        }

        selectedShape = event.overlay; // Guarda la nueva forma
        selectedShape.type = event.type; // Guarda el tipo

        // Coloca la etiqueta inicial (vacía)
        shapeLabel = new google.maps.InfoWindow({
            content: "Sin título", // Valor por defecto hasta que el usuario escriba
            position: getShapeCenter(selectedShape), // Centro del área dibujada
        });
        shapeLabel.open(map);

        // Detecta cuando se edita la forma y actualiza la posición de la etiqueta
        google.maps.event.addListener(selectedShape.getPath(), "set_at", () => {
            shapeLabel.setPosition(getShapeCenter(selectedShape));
        });
        google.maps.event.addListener(selectedShape.getPath(), "insert_at", () => {
            shapeLabel.setPosition(getShapeCenter(selectedShape));
        });

        // Geocodifica la ubicación del centro del área dibujada
        const center = getShapeCenter(selectedShape);
        if (center) {
            geocodeLatLng(center);
        }
    });

    // Escucha cambios en el input de "Lugar"
    document.querySelector("[name='lugar']").addEventListener("input", (event) => {
        const inputValue = event.target.value; // Obtiene el valor ingresado
        if (shapeLabel) {
            shapeLabel.setContent(inputValue || "Sin título"); // Actualiza la etiqueta
        }
    });
}

// Calcula el centro de una forma (polígono o rectángulo)
function getShapeCenter(shape) {
    if (shape.type === "polygon") {
        const bounds = new google.maps.LatLngBounds();
        shape.getPath().forEach((coord) => bounds.extend(coord));
        return bounds.getCenter();
    } else if (shape.type === "rectangle") {
        return shape.getBounds().getCenter();
    }
    return null;
}

// Geocodifica la ubicación y actualiza el campo de "Sector"
function geocodeLatLng(latLng) {
    geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                const addressComponents = results[0].address_components;
                let sector = "";

                // Extrae el valor del sector
                addressComponents.forEach((component) => {
                    const types = component.types;

                    if (types.includes("sublocality") || types.includes("neighborhood")) {
                        sector = component.long_name;
                    }
                });

                // Actualiza el input de "Sector" con ID sector_input
                const sectorInput = document.getElementById("sector_input");
                if (sectorInput) {
                    sectorInput.value = sector || "No identificado";
                }

                console.log(`Sector detectado: ${sector}`);
            } else {
                console.log("No se encontraron resultados para la ubicación.");
                const sectorInput = document.getElementById("sector_input");
                if (sectorInput) {
                    sectorInput.value = "No identificado";
                }
            }
        } else {
            console.log("Fallo en la geocodificación: " + status);
        }
    });
}





// let map;
// let geocoder;
// let marker; 

// function initMap() {
//     map = new google.maps.Map(document.getElementById("map"), {
//         center: { lat: -2.13396, lng: -79.59337 },
//         zoom: 14,
//     });

//     geocoder = new google.maps.Geocoder();
    
//     map.addListener("click", (event) => {
//         const latLng = event.latLng;
        
//         placeMarker(latLng);

//         geocodeLatLng(latLng);

//     });
// }

// function placeMarker(latLng) {
//     if (marker) {
//         marker.setMap(null);
//     }
    
//     marker = new google.maps.Marker({
//         position: latLng,
//         map: map,
//         title: "Ubicación seleccionada"
//     });
    
//     map.setCenter(latLng);
// }

// function geocodeLatLng(latLng) {
//     geocoder.geocode({ location: latLng }, (results, status) => {
//         if (status === "OK") {
//             if (results[0]) {
//                 const addressComponents = results[0].address_components;
//                 let sector = "";
//                 let callePrincipal = "";
                
//                 console.log("Address Components:", addressComponents);

//                 // Extraer sector y calle principal
//                 addressComponents.forEach((component) => {
//                     const types = component.types;

//                     if (types.includes("sublocality") || types.includes("neighborhood")) {
//                         sector = component.long_name; // Sector o barrio
//                     }
//                     if (types.includes("route")) {
//                         callePrincipal = component.long_name; // Calle principal
//                     }
//                 });

//                 // Validar si se encontró la calle principal
//                 if (!callePrincipal) {
//                     callePrincipal = "Calle no identificada"; // Valor predeterminado si no se encuentra
//                 }

//                 // Llenar los campos con la información obtenida
//                 document.getElementById("sector_input").value = sector || "Sector no identificado";
//                 document.getElementById("calle_principal_input").value = callePrincipal;
               
//                 console.log(`Sector: ${sector}`);
//                 console.log(`Calle Principal: ${callePrincipal}`);
//             } else {
//                 console.log("No se encontraron resultados");
//                 document.getElementById("sector_input").value = "Sector no identificado";
//                 document.getElementById("calle_principal_input").value = "Calle no identificada";
//             }
//         } else {
//             console.log("Geocoding falló: " + status);
//         }
//     });
// }
