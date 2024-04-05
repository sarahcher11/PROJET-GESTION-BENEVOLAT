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


