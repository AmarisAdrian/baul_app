
var array_host = ['http://localhost:8000/','http://127.0.0.1:8000','https://baul-erp.herokuapp.com/']
$(document).ready(function () {
    var URLactual = window.location.href;
    if (array_host.includes(URLactual)) {
        let url = $("#chart_venta_anual").data("url-venta");
        let csrftoken = $("input[name=csrfmiddlewaretoken").val()
        var data = { 'csrfmiddlewaretoken': csrftoken }
        let datos;
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            dataType: "json",
            complete: function (data) {
                if (data.responseJSON.code == 200 && data.responseJSON.status == "success") {
                    datos = data.responseJSON.datos;
                    GraficaVentaAnual(datos)
                }
                if (data.responseJSON.code == 200 && data.responseJSON.status == "error") {

                }

            }
        });
        return false;
    }
});

$(document).ready(function () {
    var URLactual = window.location.href;
    if (array_host.includes(URLactual) ) {
        let url = $("#chart_venta_producto").data("url-venta");
        let csrftoken = $("input[name=csrfmiddlewaretoken").val()
        var data = { 'csrfmiddlewaretoken': csrftoken }
        let datos;
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            dataType: "json",
            complete: function (data) {
                if (data.responseJSON.code == 200 && data.responseJSON.status == "success") {
                    datos = data.responseJSON.datos;
                    console.log(datos)
                    GraficaProductoVendido(datos)
                }
                if (data.responseJSON.code == 200 && data.responseJSON.status == "error") {

                }

            }
        });
        return false;
    }
});

//CALCULAR PRECIO CON DESCUENTO 
$("#id_descuento").keydown(function (e) {
    if (e.which == 13 || e.which == 9) {
        e.preventDefault();
        let valor_descuento = $("#id_valor_descuento").val();
        let descuento = $("#id_descuento").val();
        let valor_venta = $("#id_valor_venta").val();
        let precio;
        if (descuento == '' && valor_descuento == '') {
            descuento = 0;
            $('#id_valor_descuento').val(descuento);
        } else {
            precio = (valor_venta - descuento);
            $('#id_valor_descuento').val(precio);
        }
    }
});

//CONSULTAR STOCK
$("#frm_consultar_stock").bind("submit", function () {
    let url = $("#frm_consultar_stock").data("url");
    var data = new FormData(this);
    $.ajax({
        type: $(this).attr("method"),
        url: url,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        data: data,
        complete: function (data) {
            if (data.responseJSON.code == 200 && data.responseJSON.status == "ok") {
                $("#msj-stock").removeClass('alert alert-danger d-block').addClass('alert alert-danger d-none').text('');
                $("#tabla-movimiento").removeClass(' col-xl-12 col-lg-12 col-md-12 col-sm-12  tabla-movimiento d-none')
                    .addClass(' col-xl-12 col-lg-12 col-md-12 col-sm-12  tabla-movimiento d-block')
                    TablaStock(data.responseJSON.stock);

            }
            if (data.responseJSON.code == 200 && data.responseJSON.status == "error") {
                $("#tabla-movimiento").removeClass(' col-xl-12 col-lg-12 col-md-12 col-sm-12  tabla-movimiento d-block')
                    .addClass(' col-xl-12 col-lg-12 col-md-12 col-sm-12  tabla-movimiento d-none')
                $("#msj-stock").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text(data.responseJSON.msj);
            }

        }
    });
    return false;
});
//GENERAR TABLA DE STOCK
 let TablaStock = (datos) => {
    $("#tabla_stock > tbody").empty()
     let tabla = "";
     for (let i = 0 ; i < datos.length ; i++){
       tabla = '<tr>'+
                    '<td>' + datos[i].fecha_movimiento + '</td>'+
                    '<td>' + new Intl.NumberFormat("es-CO").format(datos[i].precio_unitario) + '</td>'+
                    '<td>' + new Intl.NumberFormat("es-CO").format(datos[i].valor)+ '</td>'+
                    '<td>' + new Intl.NumberFormat("es-CO").format(datos[i].valor_venta)+ '</td>'+
                    '<td>' +  new Intl.NumberFormat("es-CO").format(datos[i].descuento) + '</td>'+
                    '<td>' + datos[i].cantidad + '</td>'+
                    '<td>' + new Intl.NumberFormat("es-CO").format(datos[i].valor_descuento) + '</td>'+
                    '<td>' + datos[i].motivo + '</td>'+
                '</tr>';
        $('#tabla_stock > tbody').append(tabla);
     }
    //  $('#tabla_stock').DataTable({
    //     'bDestroy': true,
    // });
 }

