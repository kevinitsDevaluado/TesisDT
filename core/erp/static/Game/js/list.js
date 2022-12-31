function getDataGameGame() {
    $('#dataGameGame').DataTable({
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
                'action': 'listGame'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "teamLocal.name"},
            {"data": "teamVisitor.name"},
            {"data": "referee.user.full_name"},
            {"data": "stadium.name"},
            {"data": "dateGame"},
            {"data": "hourGame"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/detailsgame/add/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/Game/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getDataGameGame();

    
});

function limpiarStadium() {
    document.getElementById("dataGameGame").innerHTML = ""; 
}
