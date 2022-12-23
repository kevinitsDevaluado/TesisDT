function getDataStadium() {
    $.ajax({
        url: pathname,
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'action': 'listStadium'
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data) {
                for (var i = 0; i < data.length; i++)
                {
                    var coloursAlert1 = ["success","warning","info"];
                    var aleatorio = coloursAlert1[Math.floor(Math.random() * coloursAlert1.length)]
                    $('#listHtmlTextStadium').append(
                        '<div class="col-md-6" >'+
                                '<a'+
                                    'id="modalActivate" type="button"'+
                                    'data-toggle="modal" data-target="#exampleModalPreview-editStadium'+ data[i].id +'"'+
                                    'data-toggle="tooltip"'+
                                    'title="Editar Team"'+
                                    'class="btn btn-success">'+  
                                        '<div class="small-box bg-success">'+
                                            '<div class="inner">'+
                                                '<p class="text-center"><strong>'+ data[i].name +'</strong></p>'+
                                            '</div>'+
                                            '<div class="icon text-center">'+
                                                '<img class="img-fluid" width="80%" src="../../../..'+data[i].image+'" alt="">'+
                                            '</div>'+
                                            '<br>'+
                                        '</div>'+
                                '</a>'+
                        '</div>'
                    );

                    $('#modaEditStadium').append(
                        '<div class="modal fade right" id="exampleModalPreview-editStadium'+ data[i].id +'" tabindex="-1" role="dialog" aria-labelledby="exampleModalPreviewLabel" aria-hidden="true">'+
                            '<div class="modal-dialog modal-dialog momodel modal-fluid" role="document">'+
                                '<div class="modal-content modal-content ">'+
                                    '<div class=" modal-header   modal-header text-center">'+
                                        '<h5 class="modal-title w-100" id="exampleModalPreviewLabel"> Editar Información </h5>'+
                                        '<button type="button" class="close " data-dismiss="modal" aria-label="Close">'+
                                            '<span style="font-size: 1.3em;" aria-hidden="true">&times;</span>'+
                                        '</button>'+
                                    '</div>'+
                                    '<form class="form" method="post" enctype="multipart/form-data" data-url="/erp/profile/'+ data[i].sportLeague.id +'" action="/erp/Stadium/update/'+ data[i].id +'/">'+
                                        '<div class="modal-body">'+
                                            '<div class="row">'+
                                                '<div class="col-md-12">'+
                                                    '<div class="form-group">'+
                                                        '<input type="text" hidden id="id_SoccerTeamStadium" name="id_SoccerTeamStadium" value="'+ data[i].id +'">'+
                                                        '<input type="text" hidden id="image_editStadium" name="image_editStadium" value="'+ data[i].image +'">'+
                                                        '<label>Ingresa el nombre: </label>'+
                                                        '<input type="text" name="nameSoccer_editStadium" id="nameSoccer_editStadium" class="form-control" value="'+ data[i].name +'">'+
                                                        '<label>Ingresa la descripción: </label>'+
                                                        '<input type="text" name="descSoccer_editStadium" id="descSoccer_editStadium" class="form-control" value="'+ data[i].desc +'">'+
                                                        '<label>Ingresa la imagen: </label>'+
                                                        '<input type="file" name="imageSoccer_editStadium" id="imageSoccer_editStadium" class="form-control" id="refuerzo" name="refuerzo">'+
                                                        '<a href=" ../../../../media/'+ data[i].image +'">  <b>Actualmente</b>'+ data[i].image +'</a>'+
                                                    '</div>'+
                                                '</div>'+
                                            '</div>'+
                                        '</div>'+
                                        '<div class="modal-header">'+
                                            '<button type="button" class="btn btn-info" data-dismiss="modal">Cancelar</button>'+
                                            '<a href="/erp/Stadium/delete/'+ data[i].id +'" class="btn btn-danger">Eliminar</a>'+
                                            '<button type="submit" class="btn btn-success">Aceptar</button>'+
                                        '</div>'+
                                    '</form>'+
                                '</div>'+
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
    getDataStadium();
});


function limpiarStadium() {
    document.getElementById("listHtmlTextStadium").innerHTML = ""; 
}

function urlRedirect(id) {
    success_url = "{% url 'profile' "+ id +" %}";
    return success_url;
}

function urlRedirectImg(img) {
    success_url = "{{"+ img +" .url }}";
    return success_url;
}


