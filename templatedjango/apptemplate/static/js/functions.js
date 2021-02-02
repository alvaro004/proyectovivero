
function verificar() {
  table = document.getElementsByClassName('tabla_compras')
  // console.log(table.length)


  ocultar = document.getElementsByTagName('a')

  if (table.length > 0) {

    for (var i = 0; i < ocultar.length; i++) {

      ocultar[i].setAttribute('onclick', 'alerta()')
      ocultar[i].removeAttribute('href')
    }
  }

}
function alerta() {
  alert('¡Por Favor Registre la Compra o elimine los Productos para Continuar!')
}

window.onload = function () {
  verificar()
};





// SCRIPT PARA ES PARA EL HIDE Y SHOW EN LA VISTA DE PRODUCCION


var li_elements = document.querySelectorAll(".boton");
var item_elements = document.querySelectorAll(".item");
for (var i = 0; i < li_elements.length; i++) {

  // en esta parte se escuchan los clicks de las clases 

  li_elements[i].addEventListener("click", function () {
    // aca se remueve el active del primer elemento
    // li_elements.forEach(function(li) {
    //   li.classList.remove("active");
    // });
    // aca se activan los estilos de los botones
    // this.classList.add("active");

    // luego se adquieren los valores de las listas en las que se hacen click para luego mostrar el contenido
    var li_value = this.getAttribute("data-li");

    // luego se agrega el estilo de display none a todos los divs para luego mostrar el que se clickea
    item_elements.forEach(function (item) {
      item.style.display = "none";
    });

    // aca se mide la longitud de los elementos que contienen la clase productos para luego mostrarlos cuando de realiza click en el boton de productos
    cantidad = document.getElementsByClassName('productos')
    cantidad2 = document.getElementsByClassName('insumos')
    // aca se detecta que clase se clickeo para mostrar
    // console.log(cantidad.length)

    // en esta condicion se pregunt si se realiza click en el boton productos
    if (li_value == "productos") {
      for (var i = 0; i < cantidad.length; i++) {
        document.getElementsByClassName('productos')[i].style.display = "block";
      }
    } else if (li_value == "insumos") {
      for (var i = 0; i < cantidad2.length; i++) {
        document.getElementsByClassName('insumos')[i].style.display = "block";
      }
      // document.querySelector("." + li_value).style.display = "block";
    } else {
      console.log("");
    }
  });
}


function send_form(form){
  form.submit();
}

boton_logout = document.getElementById('logout_button');

boton_logout.onclick = function(){
  // console.log('entro')
  if (confirm('¿Desea cerrar la sesión? ')) {
    window.location = 'logout';
  }
}