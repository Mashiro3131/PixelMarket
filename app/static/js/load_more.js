document.addEventListener('DOMContentLoaded', function () {
 
    const btn = document.getElementById('load-more-btn');
 
    if (!btn) return;
 
    // Page courante — commence à 2 car la page 1 est déjà chargée
    let currentPage = 2;
 
    btn.addEventListener('click', async function () {
 
        btn.textContent = 'Chargement...';
        btn.disabled = true;
 
        try {
            // Récupère les oeuvres de la page suivante depuis Flask
            const response = await fetch(
                `/artworks?page=${currentPage}&ajax=1`
            );
 
            if (!response.ok) throw new Error('Erreur réseau');
 
            const data = await response.json();
 
            // Ajoute les nouvelles cards à la fin de la grille
            const grid = document.getElementById('artworks-grid');
            grid.insertAdjacentHTML('beforeend', data.html);
 
            currentPage++;
 
            // Masque le bouton s'il n'y a plus d'oeuvres à charger
            if (!data.has_more) {
                btn.style.display = 'none';
            } else {
                btn.textContent = 'Charger plus';
                btn.disabled = false;
            }
 
        } catch (error) {
            console.error('Erreur load more :', error);
            btn.textContent = 'Erreur — réessayer';
            btn.disabled = false;
        }
    });
});