//CONSULTAR CLIENTE EN FACTURACION
$("#frm_consultar_cliente").bind("submit", function () {
    let url = $("#frm_consultar_cliente").data("url");
    var data = new FormData(this);
    $.ajax({
        type: $(this).attr("method"),
        url: url,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        data: data,
        complete: function (data) {
            if (data.responseJSON.code == 200 && data.responseJSON.status == "ok") {
                $("#msj-cliente").removeClass('alert alert-danger d-block').addClass('alert alert-danger d-none').text('');
                $('#id_nombre').val(data.responseJSON.datos[0].nombre);
                $('#id_apellido').val(data.responseJSON.datos[0].apellido);
                $('#id_direccion').val(data.responseJSON.datos[0].direccion);
                $('#id_telefono').val(data.responseJSON.datos[0].telefono);
                $('#id_email').val(data.responseJSON.datos[0].email);
            }
            if (data.responseJSON.code == 200 && data.responseJSON.status == "error") {
                $("#msj-cliente").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text(data.responseJSON.msj);
                $('#id_nombre').val('');
                $('#id_apellido').val('');
                $('#id_direccion').val('');
                $('#id_telefono').val('');
                $('#id_email').val('');
            }
        },
        fail: function (data) {
            console.log(data);
        },
    });
    return false;
});

//CONSULTAR PRODUCTO EN FACTURACION
$("#frm_consultar_producto").bind("submit", function () {
    let url = $("#frm_consultar_producto").data("url");
    var data = new FormData(this);
    $.ajax({
        type: $(this).attr("method"),
        url: url,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        data: data,
        complete: function (data) {
            if (data.responseJSON.code == 200 && data.responseJSON.status == "ok") {
                $("#msj-producto").removeClass('alert alert-danger d-block').addClass('alert alert-danger d-none').text('');
                $('#id_valor').val(data.responseJSON.datos[0].valor_venta);
                $('#id_id_producto').val(data.responseJSON.datos[0].descripcion);
                $('#id_cantidad').attr('maxlength', data.responseJSON.datos[0].cantidad);
                $('#id_cantidad').val('1');
                $('#CheckoutDescuento').val(data.responseJSON.datos[0].valor_descuento);
                $('#CheckoutDescuento').attr("disabled", false)
                $('#CheckoutEnvio').attr("disabled", false)
            }
            if (data.responseJSON.code == 200 && data.responseJSON.status == "error") {
                $("#msj-producto").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text(data.responseJSON.msj);
            }
            if (data.responseJSON.code == 500) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                })
            }
        },
        fail: function (data) {
            console.log(data);
        },
    });
    return false;
});

//VALIDAR QUE LA CANTIDAD NO SEA MAYOR QUE EL STOCK y MULTIPLICA LA CANTIDAD POR EL PRECIO 
$("#id_cantidad").keydown(function (e) {
    let cantidad = $("#id_cantidad").val();
    let lenght = $('#id_cantidad').attr('maxlength');
    let check_descuento = $("#CheckoutDescuento").is(':checked')
    let valor_venta = $('#id_valor').val();
    let valor_descuento = $('#CheckoutDescuento').val();
    let total = '0';
    if (e.which == 13 || e.which == 9) {
        e.preventDefault();
        let referencia = $("#referencia_producto").val();
        if (referencia == '') {
            cant = 1;
            $('#id_cantidad').val(cant);
        }
        if (cantidad > lenght) {
            $("#msj-producto").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("No hay cantidad suficiente en el stock . Cantidad actual en stock : " + lenght);
        } else {
            if (check_descuento) {
                total = (valor_descuento * cantidad);
                $("#id_subtotal").val(new Intl.NumberFormat('es-CO').format(total));
                $("#id_total").val(new Intl.NumberFormat('es-CO').format(total));
            } else {
                total = (valor_venta * cantidad);
                $("#id_subtotal").val(new Intl.NumberFormat('es-CO').format(total));
                $("#id_total").val(new Intl.NumberFormat('es-CO').format(total));

            }
            $("#msj-producto").removeClass('alert alert-danger d-block').addClass('alert alert-danger d-none').text('');
        }
    }
});


