var TeamEditSoccer;

document.addEventListener('DOMContentLoaded', function (event) {
    const form = document.getElementById('frmEditTeamEditSoccer');
    TeamEditSoccer = FormValidation.formValidation(form, {
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
                nameSoccer_edit: {
                    validators: {
                        notEmpty: {
                            message: 'Ingrese un Nombre'
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
            const iconPlugin = TeamEditSoccer.getPlugin('icon');
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
            var parameters = new FormData(TeamEditSoccer.form);
            parameters.append('action', 'editSoccerTeam');
            let urlrefresh = TeamEditSoccer.form.getAttribute('data-url');
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function (request) {
                   //location.href = urlrefresh;
                   var idTeam = $("#id_SoccerTeam").val();
                   //console.log(idTeam);
                   $("#exampleModalPreview-editTeam"+idTeam).modal('hide');
                   limpiarSoccer();
                   getDataTeamEditSoccer();
                },
            );
        });
});

$(function () {
    console.log("Ingresando a formulario TeamEditSoccer");
});
