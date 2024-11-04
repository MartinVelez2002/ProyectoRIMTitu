const inputs = document.querySelectorAll(".input");


function addcl() {
    let parent = this.parentNode.parentNode;
    parent.classList.add("focus");
}

function remcl() {
    let parent = this.parentNode.parentNode;
    if (this.value == "") {
        parent.classList.remove("focus");
    }
}

inputs.forEach(input => {
    input.addEventListener("focus", addcl);
    input.addEventListener("blur", remcl);
});


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