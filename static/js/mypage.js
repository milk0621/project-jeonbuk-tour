//비밀번호 변경
$(document).ready(function() {
    $(".change-btn").click(function() {
        $("#change_pw").fadeIn();
    });

    $(".close").click(function() {
        $("#change_pw").fadeOut();
    });

    $(window).click(function(event) {
        if ($(event.target).is("#change_pw")) {
            $("#change_pw").fadeOut();
        }
    });

    $(".delete-btn").click(function() {
        $("#delete_user").fadeIn();
    });

    $(".d_close").click(function() {
        $("#delete_user").fadeOut();
    });

    $(window).click(function(event) {
        if ($(event.target).is("#delete_user")) {
            $("#delete_user").fadeOut();
        }
    });
});