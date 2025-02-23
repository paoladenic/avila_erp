var input_date_range;
var current_date;
var tblReport;
var columns = [];
var totalSum = 0;  // Variable para almacenar la sumatoria
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
                {
                    extend: 'pdfHtml5',
                    text: '<i class="fas fa-file-pdf"></i> Descargar PDF',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-sm mb-3',
                    download: 'open',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 13,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 8
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 11,
                                color: 'white',
                                fillColor: '#2d4154',
                                alignment: 'center'
                            }
                        };
                        doc.content[1].table.widths = columns;
                        doc.content[1].margin = [0, 35, 0, 0];
                        doc.content[1].layout = {};
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: current_date}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });

                    }
                }
            ],
            columns: [
                {data: "id"},
                {data: "date_cash"},
                {data: "tipo_pago"},
                {data: "subtotal"},
                {data: "iva"},
                {data: "total"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var numericValue = parseFloat(data);
                        console.log('Contenido de data:', numericValue, ', Tipo de datos:', typeof numericValue); 
                        if (!isNaN(numericValue)) {
                            return '€' + numericValue.toFixed(2);
                        } else {
                            return ''; // o cualquier valor predeterminado si no es numérico
                        }
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/erp/ticket/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                totalSum = 0;
                
                tblReport.rows().every(function () {
                    var data = this.data();
                    var numericValue = parseFloat(data.total);
                    if (!isNaN(numericValue)) {
                        totalSum += numericValue;
                    }
                });

                // Añadir la fila de total al final de la tabla
                if (tblReport.rows().count() > 0) {
                    var row = tblReport.row.add({
                        id: 'Total',
                        date_cash: '',
                        tipo_pago: '',
                        subtotal: '',
                        iva: '',
                        total: totalSum,
                    }).draw().node();

                    // Aplicar formato a la fila total si es necesario
                    $(row).addClass('text-bold');
                }  
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


