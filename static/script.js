$(document).ready(function() {
    $("#getAdviceBtn").click(function() {
        $("#advice").text("⏳ Generating advice...");
        $.get("/get_advice", function(response) {
            $("#advice").text(response.advice);
        });
    });
});
