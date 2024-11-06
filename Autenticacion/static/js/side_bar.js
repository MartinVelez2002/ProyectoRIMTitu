

/* Para el Sidebar */
let flecha = document.getElementById('btn');
let sidebar = document.querySelector('.side-bar');

flecha.onclick = function () {
    sidebar.classList.toggle('active');
    if (sidebar.classList.contains('active')) {
        flecha.classList.replace("fa-angles-left", "fa-angles-right");
    } else {
        flecha.classList.replace("fa-angles-right", "fa-angles-left");
    }
};

