function verificar() {
    table = document.getElementsByTagName('td')
    console.log(table.length)


    ocultar = document.getElementsByClassName('bg-light')

    if(table.length > 0){

        for (var i = 0; i < ocultar.length; i++) {

            ocultar[i].setAttribute('href', '')
        }
    }

}

window.onload = function () {
    verificar()
};