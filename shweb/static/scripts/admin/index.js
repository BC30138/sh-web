$(".change-order").on('click', function () {
    $(".save-order").css("display", "block")
    $(".cancel-order").css("display", "block")
    $(".change-order").css("display", "none")
    $(".order-buttons").css("display", "flex")
});

$(".change-order-up").on('click', function () {
    alert(JSON.stringify($(this).parent().parent().css("order")))
});