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
}); 