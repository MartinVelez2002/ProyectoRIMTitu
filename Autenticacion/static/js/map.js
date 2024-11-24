let map;
let drawingManager;
let selectedShape;
let shapeLabel;
let geocoder;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -2.13396, lng: -79.59337 },
        zoom: 14,
    });

    geocoder = new google.maps.Geocoder();

    drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ["polygon"],
        },
        polygonOptions: {
            fillColor: "#FF0000",
            fillOpacity: 0.5,
            strokeWeight: 2,
            clickable: true,
            editable: true,
        },
    });

    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, "overlaycomplete", (event) => {
        if (selectedShape) {
            selectedShape.setMap(null);
            if (shapeLabel) shapeLabel.setMap(null);
        }

        selectedShape = event.overlay;
        selectedShape.type = event.type;

        shapeLabel = new google.maps.InfoWindow({
            content: "Sin título",
            position: getShapeCenter(selectedShape),
        });
        shapeLabel.open(map);

        google.maps.event.addListener(selectedShape.getPath(), "set_at", () => {
            shapeLabel.setPosition(getShapeCenter(selectedShape));
        });
        google.maps.event.addListener(selectedShape.getPath(), "insert_at", () => {
            shapeLabel.setPosition(getShapeCenter(selectedShape));
        });

        const center = getShapeCenter(selectedShape);
        if (center) {
            geocodeLatLng(center);
        }
    });

    document.querySelector("[name='lugar']").addEventListener("input", (event) => {
        const inputValue = event.target.value;
        if (shapeLabel) {
            shapeLabel.setContent(inputValue || "Sin título");
        }
    });

    // Detecta tecla Esc para cancelar dibujo
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            drawingManager.setDrawingMode(null);
            if (selectedShape) {
                selectedShape.setMap(null);
                selectedShape = null;
            }
            if (shapeLabel) {
                shapeLabel.setMap(null);
                shapeLabel = null;
            }
        }
    });
}

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

function geocodeLatLng(latLng) {
    geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                const addressComponents = results[0].address_components;
                let sector = "";

                addressComponents.forEach((component) => {
                    const types = component.types;

                    if (types.includes("sublocality") || types.includes("neighborhood")) {
                        sector = component.long_name;
                    }
                });

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
