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
            {"data": "status"},
            {"data": "fecha_trabajo"},
            {"data": "cliente.full_name"},
            {"data": "detalle"},
            {"data": "image"},
            {"data": "presupuesto"},
            {"data": "id"}
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    var badgeColor;
                    switch (data) {
                        case "En el Taller":
                            badgeColor = 'badge-secondary';
                            break;
                        case "Entregado":
                            badgeColor = 'badge-success';
                            break;
                        case "Listo y Sin Retirar":
                            badgeColor = 'badge-warning';
                            break;
                        case "Cotización":
                            badgeColor = 'badge-info';
                            break;
                        default:
                            badgeColor = 'badge-light';
                    }
                    return '<span class="badge ' + badgeColor + '">' + data + '</span>';
                }
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-thumbnail" style="cursor: pointer; width: 50px; height: 50px;" onclick="showImage(\'' + data + '\')">';
                }
            },
            {
                targets: [6],
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
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/taller/update2/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/taller/invoice2/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="/erp/taller/delete2/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            }
        ],
    });
});
