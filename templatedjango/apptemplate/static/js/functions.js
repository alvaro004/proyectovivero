
function verificar() {
  table = document.getElementsByClassName('tabla_compras')
  console.log(table.length)


  ocultar = document.getElementsByTagName('a')

  if (table.length > 0) {

    for (var i = 0; i < ocultar.length; i++) {

      ocultar[i].setAttribute('onclick', 'alerta()')
      ocultar[i].removeAttribute('href')
    }
  }

}
function alerta() {
  alert('Por favor registre la compra para continuar')
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
    // aca se detecta que clase se clickeo para mostrar
    console.log(cantidad.length)

    // en esta condicion se pregunt si se realiza click en el boton productos
    if (li_value == "productos") {
      for (var i = 0; i < cantidad.length; i++) {
        document.getElementsByClassName('productos')[i].style.display = "block";
      }
    } else if (li_value == "insumos") {
      document.querySelector("." + li_value).style.display = "block";
    } else {
      console.log("");
    }
  });
}


// codigo para filtrar los productos y para cambiar el value de un input que e enviara en el form de
// los productos a cargar

// en esta funcion se extrae los datos del select y se dividen en dos para luego separarlos 
// y convertirlos en array que luego se utilizara para iterar y comparar con los productos 


function cambiar(mensaje) {
  var separar_mensaje = mensaje.split('-/');

  separar_mensaje = separar_mensaje[0];

  cambiar_value = document.getElementById('id_producto');

  if (cambiar_value.value) {
    cambiar_value.value = separar_mensaje;
  }
  // cambiar_value.value = separar_mensaje

  console.log(cambiar_value.value);
}

function filtrar(mensaje)
{
    var productos = document.getElementsByClassName('nombre_productos');
    var select = document.getElementById('select_default');

    // restableciendo el select

    select.selectedIndex = 0;
         
    var separate_productos = '';
    var var_temporal;
    var separate_final;
    var longitud = productos.length + 1;

    for (var i = 0; i < productos.length; i++)
    {
       var_temporal = productos[i].value.split("-");
       separate_productos += var_temporal[1];
           
    }
        
    separate_final = separate_productos.split('/');
        
    separate_final = separate_final.splice(1,longitud);


    for (var j = 0; j < productos.length; j ++)
    {
        // console.log(separate_final[j]);
        if(mensaje == separate_final[j])
        {
            productos[j].style.display = 'block';
        }
        // else
        // {
        //     productos[j].style.display = 'none';
            
        // }
    }
    
}


function filtrar_de_nuevo(mensaje,productos,select)
{    
    // restableciendo el select
    
    select.selectedIndex = 0;
    
    var separate_productos = '';
    var var_temporal;
    var separate_final;
    var longitud = productos.length + 1
    
    for (let i = 0; i < productos.length; i++)
    {
        var_temporal = productos[i].value.split("-");
        separate_productos += var_temporal[1];
        
    }
    
    separate_final = separate_productos.split('/');
    
    separate_final = separate_final.splice(1,longitud);
    
    // mensaje = toString(mensaje)
    
    for (let j = 0; j < productos.length; j ++)
    {
      if(mensaje == separate_final[j])
      {
          console.log(separate_final[j]);
            // productos[j].setAttribute('selected','selected')
            productos[j].style.display = 'block';
            // console.log('entro')
        }
        else
        {
            productos[j].style.display = 'none';
            
        }
    }
}