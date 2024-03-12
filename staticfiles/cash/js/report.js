var input_date_range;
var current_date;
var tblReport;
var columns = [];
var report = {
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
            columns.push(value.sWidthOrig);
        });
    },
    list: function (all) {
        var parameters = {
            'action': 'search_report',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }

        tblReport = $('#tblReport').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                dataSrc: ""
            },
            order: false,
            paging: false,
            ordering: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: '<i class="fas fa-file-excel"></i> Descargar excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-sm mb-3'
                },
            ],
            columns: [
                {data: "fecha_banqueado"},
                {data: "total_ventas_tarjeta"},
                {data: "total_ventas_efectivo"},
                {data: "total_gastos"},
                {data: "cierre_caja"},
                {data: "diferencia_caja"},
                {data: "monto_caja"},
                {data: "monto_banqueado"},
                {data: "usuario"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5, -6, -7, -8],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '€' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                
            }
        });
    }
};


$(function () {
    current_date = new moment().format('YYYY-MM-DD');
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            report.list(false);
        });

    $('.drp-buttons').hide();

    report.initTable();

    report.list(false);

    $('.btnSearchAll').on('click', function () {
        report.list(true);
    });
});



