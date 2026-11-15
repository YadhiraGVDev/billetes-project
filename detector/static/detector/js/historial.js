document.addEventListener('DOMContentLoaded', function () {
    const chips = document.querySelectorAll('#filter-chips .chip');
    const cards = document.querySelectorAll('#history-list .history-card');
    const searchInput = document.getElementById('search-input');

    // Filtro por chips
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            const filter = chip.dataset.filter;
            cards.forEach(card => {
                if (filter === 'all' || card.dataset.bill === filter) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Búsqueda por texto
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const q = searchInput.value.toLowerCase();
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(q) ? 'flex' : 'none';
            });
        });
    }
});