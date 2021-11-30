var releases_div = $(".releases")
var releases = {}

jQuery.each(releases_div.children(), function () {
    releases[$(this).css('order')] = $(this).attr('id')
})

$(".change-order").on('click', function () {
    $(".save-order").css("display", "block")
    $(".cancel-order").css("display", "block")
    $(".change-order").css("display", "none")
    $(".order-buttons").css("display", "flex")
});

$(".change-order-up").on('click', function () {
    var release = $(this).parent().parent()
    var order = parseInt(release.css("order"))
    if (order === 1) {
        return false
    }

    left_string = "" + (order - 1)
    right_string = "" + order

    releases[right_string] = releases[left_string]
    releases[left_string] = release.attr('id')

    release.css("order", left_string)
    $("#" + releases[right_string]).css('order', right_string)
});

$(".change-order-down").on('click', function () {
    var release = $(this).parent().parent()
    var order = parseInt(release.css("order"))
    if (order === Object.keys(releases).length) {
        return false
    }

    left_string = "" + (order + 1)
    right_string = "" + order

    releases[right_string] = releases[left_string]
    releases[left_string] = release.attr('id')

    release.css("order", left_string)
    $("#" + releases[right_string]).css('order', right_string)
});

$(".save-order").on('click', function () {
    var base_url = window.location.origin + "/admin/";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE) {
            if (this.status === 200) {
                alert("Changes will be applied in one hour or less");
                window.location.reload();
            } else {
                alert('Error');
            }
        }
        $("body").removeClass("")
        return false;
    }
    xhr.open("POST", base_url);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    $("body").addClass("loading")
    xhr.send(JSON.stringify({ "releases": releases }));

    return false
});