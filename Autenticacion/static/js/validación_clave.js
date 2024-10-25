let pswrd = document.getElementById('contraseña');
let pswrd2 = document.getElementById('contra2');
let toggleBtn = document.getElementById('toggleBtn');
let toggleBtn1 = document.getElementById('toggleBtn1');

let lowerCase = document.getElementById('lower');
let upperCase = document.getElementById('upper');
let digit = document.getElementById('number');
let specialChar = document.getElementById('special');
let minLength = document.getElementById('length');

document.querySelector('#contraseña').addEventListener('keyup', function () {
    checkPassword(this.value)
});


//Mostrar y ocultar clave

toggleBtn.onclick = function () {
    if (pswrd.type === 'password') {
        pswrd.setAttribute('type', 'text');
        toggleBtn.classList.add('hide');
    } else {
        pswrd.setAttribute('type', 'password');
        toggleBtn.classList.remove('hide');

    }
};

toggleBtn1.onclick = function () {
    if (pswrd2.type === 'password') {
        pswrd2.setAttribute('type', 'text')
        toggleBtn1.classList.add('mostrar');
    } else {
        pswrd2.setAttribute('type', 'password')
        toggleBtn1.classList.remove('mostrar');
    }
};


function checkPassword(data) {
    const lower = new RegExp('(?=.*[a-z])');
    const upper = new RegExp('(?=.*[A-Z])');
    const number = new RegExp('(?=.*[0-9])');
    const special = new RegExp('(?=.*[!@#\$%\^&\*])');
    const length = new RegExp('(?=.{10,})');

    //Validar minúsculas
    if (lower.test(data)) {
        lowerCase.classList.add('valid');
    } else {
        lowerCase.classList.remove('valid');
    }
    //Validar Mayúsculas
    if (upper.test(data)) {
        upperCase.classList.add('valid');
    } else {
        upperCase.classList.remove('valid');
    }

    // Validar números
    if (number.test(data)) {
        digit.classList.add('valid');
    } else {
        digit.classList.remove('valid');
    }

    //Validar caracteres especiales
    if (special.test(data)) {
        specialChar.classList.add('valid');
    } else {
        specialChar.classList.remove('valid');
    }
    //Mínimo de caracteres
    if (length.test(data)) {
        minLength.classList.add('valid');
    } else {
        minLength.classList.remove('valid');
    }
}