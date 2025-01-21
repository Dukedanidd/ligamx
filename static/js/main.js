document.addEventListener('DOMContentLoaded', function() {
    // Manejo de la navegación
    const menuItems = document.querySelectorAll('.menu-item');
    const views = document.querySelectorAll('.view-container');

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remover clase active de todos los items
            menuItems.forEach(i => i.classList.remove('active'));
            // Agregar clase active al item seleccionado
            this.classList.add('active');

            // Mostrar la vista correspondiente
            const viewId = this.dataset.view + '-view';
            views.forEach(view => {
                view.classList.add('hidden');
                if (view.id === viewId) {
                    view.classList.remove('hidden');
                }
            });
        });
    });

    // Manejo del filtro de temporada
    const seasonFilter = document.getElementById('season-filter');
    if (seasonFilter) {
        seasonFilter.addEventListener('change', function() {
            // Aquí puedes agregar la lógica para actualizar los datos
            // según la temporada seleccionada
        });
    }

    // Crear el gráfico
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('standings-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Puntos',
                        data: data.data,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Puntos por Equipo'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
}); 