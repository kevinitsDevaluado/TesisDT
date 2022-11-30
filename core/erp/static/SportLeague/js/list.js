function getData() {
    $.ajax({
        url: pathname,
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'action': 'listSportLeague'
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data) {
                for (var i = 0; i < data.length; i++)
                {
                    $('#listHtmlText').append(
                        '<div class="col-md-3">'+
                            '<a href="/erp/profile/'+ data[i].id +'" class="dropdown-item" >'+
                                '<div class="info-box">'+
                                    '<span class="info-box-icon bg-warning"><i class="fas fa-futbol"></i></span>'+
                                    '<div class="info-box-content">'+
                                        '<span class="info-box-text">' + data[i].name + '</span>'+
                                    '</div>'+
                                '</div>'+
                            '</a>'+
                        '</div>'
                    );
                    console.log(urlRedirect(data[i].id));
                }
            }
        }
    });
}

$(function () {
    getData();
});


function limpiar() {
    document.getElementById("listHtmlText").innerHTML = ""; 
}

function urlRedirect(id) {
    success_url = "{% url 'profile' "+ id +" %}";
    return success_url;
}



