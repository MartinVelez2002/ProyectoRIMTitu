document.addEventListener('DOMContentLoaded', function() {
    // Obtener los elementos de los campos
    const cedulaInput = document.getElementById('id_cedula');
    const password1Input = document.getElementById('passw1');
    const password2Input = document.getElementById('passw2');
    
    // Verificar si los elementos existen
    if (cedulaInput && password1Input && password2Input) {
        // Función que asigna el valor de la cédula a los campos de contraseñas
        cedulaInput.addEventListener('input', function() {
            const cedulaValue = cedulaInput.value;
            console.log('Valor de cédula:', cedulaValue); // Línea de depuración
            password1Input.value = cedulaValue;
            password2Input.value = cedulaValue;
        });
    } else {
        console.log("No se encontraron los campos de entrada necesarios.");
    }
});