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


// Verificar si los inputs tienen un valor al cargar la página y aplicar la clase focus automáticamente
inputs.forEach(input => {
    if (input.value !== "") {
        let parent = input.closest('.div');
        if (parent) {
            parent.classList.add("focus");
        }
    }

    input.addEventListener("focus", addcl);
    input.addEventListener("blur", remcl);
});