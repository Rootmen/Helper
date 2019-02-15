(function() {
    var msgRow = $("#message-row");
    var msgInput = $("#enter-message");

    $(".radio").click(
        function() {
            if($(this).attr("data-need-message") == '0') {
                msgInput.removeAttr("required");
                msgRow.hide();
            } else {
                msgInput.attr("required", "");
                msgRow.show();
            }
        }
    );
})();
