$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "numero"},
            {"data": "fecha_trabajo"},
            {"data": "nombre"},
            {"data": "apellido"},
            {"data": "telefono"},
            {"data": "vehiculo"},
            {"data": "detalle"},
            {"data": "image"},
            {"data": "presupuesto"},
            {"data": "status"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var imageUrl = '<img src="' + data + '" class="img-thumbnail" style="cursor: pointer; width: 50px; height: 50px;" onclick="showImage(\'' + data + '\')">';
                    return imageUrl;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (isNaN(parseFloat(data)) || data === '') {
                        return 'N/A';
                    } else {
                        return '€' + parseFloat(data).toFixed(2);
                    }
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var badgeColor;
                    if (row.status === "En el Taller") {
                        badgeColor = 'badge-secondary';
                    } else if (row.status === "Entregado") {
                        badgeColor = 'badge-success';
                    } else if (row.status === "Listo y Sin Retirar") {
                        badgeColor = 'badge-warning';
                    } else if (row.status === "Cotización") {
                        badgeColor = 'badge-info';
                    } else {
                        badgeColor = 'badge-light';
                    }
                    return '<span class="badge ' + badgeColor + '">' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/taller/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/taller/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="/erp/taller/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        order: [[10, 'desc']],
        initComplete: function (settings, json) {

        }
    });
});

