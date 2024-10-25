const forma = document.getElementById('formul');
const email = document.getElementById('correo');
const clave = document.getElementById('contraseña');
const clave2 = document.getElementById('contra2');


forma.addEventListener('submit', e => {
    e.preventDefault();
    validateInputs();
});


const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error')

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
};

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');

};

const isValidEmail = email => {
    const re = /^(([^<>()\[\]\\.,;:\s@”]+(\.[^<>()\[\]\\.,;:\s@”]+)*)|(“.+”))@((\[[0–9]{1,3}\.[0–9]{1,3}\.[0–9]{1,3}\.[0–9]{1,3}])|(([a-zA-Z\-0–9]+\.)+[a-zA-Z]{2,}))$/
    return re.test(String(email).toLowerCase());
};


const validateInputs = () => {
    const emailValue = email.value.trim();
    const passwordValue = clave.value.trim();
    const password2Value = clave2.value.trim();


    if (!isValidEmail(emailValue)) {
        setError(email, 'Proporcionar un email válido.');
    } else {
        setSuccess(email);
        if (password2Value !== passwordValue) {
            setError(clave2, 'Las claves no coinciden.');
        } else {
            setSuccess(clave2);
            document.querySelector("form").submit();
        }
    }

    if (password2Value !== passwordValue) {
        setError(clave2, 'Las claves no coinciden.');
    }
};


