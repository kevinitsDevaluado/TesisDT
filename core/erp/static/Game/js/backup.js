function getDataGame() {
    $.ajax({
        url: pathname,
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'action': 'listGame'
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data) {
                console.log("Datos Games");
                console.log(data);
                for (var i = 0; i < data.length; i++)
                {
                    var coloursAlert1 = ["success","warning","info"];
                    var aleatorio = coloursAlert1[Math.floor(Math.random() * coloursAlert1.length)]
                    $('#listHtmlTextGame').append(
                        '<div class="col-md-12" >'+
                            '<div class="small-box bg-'+aleatorio+'">'+
                                '<div class="inner">'+
                                    '<p class="text-center"><strong>'+ data[i].teamLocal.name +'</strong> VS <strong>'+ data[i].teamVisitor.name +'</strong></p>'+
                                '</div>'+
                                '<div class="icon text-center">'+
                                    '<div class="row">'+
                                        '<div class="col-md-6">'+
                                            '<img class="img-fluid" style="width: 150px !important; height: 150px !important" src="../../../..'+data[i].teamLocal.image+'" alt="">'+
                                        '</div>'+
                                        '<div class="col-md-6">'+
                                            '<img class="img-fluid" style="width: 150px !important; height: 150px !important" src="../../../..'+data[i].teamVisitor.image+'" alt="">'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="inner">'+
                                    '<p class="text-center">Arbitro: <strong>'+ data[i].referee.user.full_name +'</strong> Estadio: <strong> '+ data[i].stadium.name +'</strong></p>'+
                                    '<p class="text-center">Fecha: <strong>'+ data[i].dateGame +'</strong> Hora:<strong> '+ data[i].hourGame +'</strong></p>'+
                                '</div>'+
                                '<br>'+
                            '</div>'+
                        '</div>'
                    );
                    aleatorio = "";
                }
            }
        }
    });
}

$(function () {
    getDataGame();
});


function limpiarGame() {
    document.getElementById("listHtmlTextGame").innerHTML = ""; 
}


