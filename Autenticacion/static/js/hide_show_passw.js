let toggleBtn = document.getElementById('toggleBtn');
let toggleBtnR = document.getElementById('toggleBtn1');
let toggleBtnR2 = document.getElementById('toggleBtn2');
let toggleBtnActual = document.getElementById('toggleBtnActual');
let toggleBtnNueva = document.getElementById('toggleBtnNueva');
let toggleBtnNuevaConf = document.getElementById('toggleBtnNuevaConf');



let clave_registro = document.getElementById('passw1');
let clave_conf_registro = document.getElementById('passw2');
let clave_login = document.getElementById('contraseña');
let clave_actual = document.getElementById('passw_actual'); // Asegúrate que el ID sea correcto
let clave_nueva = document.getElementById('passw_new'); // Asegúrate que el ID sea correcto
let clave_nueva_conf = document.getElementById('passw_new_conf'); // Asegúrate que el ID sea correcto

// Función para alternar la visibilidad de la contraseña
function togglePasswordVisibility(inputField, toggleButton) {

    if (!inputField) {
        console.error("El campo de contraseña no fue encontrado.");
        return;
    }

    if (inputField.type === 'password') {
        inputField.setAttribute('type', 'text');
        toggleButton.classList.add('hide');
    } 
    
    else {
        inputField.setAttribute('type', 'password');
        toggleButton.classList.remove('hide');
    }
}
// Asignar onclick solo si los elementos existen en el DOM
if (toggleBtn) {
    toggleBtn.onclick = function () {
        togglePasswordVisibility(clave_login, toggleBtn);
    };
}


if (toggleBtnR) {
    toggleBtnR.onclick = function () {
        togglePasswordVisibility(clave_registro, toggleBtnR);
    };
}
if (toggleBtnR2) {
    toggleBtnR2.onclick = function () {
        togglePasswordVisibility(clave_conf_registro, toggleBtnR2);
    };
}



if (toggleBtnActual) {
    toggleBtnActual.onclick = function () {
        togglePasswordVisibility(clave_actual, toggleBtnActual);
    };
}
if (toggleBtnNueva) {
    toggleBtnNueva.onclick = function () {
        togglePasswordVisibility(clave_nueva, toggleBtnNueva);
    };
}
if (toggleBtnNuevaConf) {
    toggleBtnNuevaConf.onclick = function () {
        togglePasswordVisibility(clave_nueva_conf, toggleBtnNuevaConf);
    };
}