let numero = 0;
let texto = document.getElementById("tiempo")

function incremento(){
    numero++;
    incrementoID = setTimeout(incremento, 1000);
    texto.innerHTML = `${numero}`
}

let incrementoID = setTimeout(incremento, 1000);