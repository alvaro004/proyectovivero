function verificar(){
    table = document.getElementsByTagName('td')

    if(table.length < 1){
        ocultar = document.getElementsByClassName('bg-light')

        for(var i =0; i < ocultar.length; i++)
        {

            ocultar[i].setAttribute('href','')
        }
    }
}