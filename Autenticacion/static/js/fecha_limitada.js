document.addEventListener("DOMContentLoaded", function () {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Mes actual (1-12)
    const day = String(today.getDate()).padStart(2, '0'); // Día actual (01-31)

    // Deshabilitar meses pasados
    document.querySelectorAll("input[type='date']").forEach(input => {
        // Establece el mínimo permitido (YYYY-MM-DD)
        input.setAttribute("min", `${year}-${month}-${day}`);
    });
});