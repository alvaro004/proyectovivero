// document.addEventListener("DOMContentLoaded", () => {
//     // Escuchamos el click del botón
//     const $boton = document.querySelector("#btnCrearPdf");
//     $boton.addEventListener("click", () => {
//         ocultar = document.getElementsByClassName("ocultar");
//         dataTables_length = document.getElementsByClassName("dataTables_length")[0];
//         formcontrolsm = document.getElementsByClassName("dataTables_filter")[0];
//         membreteContenedor = document.getElementById("membreteContenedor");
//         membreteContenedor.style.display = 'block';
//         for (let i = 0; i < ocultar.length; i++) {
            
//             ocultar[i].style.display = 'none';
            
//         }
//         dataTables_length.style.display = 'none';
//         formcontrolsm.style.display = 'none';
        
//         const $elementoParaConvertir = document.getElementById("estos"); // <-- Aquí puedes elegir cualquier elemento del DOM
//         html2pdf()
//             .set({
//                 margin: 1,
//                 filename: 'Reporte.pdf',
//                 image: {
//                     type: 'jpeg',
//                     quality: 0.98
//                 },
//                 html2canvas: {
//                     scale: 3, // A mayor escala, mejores gráficos, pero más peso
//                     letterRendering: true,
//                 },
//                 jsPDF: {
//                     unit: "in",
//                     format: "a2",
//                     orientation: 'portrait' // landscape o portrait
//                 }
//             })
//             .from($elementoParaConvertir)
//             .save()
//             .catch(err => console.log(err));

//             setTimeout(function(){ 

//                 for (var j = 0; j < ocultar.length; j++) {
                    
//                     ocultar[j].style.display = '';
                    
//                 }

//                 membreteContenedor.style.display = '';
//                 dataTables_length.style.display = '';
//                 formcontrolsm.style.display = '';

//             }, 100);

            
//     });

// });

