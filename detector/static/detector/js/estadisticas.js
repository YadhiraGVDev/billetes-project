document.addEventListener("DOMContentLoaded", () => {
    const elementoDatos = document.getElementById("datos-grafico");
    const canvas = document.getElementById("donutChart");
    const legendContainer = document.getElementById("chart-legend");

    if (!elementoDatos || !canvas || !legendContainer) {
        console.error("No se encontraron los elementos de la gráfica.");
        return;
    }

    const datos = JSON.parse(elementoDatos.textContent);

    if (!datos || datos.length === 0) {
        canvas.parentElement.innerHTML =
            '<p style="text-align:center; color:#94a3b8;">Sin datos aún</p>';
        legendContainer.innerHTML = "";
        return;
    }

    const coloresPorDenominacion = {
        20: "#3685A8",
        50: "#A34D9B",
        100: "#D65345",
        200: "#548A50",
        500: "#3479B9",
        1000: "#73717D"
    };

    function obtenerColor(nombre) {
        const denominacion = Number(
            String(nombre).replace(/[^\d]/g, "")
        );

        return coloresPorDenominacion[denominacion] || "#9CA3AF";
    }

    const labels = datos.map(item => item.nombre);
    const values = datos.map(item => Number(item.total));
    const colores = datos.map(item => obtenerColor(item.nombre));

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colores,
                borderColor: "#FFFFFF",
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const item = datos[context.dataIndex];
                            return ` ${item.nombre}: ${item.total} billetes (${item.porcentaje}%)`;
                        }
                    }
                }
            }
        }
    });

    legendContainer.innerHTML = "";

    datos.forEach((item, index) => {
        const li = document.createElement("li");
        const ladoIzquierdo = document.createElement("div");
        ladoIzquierdo.className = "legend-left";

        const indicador = document.createElement("span");
        indicador.className = "legend-color";
        indicador.style.backgroundColor = colores[index];

        const nombre = document.createElement("span");
        nombre.textContent = item.nombre;

        const porcentaje = document.createElement("span");
        porcentaje.className = "legend-percent";
        porcentaje.textContent = `${item.porcentaje}%`;

        ladoIzquierdo.appendChild(indicador);
        ladoIzquierdo.appendChild(nombre);

        li.appendChild(ladoIzquierdo);
        li.appendChild(porcentaje);

        legendContainer.appendChild(li);
    });
});