$(document).ready(function () {

    $('table.tablita').DataTable({
      responsive: true,
      "bInfo" : false,
      "language": {
        "url": "https://cdn.datatables.net/plug-ins/1.10.20/i18n/Spanish.json"
      },
      "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "Todo"]]
      

      //Otra forma de cambiar el idioma
      // "language": {
          //     "lengthMenu": "Mostrando _MENU_ ",
          //     "zeroRecords": "No se encontro nada - ¡Lo siento!",
          //     "info": "Mostrando pagina _PAGE_ de _PAGES_",
          //     "infoEmpty": "No hay registros disponibles",
          //     "infoFiltered": "(filtrando de _MAX_ registros totales)",
          //      "search": "Busqueda:",
          //      "paginate": {
            //          "previous": "Anterior",
            //          "next": "Siguiente"
            
            //      }
            //  }
            
          });
          
        });
        
      $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
      });
