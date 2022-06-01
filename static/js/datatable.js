$(document).ready(function (mensaje) {

    var tabla_producto = $('#tabla_producto').DataTable({
      extend: 'collection',
      processing: true,
      'processing': true,
      "ordering": false,
      "order": [[ 0, "desc" ]],
      "bDestroy": true,
      buttons: [
        'csv',
        'excel',
        {
          extend: 'pdf',
        },
        {
          extend: 'print',
        }
  
      ],
    });
    tabla_producto.buttons(0, null).containers().appendTo('#Menu_herramienta_producto');

    var tabla_facturacion = $('#tabla_facturacion').DataTable({
      extend: 'collection',
      processing: true,
      'processing': true,
      "ordering": false,
      "order": [[ 0, "desc" ]],
      buttons: [
        'csv',
        'excel',
        {
          extend: 'pdf',
        },
        {
          extend: 'print',
        }
  
      ],
    });
    tabla_facturacion.buttons(0, null).containers().appendTo('#Menu_herramienta_facturacion');

    var tabla_inventario = $('#tabla_inventario').DataTable({
      extend: 'collection',
      processing: true,
      'processing': true,
      "ordering": false,
      "order": [[ 0, "desc" ]],
      buttons: [
        'csv',
        'excel',
        {
          extend: 'pdf',
        },
        {
          extend: 'print',
        }
  
      ],
    });
    tabla_inventario.buttons(0, null).containers().appendTo('#Menu_herramienta_inventario');
});