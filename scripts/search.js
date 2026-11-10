// ===========================
//  ПРОСТОЙ ПОИСК ПО ФИЛЬМАМ
// ===========================

const input = document.getElementById('search-input');
const sections = document.querySelectorAll('.movie-section');

input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    const isSearching = query.length > 0;

    sections.forEach(section => {
        const cards = section.querySelectorAll('.card');
        const heading = section.querySelector('h2');
        let visibleCount = 0;

        cards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();

            if (title.includes(query)) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Заголовок секции скрываем, как только начался поиск
        heading.style.display = isSearching ? 'none' : 'block';

        // Секцию целиком скрываем, если в ней нет подходящих карточек
        section.style.display = visibleCount === 0 ? 'none' : 'block';
    });
});