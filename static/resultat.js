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
document.addEventListener('DOMContentLoaded', function() {
    // Écouter l'événement de soumission du formulaire de recherche
    document.getElementById('search-form2').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêcher le formulaire d'être soumis normalement

        // Récupérer le terme de recherche
        var searchQuery = document.getElementById('search-input2').value;

        // Effectuer une redirection vers la page de résultats de recherche avec le terme de recherche comme paramètre
        window.location.href = '/search1?name=' + encodeURIComponent(searchQuery);
    });
});


const selectbtn = document.querySelector(".select-btn");
const items = document.querySelectorAll(".item");

selectbtn.addEventListener("click", () => {
    selectbtn.classList.toggle("open");
});

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");
    });
});


const selectbtnskill = document.querySelector(".select-btnskill");
const itemsskill = document.querySelectorAll(".itemskill");

selectbtnskill.addEventListener("click", () => {
    selectbtnskill.classList.toggle("openskill");
});

itemsskill.forEach(itemskill => {
    itemskill.addEventListener("click", () => {
        itemskill.classList.toggle("checkedskill");
    });
});





const form = document.getElementById("myForm");

form.addEventListener("submit", function(event) {
    event.preventDefault(); // Empêcher le rechargement de la page

    // Récupérer les valeurs sélectionnées
    const selectedSkills = [];
    document.querySelectorAll(".itemskill.checkedskill .item-textskill").forEach(skill => {
        selectedSkills.push(skill.textContent.trim());
    });

    const selectedInterests = [];
    document.querySelectorAll(".item.checked .item-text").forEach(interest => {
        selectedInterests.push(interest.textContent.trim());
    });

    const selectedSexe = document.getElementById("sexe").value;
    const selectedAge = document.getElementById("age").value;

    // Construire la chaîne de requête
    var queryString = "skills=" + encodeURIComponent(selectedSkills.join(',')) +
                      "&interests=" + encodeURIComponent(selectedInterests.join(',')) +
                      "&sexe=" + encodeURIComponent(selectedSexe) +
                      "&age=" + encodeURIComponent(selectedAge);

    // Construire l'URL avec la chaîne de requête
    var url = '/filtrer?' + queryString;

    // Rediriger vers l'URL construit
    window.location.href = url;
});

