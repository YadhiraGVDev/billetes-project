document.addEventListener("DOMContentLoaded", () => {
    // 1. Recuperar los datos que enviamos desde Django
    const datosJSON = document.getElementById('datos-grafico').textContent;
    const datos = JSON.parse(datosJSON);

    const canvas = document.getElementById('donutChart');
    const legendContainer = document.getElementById('chart-legend');

    // Si no hay datos, mostramos un mensaje
    if (datos.length === 0) {
        canvas.parentElement.innerHTML = '<p style="text-align:center; font-size:12px; color:#94a3b8; margin-top:40px;">Sin datos aún</p>';
        return;
    }

    // 2. Preparar arrays para Chart.js
    const labels = datos.map(item => item.nombre);
    const values = datos.map(item => item.total);
    const percentages = datos.map(item => item.porcentaje);

    // Paleta de colores (Azul, Verde, Rojo, Morado, Naranja, etc.)
    const colores = ['#0b3b60', '#10b981', '#8b5cf6', '#ef4444', '#f59e0b', '#06b6d4'];

    // 3. Crear el gráfico de Dona
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colores,
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverOffset: 4
            }]
        },
        options: {
            cutout: '70%', // Hace el hueco del centro (70%)
            plugins: {
                legend: { display: false } // Ocultamos la leyenda por defecto (usaremos la nuestra)
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // 4. Llenar la leyenda personalizada (al lado del gráfico)
    legendContainer.innerHTML = ''; // Limpiar
    
    datos.forEach((item, index) => {
        const li = document.createElement('li');
        
        // Asignamos un color (si hay más de 6, repetimos la paleta)
        const color = colores[index % colores.length]; 

        li.innerHTML = `
            <div class="legend-left">
                <span class="legend-color" style="background-color: ${color};"></span>
                <span>${item.nombre}</span>
            </div>
            <span class="legend-percent">${item.porcentaje}%</span>
        `;
        
        legendContainer.appendChild(li);
    });
});