//ACTIVAR DESCUENTO
$("#CheckoutDescuento").change(function (e) {
    const valor_descuento = $('#CheckoutDescuento').val();
    if ($(this).is(':checked')) {
        $('#TxtDescuento').val(valor_descuento);
    } else {
        $('#TxtDescuento').val('');
    }
});

//VALIDAR CARRITO
let Array_carrito = [];
$("#AgregarCarrito").click(function (e) {
    let id_cliente = $("#documento").val();
    let producto = $("#id_id_producto").val();
    let id_subtotal = $("#id_subtotal").val();
    let id_total = $("#id_total").val();
    let envio = $("#TxtEnvio").val();
    let referencia_producto = $("#referencia_producto").val();
    let id_cantidad = $("#id_cantidad").val();
    let id_valor = $("#id_valor").val();
    let TxtDescuento = $("#TxtDescuento").val();
    let remove_class = $("#msj-factura").removeClass('alert alert-danger d-block').addClass('alert alert-danger d-none').text('');
    if (id_cliente == "" || id_cantidad == "" || referencia_producto == "") {
        id_cliente == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("Campo cliente no puede estar vacio") : remove_class
        id_cantidad == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("Campo cantidad no puede estar vacio") : remove_class
        referencia_producto == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("Campo referencia producto no puede estar vacio") : remove_class
        id_subtotal == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("El campo subtotal se encuentra vacio") : remove_class
        id_total == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("El campo total no puede estar vacio") : remove_class
        envio == "" ? $("#msj-factura").removeClass('alert alert-danger d-none').addClass('alert alert-danger d-block').text("El campo envio no puede estar vacio") : remove_class
    } else {
        remove_class
        AgregarCarrito(id_cliente, producto, id_subtotal, id_total, envio, referencia_producto, id_cantidad, id_valor, TxtDescuento);
    }
});

//AGREGAR PRODUCTO AL CARRITO
let total_factura_array;
let AgregarCarrito = (id_cliente, producto, id_subtotal, id_total, envio, referencia_producto, id_cantidad, id_valor, TxtDescuento) => {
    let total_producto = '0';
    if (TxtDescuento == "") {
        TxtDescuento = '0'
        total_producto = (id_cantidad * id_valor);
    } else {
        total_producto = (id_cantidad * TxtDescuento);
    }

    if (Array_carrito.length === 0) {
        id_total = total_producto;
        id_subtotal = total_producto;
        total_factura_array = id_total
        if (id_total <= 100000) {
            envio = '10000';
            $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(10000));
        } else {
            $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(0))
            envio = '0';
        }
    } else {
        for (var i = 0; i < Array_carrito.length; i++) {
            id_total = (Array_carrito[i].id_total + total_producto);
            id_subtotal = (Array_carrito[i].id_total + total_producto);
            Array_carrito[i].id_total = id_total;
            Array_carrito[i].id_subtotal = id_subtotal;
            total_factura_array = id_total;
            if (id_total <= 100000) {
                envio = '10000';
                $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(10000));
            } else {
                $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(0))
                envio = '0';
            }
            Array_carrito[i].envio = envio;
            $("#id_total").val(new Intl.NumberFormat('es-CO').format(id_total));
            $("#id_subtotal").val(new Intl.NumberFormat('es-CO').format(id_total));
        }
    }
    //CREA UN ARRAY CON LOS PRODUCTOS 
    Array_carrito.push({
        'id_cliente': id_cliente,
        'id_subtotal': id_subtotal,
        'id_total': id_total,
        'envio': envio,
        'referencia_producto': referencia_producto,
        'id_cantidad': id_cantidad,
        'id_valor': total_producto,
        'TxtDescuento': TxtDescuento
    });
    $("#tabla-carrito").append(`<tr><td  style="width:500px"> <input style="width:480px" type="text" value="${referencia_producto}-${producto}" class="border-0" name="producto[]" disabled="true"/></td><td  style="width:200px"> <input  style="width:200px" class="border-0" type="text" value="${id_cantidad}" name="cantidad[]" disabled="true"/></td><td> <input type="text" class="valor border-0" value="${total_producto}" id="valor" name="valor[]" disabled="true"/></td><td style="width:200px"> <a  href="#" class="btn_eliminar_item btn btn-danger btn-circle btn-sm" id="btn_eliminar_item" name="btn_eliminar_item" title="Eliminar producto" data-id="#" data-toggle="tooltip" data-placement="top" data-method="DELETE"><i class="fa fa-trash"></i> Eliminar</a></td></tr>`);
    $("#Facturar").removeClass('btn btn-warning d-none').addClass('btn btn-warning d-block');
    $("#Cotizar").removeClass('btn btn-success d-none').addClass('btn btn-success d-block');
    $("#Cancelar").removeClass('btn btn-danger d-none').addClass('btn btn-danger d-block');
    VaciarCamposProducto();
}

