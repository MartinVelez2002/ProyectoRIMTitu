const numCed = document.getElementById("inputCedula")

numCed.addEventListener("keyup", function () {
    Comprobacion(numCed.value)

})

function Comprobacion(numCed) {
    let out = '';
    let correct = '1234567890';

    for (let i = 0; i < numCed.length; i++)
        if (correct.indexOf(numCed.charAt(i)) != -1)
            out += numCed.charAt(i);
    numCed = out;
    document.getElementById("inputCedula").value = numCed;
}

