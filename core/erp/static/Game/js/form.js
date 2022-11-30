var Game;
var select_local;
var select_visit;
var select_stadio;

document.addEventListener('DOMContentLoaded', function (event) {
    const form = document.getElementById('frmFormGame');
    Game = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                referee: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Arbitro',
                        },
                    }
                },
                teamVisitor: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Equipo Visitante',
                        },
                    }
                },
                teamLocal: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Equipo Local',
                        },
                    }
                },
                stadium: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Estadio',
                        },
                    }
                },
                hourGame: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Estadio',
                        },
                        regexp: {
                            regexp: /^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?$/,
                            message: 'El formato email no es correcto'
                        },
                    }
                },
                dateGame: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione la fecha del Partido',
                        },
                    }
                },
                price: {
                    validators: {
                        notEmpty: {
                            message: 'Ingrese el precio',
                        },
                    }
                },
            }
            
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = Game.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(Game.form);
            parameters.append('action', 'addGame');
            let urlrefresh = Game.form.getAttribute('data-url');
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function (request) {
                   //location.href = urlrefresh;
                   $("#exampleModalPreview-createGame").modal('hide');
                   limpiarGame();
                   getDataGame();
                },
            );
        });
});

$(function () {
    date_current = new moment().format("YYYY-MM-DD");
    select_local = $('select[name="teamLocal"]'); 
    select_visit = $('select[name="teamVisitor"]');
    select_stadio = $('select[name="stadium"]');
    $('#creada_en').datetimepicker({
        format: 'YYYY-MM-DD',
        minDate: date_current,
    });

    select_local.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_team'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            console.log(e.params.data);
            fv.revalidateField('teamLocal');
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('teamLocal');
        });

    select_visit.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_team'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            console.log(e.params.data);
            fv.revalidateField('teamVisitor');
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('teamVisitor');
        });


    select_stadio.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_stadium'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            console.log(e.params.data);
            fv.revalidateField('stadium');
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('stadium');
        });
});