//ELIMINA LOS PRODUCTOS DEL CARRITO
let total;
$(document).on('click', '#btn_eliminar_item', function (e) {
    let i = $(this).closest('tr').index();
    if (i !== -1) {
        Array_carrito.splice(i, 1);
    }
    CalcularTotal();
    $(this).parent('td').parent('tr').remove();


});

//CALCULAR TOTAL CUANDO UN ELEMENTO DEL CARRITO ES ELIMINADO
let CalcularTotal = () => {
    let total = 0;
    if (Array_carrito.length > -1) {
        $.each(Array_carrito, (i, value) => {
            total = total + Array_carrito[i].id_valor;
            Array_carrito[i].id_total = total;
            Array_carrito[i].id_subtotal = total;
        });
    }
    if (total <= 100000) {
        $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(10000));
    } else {
        $("#TxtEnvio").val(new Intl.NumberFormat('es-CO').format(0))
    }
    $("#id_total").val(new Intl.NumberFormat('es-CO').format(total));
    $("#id_subtotal").val(new Intl.NumberFormat('es-CO').format(total));
}


//VACIAR CAMPOS
let VaciarCamposProducto = () => {
    $("#referencia_producto").val('');
    $("#id_id_producto").val('');
    $("#id_valor").val('');
    $("#TxtDescuento").val('');
    $("#id_cantidad").val('');
    $("#CheckoutDescuento").prop('checked', false);
    $("#CheckoutDescuento").val('');
}
//VACIAR CAMPOS CLIENTE
let VaciarCamposCliente = () => {
    $("#documento").val('');
    $("#id_nombre").val('');
    $("#id_apellido").val('');
    $("#id_direccion").val('');
    $("#id_telefono").val('');
}

//VACIAR CAMPOS DATOS FACTURA
let VaciarCamposFactura = () => {
    $("#id_total").val('');
    $("#id_subtotal").val('');
    $("#TxtEnvio").val('');
}


//CONFIRMACION FACTURACION
$('#Facturar').click(function (e) {
    Swal.fire({
        title: '¿Estas seguro de crear la factura?',
        text: "No pódras deshacer esta decision",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#d33',
        confirmButtonText: '<i class="fas fa-file-invoice-dollar"></i> Facturar',
        backdrop: `
          rgba(0,0,123,0.4)
          url("/static/img/Pollito.gif")
          left top
          no-repeat
        `
    }).then((result) => {
        if (result.isConfirmed) {
            Facturacion()
        }
    })

});

//ENVIAR ARRAY DE PRODUCTOS 
let Facturacion = () => {
    let url = $("#Facturar").data("url")
    let csrftoken = $("input[name=csrfmiddlewaretoken").val()
    var data = { 'factura': JSON.stringify(Object.assign({}, Array_carrito)), 'csrfmiddlewaretoken': csrftoken }
    // console.log(data.factura)
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: data,
        beforeSend: function () {
            Swal.fire({
                imageUrl: '/static/img/Loading.gif',
                imageWidth: 250,
                imageHeight: 200,
                imageAlt: 'Custom image',
                showConfirmButton: false,
                title: 'Cargando ...',
            });
        },
        complete: function (data) {
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                }).then(() => {
                    VaciarCamposProducto()
                    VaciarCamposCliente()
                    VaciarCamposFactura()
                    Array_carrito = []
                    $("#tabla-carrito > tbody").empty()
                    location.reload()
                });
            }
        }
    });
    return false;

}

//CANCELAR FACTURACION
$('#Cancelar').click(function (e) {
    Swal.fire({
        title: '¿Estas seguro de cancelar la factura?',
        text: "No pódras deshacer esta decision",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#198754',
        confirmButtonText: '<i class="fas fa-stop-circle"></i> Eliminar',
        backdrop: `
        rgba(0,0,123,0.4)
        url("/static/img/Pollito_cancelar.gif")
        left top
        no-repeat
      `
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Cancelado',
                'Factura cancelada.',
                'success',
                VaciarCamposProducto(),
                VaciarCamposCliente(),
                VaciarCamposFactura(),
                Array_carrito = [],
                $("#tabla-carrito > tbody").empty(),
                $("#Facturar").removeClass('btn btn-warning d-block').addClass('btn btn-warning d-none'),
                $("#Cancelar").removeClass('btn btn-danger d-blocl').addClass('btn btn-danger d-none'),
            )
        }
    })

});

