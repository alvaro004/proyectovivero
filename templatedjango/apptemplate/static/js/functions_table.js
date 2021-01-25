// // codigo para filtrar los productos y para cambiar el value de un input que e enviara en el form de
// // los productos a cargar

// // en esta funcion se extrae los datos del select y se dividen en dos para luego separarlos 
// // y convertirlos en array que luego se utilizara para iterar y comparar con los productos 

function filtro(primer_select, segundo_select) {

    for (var i = 0; i < segundo_select.length; i++) {
      valor = segundo_select[i].value
      valor = valor.split('-')
      valor = valor[1]

      console.log(primer_select.value)
  
      if (primer_select.value == valor) {

        // console.log('entro en el if')
  
        segundo_select[i].style.display = '';
        segundo_select[i].setAttribute('selected', 'selected')
  
      }
      else {
        segundo_select[i].style.display = 'none';
        segundo_select[i].removeAttribute('selected', 'selected')
  
  
      }
    }
  
  }
  
  // funcion para cambiar el valor del input del ual se va a enciar el id del nombre del producto
function cambiar_enviar(valor, enviar) {
    enviar.value = valor.value.split('-')[0];
  }
  
  // funcion para establecer un valor predeterminado por el valor de la tabla que contiene los datos a editar
  function filtro_editar(valores, valor_tabla) {
    // console.log(valor_tabla.innerHTML)

    console.log(valores);
    console.log(valor_tabla);
      for (var i = 0; i < valores.length; i++) {
  
        // console.log(valores[i].value)
        if (valores[i].value == valor_tabla.innerText) {
  
        valores[i].setAttribute('selected', 'selected');
        }
        else {
  
        valores[i].removeAttribute('selected', 'selected');
        }
    }
    } 
  
  // funcion para filtrar los nombres por categoria del select del modal para editar
  function filtro_editar_con_select(select_categoria,select_nombres){
      // console.log(select_categoria.value)
      
      for (var i =0 ; i < select_nombres.length; i ++)
      {
        select_nombres.selectedIndex = 0;
        valor = select_nombres[i].value.split("-")[1];
        
        if(select_categoria.value == valor)
        {
          select_nombres[i].style.display = 'block';   
        }
        else{   
          select_nombres[i].style.display = 'none';
          }
      }
  }
  
  // funcion para filtrar los nombres por la categoria de los datos de la tabla
  function filtrar_select_nombre_modal(tabla_nombre,select){
    // console.log(tabla_nombre.innerHTML)
    // console.log(select[1].value)
  
    for (var i = 0; i < select.length; i ++)
    {
        if(tabla_nombre.innerHTML == select[i].innerHTML )
        {
            select[i].setAttribute('selected', 'selected');
        }
        else
        {
            select[i].removeAttribute('selected', 'selected');
        }
  
        // console.log(tabla_nombre.innerHTML)
  
    }
  }

  function confirmar_logout(){
    confirm(' Desea cerrar la sesion?. ')
  }