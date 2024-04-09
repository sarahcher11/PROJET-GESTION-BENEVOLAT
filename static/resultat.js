document.addEventListener('DOMContentLoaded', function() {

    // Écouter l'événement de soumission du formulaire de recherche
    document.getElementById('search-form1').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêcher le formulaire d'être soumis normalement

        // Récupérer le terme de recherche
        var searchQuery = document.getElementById('search-input1').value;

        // Effectuer une redirection vers la page de résultats de recherche avec le terme de recherche comme paramètre
        window.location.href = '/search?name=' + encodeURIComponent(searchQuery);
    });
});