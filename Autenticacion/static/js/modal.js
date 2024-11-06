var $ = jQuery.noConflict();
function abrir_modal(url) {
    $('#insertar').load(url, function () {
        $(this).modal('show');
    });
}

function abrir_modal_eliminar(url) {
    $('#eliminar').load(url, function () {
        $(this).modal('show')
    });
}
function abrir_modal_editar(url) {
    $('#editar').load(url, function () {
        $(this).modal('show')
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los divs con la clase 'input-div one'
    const inputDivs = document.querySelectorAll(".input-div.one");

    // Cuenta cuántos hay
    const count = inputDivs.length;

    // Selecciona el contenedor de la cuadrícula
    const formGrid = document.querySelector(".form-grid");
    console.log(formGrid)

    // Modifica el estilo grid-template-columns para repetir según la cantidad de 'input-div one'
    formGrid.style.display = "grid";
    formGrid.style.gridTemplateColumns = `repeat(${count}, 1fr)`;
    console.log("FUNCIONANDO")
});
console.log("MODO SEXO")