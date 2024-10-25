const clave1 = document.getElementById('contraseña');


toggleBtn.onclick = function () {
    if (clave1.type === 'password') {
        clave1.setAttribute('type', 'text');
        toggleBtn.classList.add('hide');
    } else {
        clave1.setAttribute('type', 'password');
        toggleBtn.classList.remove('hide');

    }
};