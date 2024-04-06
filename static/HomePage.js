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
function searchBenevoles(event) {
    // Prevent default form submission
    event.preventDefault();

    // Get the search query from the input field
    var searchQuery = document.querySelector('.search-bar input').value;

    // Fetch the search results from the server
    fetch('/search?q=' + searchQuery)
        .then(response => {
            // Check if the response is successful
            if (response.ok) {
                // If successful, reload the page to show the search results
                window.location.href = '/search?q=' + searchQuery;
            } else {
                // If not successful, display an error message
                console.error('Error:', response.status);
            }
        })
        .catch(error => console.error('Error:', error));
}


// Add event listener to the form submission
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("search-form").addEventListener('submit', searchBenevoles);
});


