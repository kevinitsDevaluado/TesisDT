var tblListAsistencia;
var columns = [];

function getDataListAsistencia() {
    tblListAsistencia = $('#dataAsistenciaList').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action': 'searchListAsistencia',
                'estado_list': $('select[name="estado_list"]').val(),
                'id_traininglist' : $('select[name="id_traininglist"]').val(),
            },
            dataSrc: ""
        },
        order: [[0, 'asc']],
        paging: false,
        ordering: true,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            }
        ],
        columns: [
            {data: "pos"},
            {data: "referee.user.full_name"},
            {data: "asistencia"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data) {
                        return '<span class="badge badge-success">Asistió</span>';
                    }
                    return '<span class="badge badge-danger">No Asistió</span>';
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });

}

$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="estado_list"]').on('change', function () {
        getDataListAsistencia();
    });
    $('select[name="id_traininglist"]').on('change', function () {
        getDataListAsistencia();
    });
    
   
});