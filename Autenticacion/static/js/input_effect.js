const inputs = document.querySelectorAll(".input");
    
function addcl() {
    let parent = this.parentNode.parentNode;
    parent.classList.add("focus");
}

function remcl() {
    let parent = this.parentNode.parentNode;
    if (this.value.trim() === "") {
        parent.classList.remove("focus");
    }
}

// Verificar al cargar la página si el input ya tiene valor
inputs.forEach(input => {
    if (input.value.trim() !== "") {
        input.parentNode.parentNode.classList.add("focus");
    }
    input.addEventListener("focus", addcl);
    input.addEventListener("blur", remcl);
});