//MOSTRAR GRAFICA VENTA ANUAL
let GraficaVentaAnual = (datos) => {
    var enero = datos.venta[0][0]
    var febrero = datos.venta[0][1]
    var marzo = datos.venta[0][2]
    var abril = datos.venta[0][3]
    var mayo = datos.venta[0][4]
    var junio = datos.venta[0][5]
    var julio = datos.venta[0][6]
    var agosto = datos.venta[0][7]
    var septiembre = datos.venta[0][8]
    var octubre = datos.venta[0][9]
    var noviembre = datos.venta[0][10]
    var diciembre = datos.venta[0][11]
    var ctx = document.getElementById('chart_venta_anual').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: [enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre],
                backgroundColor: ['#42a5f5', 'red', 'green', 'blue', 'violet'],
                label: 'Ventas anuales'
            }],
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        },
        options: { responsive: true }
    });
}
//VER DONUTS DE PRODUCTO MAS VENDIDOS
let GraficaProductoVendido = (datos) => {
    var ctx = document.getElementById('chart_venta_producto').getContext('2d');
    let venta = datos.venta;
    let array_nombre = []
    let array_cantidad = []
    let background_color = ['#42a5f5', 'red', 'green', 'blue', 'violet']
    let label = "producto mas vendidos"
    let labels = []
    let dataset_cantidad = []

    for (var i = 0; i < venta.length; i++) {
        array_cantidad[i] = venta[i][2]
        array_nombre[i] = venta[i][1]
    }

    dataset_cantidad.push({
        'data': array_cantidad,
        'backgroundColor': background_color,
        'label': 'Producto mas vendidos'
    })

    labels.push({
        'labels': array_nombre
    })
    labels = labels[0]['labels']
    var chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets:
                dataset_cantidad,
            labels
        },
        options: { responsive: true ,  maintainAspectRatio: false, }
    });

}
//VER DETALLE FACTURA EN UN MODAL
$(".ver_detalle_factura").on("click", function () {
    let url = $(this).data("url");
    $(".modal-body").load(url, function () {
        $("#modal_facturacion").modal({ show: true });
    });
});

// VER NOTIFICACION EN UN MODAL
$(".ver_notificacion").on("click", function () {
    let url = $(this).data("url");
    $(".modal-body").load(url, function () {
        $("#modal_facturacion").modal({ show: true });
    });
});



$('#menu-notificacion').hover(function () {
    $('ul', this).fadeIn();
}, function (){
    $('ul', this).fadeOut(); 
});


$('#menu-producto').hover(function () {
    $('ul', this).fadeIn();
}, function (){
    $('ul', this).fadeOut(); 
});

$("#frmcruzar").bind("submit", function () {
    var btnenviar = $("#btn-cruzar");
    let url = $(this).data("url");
    let csrftoken = $("input[name=csrfmiddlewaretoken").val()
    var data = { 'csrfmiddlewaretoken': csrftoken }
    $.ajax({
        type:'POST',
        url: url,
        dataType: "json",
        data: data,
        beforeSend: function () {
            btnenviar.text("Procesando archivos ");
            btnenviar.attr("disabled", "disabled");
            btnenviar.append('<span class="spinner-border spinner-border-md" role="status" aria-hidden="true"></span>');
        },
        done: function (data) {
            btnenviar.text("Archivos cargados");
        },
        complete: function (data) {
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                })
                btnenviar.text("Inventario cruzado");
            }else{
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                })
                btnenviar.text("Inventario no cruzado");
            }
            btnenviar.removeAttr("disabled");
            
        },
        fail: function (jqXHR, textStatus, errorThrown) {
            alert("\nError: " + jqXHR.status + ' \nMensaje ' + textStatus + ' \nestado ' + errorThrown);
        },
    });
    return false;
});


