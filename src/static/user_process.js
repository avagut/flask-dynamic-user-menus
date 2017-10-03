
/*Client Side User Processing*/

$(document).ready(function(){
    LoadUserName();
    $("#user_name").change(function (){
        LoadUserName();
    });
    $("#my_roles").delegate("td.selected_role", "click", function(){
        var selected = $(this).closest('tr').children('td.role_name').text();
        var user = $("#role_user_name").val()
        ConfirmUnassignDialog('Unassign Role','Please confirm unassigning of role for the user',selected, user);
        event.preventDefault();

    });
    function UnassignRole(selected, user){
        if (selected !== undefined && user!== undefined) {
            var url_string = $(location).attr('href')
            $.ajax ({
                    url: url_string,
                    data: {'my_action':'unassign_role', 'role_name': selected, 'user_name':user},
                    type: 'POST',
                    success: function(response) {
                        console.log(response);
                        var ret = response;
                        if (ret.errorstate == '0') {
                            window.location.replace(url_string);
                            }
                    },
                    error: function(error){
                        console.log(error);
                    }
            });
        }
    }
    function LoadUserName(){
        var user_name = $("#user_name").val();
        console.log(user_name)
        $("#role_user_name").val(user_name);
    }

    function ConfirmUnassignDialog(mytitle, message,selected, user) {
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'?</h6></div>')
            .dialog({
                modal: true,
                title: mytitle,
                zIndex: 10000,
                autoOpen: true,
                resizable: true,
                buttons: {
                    Ok: function () {
                        UnassignRole(selected, user);
                        $(this).dialog("close");
                    },
                    Cancel: function () {
                        $(this).dialog("close");
                    }
                },
                close: function (event, ui) {
                    $(this).remove();
                }
            });
    };

}); //doc ready end