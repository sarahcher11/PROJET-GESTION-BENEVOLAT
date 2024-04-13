let number1 =document.getElementById("number1");
let counter1=0;
setInterval(()=>{
    if(counter1==200){
        clearInterval();
    }else{
        counter1+=1;
        number1.innerHTML="+ "+counter1;
    }
},25);

let number2 =document.getElementById("number2");
let counter2=0;
setInterval(()=>{
    if(counter2==200){
        clearInterval();
    }else{
        counter2+=1;
        number2.innerHTML="+ "+counter2;
    }
},25);




// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {
    // Écouter l'événement de soumission du formulaire de recherche
    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêcher le formulaire d'être soumis normalement

        // Récupérer le terme de recherche
        var searchQuery = document.getElementById('search-input').value;

        // Effectuer une redirection vers la page de résultats de recherche avec le terme de recherche comme paramètre
        window.location.href = '/search?name=' + encodeURIComponent(searchQuery);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Écouter l'événement de soumission du formulaire de recherche
    document.getElementById('search-formpro').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêcher le formulaire d'être soumis normalement

        // Récupérer le terme de recherche
        var searchQuery = document.getElementById('search-inputpro').value;

        // Effectuer une redirection vers la page de résultats de recherche avec le terme de recherche comme paramètre
        window.location.href = '/searchpro?name=' + encodeURIComponent(searchQuery);
    });
});


  
  document.addEventListener('DOMContentLoaded', function() {
    var profileLink = document.getElementById('profile-link');
    var subWrap = document.querySelector('.sub-wrap');

    // Fonction pour afficher la sub-wrap
    function showSubWrap() {
        subWrap.style.display = 'block';
    }

    // Fonction pour masquer la sub-wrap
    function hideSubWrap() {
        subWrap.style.display = 'none';
    }

    // Afficher la sub-wrap lors du survol du profil
    profileLink.addEventListener('mouseenter', showSubWrap);

    // Masquer la sub-wrap lors du survol d'autre éléments
    subWrap.addEventListener('mouseleave', hideSubWrap);
});