//BUSCAR PRODUCTO EN INVENTARIAR 
$("#TxtBuscarProducto").keydown(function (e) {
    if (e.which == 13 || e.which == 9) {
        e.preventDefault();
        let producto = $('#TxtBuscarProducto').val();
        var btnenviar = $("#AgregarInventario");
        let url = $('#TxtBuscarProducto').data("url");
        let csrftoken = $("input[name=csrfmiddlewaretoken").val()
        var data = { 'csrfmiddlewaretoken': csrftoken ,'TxtBuscarProducto': producto}
        if (producto == ""){
            Swal.fire({
                title: 'Error de validacion',
                text: 'El campo referencia de producto no puede ir vacio',
                icon: 'error',
                timer: 6000,
            })
        }else{
            $.ajax({
                type:'POST',
                url: url,
                dataType: "json",
                data: data,
                beforeSend: function () {
                    btnenviar.text("Agregando");
                    btnenviar.attr("disabled", "disabled");
                    btnenviar.append('<span class="spinner-border spinner-border-md" role="status" aria-hidden="true"></span>');
                },
                complete: function (data) {
                    if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                        ArrayInventario(data.responseJSON.datos)
                    }else{
                        Swal.fire({
                            title: data.responseJSON.status + ' ' + data.responseJSON.code,
                            text: data.responseJSON.msj,
                            icon: 'warning',
                            timer: 4000,
                        })  
                        $('.spn-referencia').html('<i class="fas fa-window-close"></i>').removeClass().addClass('spn-referencia input-group-text text-light bg-danger');                 
                    }
                    btnenviar.text("Agregar");
                    btnenviar.append('<i class="fas fa-arrow-circle-right"></i>');
                    
                },
                fail: function (jqXHR, textStatus, errorThrown) {
                    alert("\nError: " + jqXHR.status + ' \nMensaje ' + textStatus + ' \nestado ' + errorThrown);
                },
            });
            return false;

        }
    }
});

//AGREGAR ARRAY DE INVENTARIOS
let Array_inventario = [];
let cantidad;
let id;
let id_producto;
let descripcion;
let iteracion;
let ArrayInventario = (Array) => {
    if (Array != ""){
        cantidad = Array.cantidad;
        id  = Array.id;
        id_producto  = Array.id_producto;
        descripcion  = Array.descripcion;
        iteracion = 1;
    }
    if (Array_inventario.length==0){
        Array_inventario.push({
            'id': id,
            'id_producto': id_producto,
            'cantidad': cantidad,
            'descripcion': descripcion,
            'iteracion': iteracion       
         })
    } else {
        for (var i = 0; i < Array_inventario.length; i++) {
            if (Array_inventario[i].id_producto == id_producto){ 
                cantidad = (Array_inventario[i].cantidad + cantidad);
                iteracion = iteracion+1;
            }  
        }
        Array_inventario.push({
            'id': id,
            'id_producto': id_producto,
            'cantidad': cantidad,
            'descripcion': descripcion, 
            'iteracion': iteracion
        })  

    }
    if (Array_inventario.length > 0) {
        ValidarAgregarLista(Array_inventario);       
    }
}

//VALIDAR PROCESOS
let ValidarAgregarLista = (Array) => {
    $('.spn-referencia').html('<i class="fas fa-check-circle"></i>').removeClass().addClass('spn-referencia input-group-text text-light bg-success'); 
    $( '.CheckConfirmarProducto' ).on( 'click', function() {
        if( $(this).is(':checked') ){
            AgregarLista(Array)
            $("#AgregarInventario").removeAttr("disabled");
        } else {
            $("#AgregarInventario").attr("disabled", "disabled");
        }
    }); 
}

let AgregarLista = (Array) => {
    $( '.AgregarInventario' ).on( 'click', function() {
        if( $('.CheckConfirmarProducto').is(':checked') ){   
            for (var i = 0; i < Array.length; i++) { 
                $('#item-vacio').remove();
                let existe = $(`.lista-producto-inventario`).find(`#${Array[i].id_producto}`).length;
                if(existe==0){   ;         
                    $('.lista-producto-inventario').append(
                        `<li class="list-group-item" id="${Array[i].id_producto}" name="${Array[i].id_producto}"> 
                        <input class="form-check-input me-1 eliminar-producto-inventario" name="eliminar-producto-inventario" id="eliminar-producto-inventario" type="checkbox" value="${Array[i].id_producto}" aria-label="..."> 
                        ${Array[i].descripcion}
                        <span class="badge bg-primary rounded-pill">${Array[i].iteracion}</span>
                    </li>`
                    )
                    $("#TxtBuscarProducto").val('');
                    $("#CheckConfirmarProducto").prop('checked', false);
                    $('.spn-referencia').html('<i class="fas fa-question-circle"></i>').removeClass().addClass('spn-referencia input-group-text text-light bg-warning'); 
                    $('.card-resultado').removeClass().addClass('card shadow rounded card-resultado d-block');
                } 
                if (existe > 0) { 
                    $('.lista-producto-inventario').find(`#${Array[i].id_producto}`).replaceWith(
                        `<li class="list-group-item" id="${Array[i].id_producto}" name="${Array[i].id_producto}"> 
                        <input class="form-check-input me-1 eliminar-producto-inventario" name="eliminar-producto-inventario" id="eliminar-producto-inventario" type="checkbox" value="${Array[i].id_producto}" aria-label="..."> 
                        ${Array[i].descripcion}
                        <span class="badge bg-primary rounded-pill">${Array[i].iteracion}</span>
                    </li>`
                    )
                    $("#TxtBuscarProducto").val('');
                    $("#CheckConfirmarProducto").prop('checked', false);
                    $('.spn-referencia').html('<i class="fas fa-question-circle"></i>').removeClass().addClass('spn-referencia input-group-text text-light bg-warning'); 
                    $('.card-resultado').removeClass().addClass('card shadow rounded card-resultado d-block');   
                }
            }

        }
    });
}


