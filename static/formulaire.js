const selectbtn = document.querySelector(".select-btn");
const items = document.querySelectorAll(".item");
const items_skills=document.querySelectorAll(".item-skills")

selectbtn.addEventListener("click", () => {
    selectbtn.classList.toggle("open");
});

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");
    });
});

items_skills.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked")
    })
})
document.addEventListener('DOMContentLoaded', function() {
    const selectBtnSkills = document.querySelector('.select-btn-skills');
    const skillsList = document.querySelector('.list-items-skills');

    selectBtnSkills.addEventListener('click', function() {
        selectBtnSkills.classList.toggle('open');
        skillsList.classList.toggle('show');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche l'envoi du formulaire pour le moment

        const interestsChecked = [];
        const skillsChecked = [];

        const interestsItems = document.querySelectorAll('.list-items .item');
        const skillsItems = document.querySelectorAll('.list-items-skills .item-skills');

        interestsItems.forEach(item => {
            if (item.classList.contains('checked')) {
                interestsChecked.push(item.querySelector('.item-text').textContent.trim());
            }
        });

        skillsItems.forEach(item => {
            if (item.classList.contains('checked')) {
                skillsChecked.push(item.querySelector('.item-text').textContent.trim());
            }
        });

        // Créer et ajouter les champs cachés pour les intérêts et les compétences
        const interestsInput = document.createElement('input');
        interestsInput.setAttribute('type', 'hidden');
        interestsInput.setAttribute('name', 'interests');
        interestsInput.setAttribute('value', JSON.stringify(interestsChecked));
        form.appendChild(interestsInput);

        const skillsInput = document.createElement('input');
        skillsInput.setAttribute('type', 'hidden');
        skillsInput.setAttribute('name', 'skills');
        skillsInput.setAttribute('value', JSON.stringify(skillsChecked));
        form.appendChild(skillsInput);

        // Maintenant que les champs cachés sont ajoutés, soumettez le formulaire
        form.submit();
    });
});
