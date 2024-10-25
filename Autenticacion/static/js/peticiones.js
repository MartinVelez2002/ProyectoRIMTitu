class Finanzas {
    constructor(save) {
        this.save = save //Guarda mi enlace
        this.finanza = {
            anio: '',
            mes: '',
            mensualidades: 0,
            ingresos: 0,
            gastos: 0,
            ganancias: 0,

        }

    }

    CrearList(lista) {
        let datos = [];

        lista.forEach((valor) => {
            let REGISTRO = {}
            REGISTRO.cantidad = valor.Cantidad
            REGISTRO.precio = valor.precio
            REGISTRO.fecha = valor.fecha

            datos = [...datos, REGISTRO]
        })
        return datos
    }

    GenerarGastos(gastos_generados, hol) {

        for (let h of gastos_generados) {

            if (hol.value.split("-")[0] == h.fecha.split("-")[0] && hol.value.split("-")[1] == h.fecha.split("-")[1]) {
                this.finanza.gastos += h.precio * h.cantidad
            }
        }
        this.finanza.ganancias = this.finanza.ingresos - this.finanza.gastos

        document.getElementById("ingresos").value = this.finanza.ingresos
        document.getElementById("gastos").value = this.finanza.gastos
        document.getElementById("ganancias").value = this.finanza.ganancias

    }

    GenerarMensualidades(mensualidades_listado, hol) {
        this.finanza.mensualidades = 0
        this.finanza.ingresos = 0
        this.finanza.gastos = 0
        this.finanza.ganancias = 0
        let detail = document.getElementById("detalle")
        detail.innerHTML = ""
        for (let j of mensualidades_listado) {
            // let item = {}
            if (hol.value.split("-")[0] == j.fecha_inicio_año && hol.value.split("-")[1] == j.fecha_inicio_mes) {
                console.log(hol.value.split())
                detail.innerHTML +=
                    `<tr>
                        <td class="text-center"> ${j.cliente} </td>
                        <td class="text-center"> 
                        ${j.fecha_inicio_año} - ${j.fecha_inicio_mes} - ${j.fecha_inicio_dia} </td>
                    </tr>`
                this.finanza.mensualidades += 1
                this.finanza.ingresos += j.precio

            }
        }
        document.getElementById("mensualidades").value = this.finanza.mensualidades
    }


    guardar_registros(hol) {
        this.finanza.action = document.querySelector('[name=action]').value
        let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        this.finanza.anio = hol.value.split("-")[0]
        this.finanza.mes = hol.value.split("-")[1]
        console.log(this.finanza)
        const grabarFinanza = async (url) => {

            try {
                const res = await fetch(url,
                    {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf,
                        },
                        body: JSON.stringify(this.finanza)
                    });
                const post = await res.json();

            } catch (error) {
                console.log("error=>", error);
                alert(error)
            }
        };
        grabarFinanza(this.save).then(() => {
            location.href = '/finanzas/detalle_finanzas/'
            return false
        })
    }

}

document.addEventListener('DOMContentLoaded', (e) => {
    let Datos_Finanzas = new Finanzas(save)
    let mensualidades_listado = []
    let maquinarias_listado = Datos_Finanzas.CrearList(maquinaria)
    let instrumento_listado = Datos_Finanzas.CrearList(instrumento)
    let hol = document.getElementById("fecha_año_mes")


    mensualidad.forEach((valor) => {
        let REGISTRO = {}
        REGISTRO.cliente = valor.cliente
        REGISTRO.precio = parseFloat(valor.precio)
        REGISTRO.fecha_inicio_año = valor.fecha_inicio.split("-")[0]
        REGISTRO.fecha_inicio_mes = valor.fecha_inicio.split("-")[1]
        REGISTRO.fecha_inicio_dia = valor.fecha_inicio.split("-")[2]

        mensualidades_listado = [...mensualidades_listado, REGISTRO]
        //acumular_todo lo que tengo en la variable

    })
    if (document.querySelector('[name=action]').value == 'edit') {
        hol.value = editar_finanzas.anio + '-' + editar_finanzas.mes
        Datos_Finanzas.GenerarMensualidades(mensualidades_listado, hol)
        Datos_Finanzas.GenerarGastos(maquinarias_listado, hol)
        Datos_Finanzas.GenerarGastos(instrumento_listado, hol)
        let select_fech = document.getElementById("fecha_año_mes")
        select_fech.setAttribute("disabled", "true")
    }

    hol.addEventListener('change', (e) => {

            Datos_Finanzas.GenerarMensualidades(mensualidades_listado, hol)
            Datos_Finanzas.GenerarGastos(maquinarias_listado, hol)

        }
    )
    const btn = document.getElementById("boton-guardar")
    btn.addEventListener('click', (e) => {
        e.preventDefault()
        Datos_Finanzas.guardar_registros(hol)

    })


})