//ELIMINA LOS PRODUCTOS DEL CARRITO
$(document).on('change', '.eliminar-producto-inventario', function (e) {
    if( $('.eliminar-producto-inventario').is(':checked') ){   
            Swal.fire({
                title: '¿Desea eliminar este producto de inventario?',
                text: 'Proceso irreversible',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Eliminarlo'
        }).then((result) => {
            if (result.isConfirmed) {
                let id = $(this).val();
                $('.lista-producto-inventario').children(`#${id}`).remove();
                const result = Array_inventario.findIndex(id_producto => id_producto.id_producto == id)
                Array_inventario.splice(result,1);          
        }})
    }
});

//CONFIRMACION INVENTARIAR
$('#VerificarInventario').click(function (e) {
    if (Array_inventario.length > 0){
        Swal.fire({
            title: '¿Estas seguro de realizar cruce de inventario?',
            text: "No pódras deshacer esta decision",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#198754',
            cancelButtonColor: '#d33',
            confirmButtonText: '<i class="fas fa-file-invoice-dollar"></i> Inventariar',
            backdrop: `
            rgba(0,0,123,0.4)
            url("/static/img/Pollito.gif")
            left top
            no-repeat
            `
        }).then((result) => {
            if (result.isConfirmed) {
                Inventariar()
            }
        })
    } else {
        Swal.fire({
            title: 'Error de validacion',
            text: 'No se ha agregado ni un producto a inventariar',
            icon: 'warning',
    })}
});

//ENVIAR ARRAY DE PRODUCTOS PARA INVENTARIAR
let Inventariar = () => {
    let url = $("#VerificarInventario").data("url")
    let csrftoken = $("input[name=csrfmiddlewaretoken").val()
    var data = { 'inventario': JSON.stringify(Object.assign({}, Array_inventario)), 'csrfmiddlewaretoken': csrftoken }
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: data,
        beforeSend: function () {
            Swal.fire({
                imageUrl: '/static/img/Loading.gif',
                imageWidth: 250,
                imageHeight: 200,
                imageAlt: 'Custom image',
                showConfirmButton: false,
                title: 'Cargando ...',
            });
        },
        complete: function (data) {
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                })
                ResultadoInventario(data.responseJSON.resultado);
                Array_inventario = []
                $("#lista-producto-inventario").empty()
                $("#VerificarInventario").attr("disabled", "disabled");
                $("#lista-producto-inventario")
                .append('<li class="item-vacio list-group-item" name="item-vacio" id="item-vacio"><input class="form-check-input me-1 eliminar-producto-inventario" name="eliminar-producto-inventario" id="eliminar-producto-inventario" type="checkbox" value="" aria-label="..."> Sin producto <span class="badge bg-primary rounded-pill">0</span></li>');
            }
        }
    });
    return false;

}

let ResultadoInventario = (Array) => {

    for (var i = 0; i < Array.length; i++) { 
        if(Array[i].status == "dispaer"){
            $(".resultado-inventario").append(` <li class="list-group-item">${Array[i].msj} <i class="fas fa-exclamation-circle"></i></li> `)
        } 
        if(Array[i].status == "ok"){
            $(".resultado-inventario").append(` <li class="list-group-item">${Array[i].msj} <i class="far fa-check-square"></i></li> `)
            
        }
    }

}
//CONFIRMACION COTIZACION
$('#Cotizar').click(function (e) {
    Swal.fire({
        title: '¿Estas seguro de crear la cotizacion?',
        text: "No pódras deshacer esta decision",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#d33',
        confirmButtonText: '<i class="fas fa-file-invoice-dollar"></i> Cotizar',
        backdrop: `
          rgba(0,0,123,0.4)
          url("/static/img/Pollito.gif")
          left top
          no-repeat
        `
    }).then((result) => {
        if (result.isConfirmed) {
            Cotizacion()
        }
    })

});

