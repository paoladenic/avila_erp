$(function () {
    function getCSRFToken() {
        let csrfToken = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                const [key, value] = cookie.trim().split('=');
                if (key === 'csrftoken') csrfToken = decodeURIComponent(value);
            });
        }
        return csrfToken;
    }

    function updateStatus(trabajoId, nuevoStatus) {
        $.ajax({
            url: `/erp/taller/update_status/${trabajoId}/`,  // ✅ Aseguramos que tenga "erp/"
            type: "POST",
            data: { status: nuevoStatus },
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function (response) {
                console.log("✅Estado actualizado correctamente");
            },
            error: function (xhr) {
                console.error("❌Error al actualizar estado:", xhr.responseText);
            }
        });
    }

    function formatStatusBadge(state) {
        if (!state.id) return state.text;
        let badgeMap = {
            "Sin Comenzar": "badge bg-danger",             // 🔴 Rojo
            "En el Taller": "badge bg-warning text-dark",  // 🟠 Naranja
            "Entregado": "badge bg-success",               // 🟢 Verde
            "Listo y Sin Retirar": "badge bg-primary",     // 🔵 Azul
            "Cotización": "badge bg-secondary"             // ⚪ Gris (secondary)
        };
        let badgeClass = badgeMap[state.text] || "badge bg-secondary";
        return `<span class="${badgeClass}" style="padding: 5px 10px; border-radius: 10px; display: inline-block; width: 100%; text-align: center;">${state.text}</span>`;
    }

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
            {"data": "id"},
            {"data": "status"},
            {"data": "fecha_trabajo"},
            {"data": "cliente.full_name"},
            {"data": "detalle"},
            {"data": "numero"},
            {"data": "id"},
            {"data": "id"},
        ],
        order: [[0, 'desc']],
        columnDefs: [
            {
                targets: [1],  // Columna de Status
                class: 'text-center',
                render: function (data, type, row) {
                    let statusOptions = {
                        "Sin Comenzar": "Sin Comenzar",
                        "En el Taller": "En el Taller",
                        "Entregado": "Entregado",
                        "Listo y Sin Retirar": "Listo y Sin Retirar",
                        "Cotización": "Cotización"
                    };
                    let select = `<select class="status-select form-control" data-id="${row.id}">`;
                    $.each(statusOptions, function (key, value) {
                        let selected = (key === data) ? "selected" : "";
                        select += `<option value="${key}" ${selected}>${value}</option>`;
                    });
                    select += `</select>`;
                    return select;
                }
            },
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                // render: function (data, type, row) {
                //     return isNaN(parseFloat(data)) || data === '' ? 'N/A' : '€' + parseFloat(data).toFixed(2);
                // }
                render: function (data, type, row) {
                    var buttons = `<a href="/erp/taller/update2/${row.id}/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-edit"></i></a> `;
                    return buttons;
                }
            },
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = `<a href="/erp/taller/update2/${row.id}/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> `;
                    buttons += `<a href="/erp/taller/invoice2/pdf/${row.id}/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> `;
                    buttons += `<a href="/erp/taller/delete2/${row.id}/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>`;
                    return buttons;
                }
            }
        ],
        drawCallback: function () {
            $(".status-select").select2({
                width: '100%',
                dropdownAutoWidth: true,
                templateResult: formatStatusBadge,
                templateSelection: formatStatusBadge,
                escapeMarkup: function (markup) { return markup; }
            }).on('select2:open', function () {
                $('.select2-results__options').css('font-size', '14px');
            });

            // 🔥 Ajuste de altura y alineación del select2
            $('.select2-container--default .select2-selection--single').css({
                'height': '38px',
                'display': 'flex',
                'align-items': 'center',
                'border-radius': '10px'
            });
        }
    });


    $(document).on("change", ".status-select", function () {
        let trabajoId = $(this).data("id");
        let nuevoStatus = $(this).val();
        updateStatus(trabajoId, nuevoStatus);
    });  
});
