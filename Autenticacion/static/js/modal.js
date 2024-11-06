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