//ENVIAR ARRAY DE PRODUCTOS A COTIZAR
let Cotizacion = () => {
    let url = $("#Cotizar").data("url")
    let csrftoken = $("input[name=csrfmiddlewaretoken").val()
    var data = { 'cotizacion': JSON.stringify(Object.assign({}, Array_carrito)), 'csrfmiddlewaretoken': csrftoken }
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: data,
        beforeSend: function () {
            Swal.fire({
                imageUrl: '/static/img/Loading.gif',
                imageWidth: 250,
                imageHeight: 200,
                imageAlt: 'Custom image',
                showConfirmButton: false,
                title: 'Cargando ...',
            });
        },
        complete: function (data) {
            console.log(data.responseJSON)
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                }).then(() => {
                    VaciarCamposProducto()
                    VaciarCamposCliente()
                    VaciarCamposFactura()
                    Array_carrito = []
                    $("#tabla-carrito > tbody").empty()
                    location.reload()
                });
            }else{
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                });
            }
        }
    });
    return false;

}

//VER COTIZACION DE  FACTURA EN UN MODAL
$(".ver_cotizacion").on("click", function () {
    let url = $(this).data("url");
    $(".modal-body").load(url, function () {
        $("#modal_cotizacion").modal({ show: true });
    });
});


//FACTURAR COTIZACION
$(document).on('click', '.Facturar_cotizacion',function (e) {
    Swal.fire({
        title: '¿Estas seguro de crear la factura?',
        text: "No pódras deshacer esta decision",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#d33',
        confirmButtonText: '<i class="fas fa-file-invoice-dollar"></i> Facturar',
        backdrop: `
          rgba(0,0,123,0.4)
          url("/static/img/Pollito.gif")
          left top
          no-repeat
        `
    }).then((result) => {
        if (result.isConfirmed) {
            FacturarCotizacion()
        }
    })

});


//ENVIAR ARRAY DE PRODUCTOS A COTIZAR
let FacturarCotizacion = () => {
    let url = $("#Facturar_cotizacion").data("url")
    let id = $("#Facturar_cotizacion").data("id")
    let csrftoken = $("input[name=csrfmiddlewaretoken").val()
    var data = { 'id': id, 'csrfmiddlewaretoken': csrftoken }
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: data,
        beforeSend: function () {
            Swal.fire({
                imageUrl: '/static/img/Loading.gif',
                imageWidth: 250,
                imageHeight: 200,
                imageAlt: 'Custom image',
                showConfirmButton: false,
                title: 'Cargando ...',
            });
        },
        complete: function (data) {
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                }).then(() => {
                    VaciarCamposProducto()
                    VaciarCamposCliente()
                    VaciarCamposFactura()
                    Array_carrito = []
                    $("#tabla-carrito > tbody").empty()
                    location.reload()
                });
            }else{
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                });
            }
        }
    });
    return false;

}


//VER DETALLE FACTURA EN UN MODAL
$(".btn_agregar_imagen").on("click", function () {
    let url = $(this).data("url");
    $(".modal-body").load(url, function () {
        $("#modal_imagen_producto").modal({ show: true });
    });
});


$(document).on('submit', '#frmimagenproducto', function (e){
    $.ajax({
        type: $(this).attr("method"),
        url: url,
        dataType: "JSON",
        data:  new FormData(this),
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function () {
            Swal.fire({
                imageUrl: '/static/img/Loading.gif',
                imageWidth: 250,
                imageHeight: 200,
                imageAlt: 'Custom image',
                showConfirmButton: false,
                title: 'Cargando ...',
            });
        },
        complete: function (data) {
            if (data.responseJSON.status == "success" && data.responseJSON.code == 200) {
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                })
            }else{
                Swal.fire({
                    title: data.responseJSON.status + ' ' + data.responseJSON.code,
                    text: data.responseJSON.msj,
                    icon: data.responseJSON.status,
                    timer: 4000,
                });
            }
        }
    })
    return false;
});
