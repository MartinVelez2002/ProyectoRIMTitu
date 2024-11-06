let pswrd1 = document.getElementById('passw_new');

let lowerCase = document.getElementById('lower');
let upperCase = document.getElementById('upper');
let digit = document.getElementById('number');
let specialChar = document.getElementById('special');
let minLength = document.getElementById('length');





pswrd1.addEventListener('keyup', function () {
    checkPassword(this.value)
});


// Función para verificar los criterios y actualizar visualización
function checkPassword(data) {
    const lower = new RegExp('(?=.*[a-z])');
    const upper = new RegExp('(?=.*[A-Z])');
    const number = new RegExp('(?=.*[0-9])');
    const special = new RegExp('(?=.*[!@#\\$%\\^&\\*])');
    const length = new RegExp('(?=.{8,})');

    updateValidationStatus(lowerCase, lower.test(data));
    updateValidationStatus(upperCase, upper.test(data));
    updateValidationStatus(digit, number.test(data));
    updateValidationStatus(specialChar, special.test(data));
    updateValidationStatus(minLength, length.test(data));
}

// Función auxiliar para actualizar el estado visual de cada criterio
function updateValidationStatus(element, isValid) {
    if (isValid) {
        element.classList.add('valid');
    } 
    else {
        element.classList.remove('valid');
    }
}

