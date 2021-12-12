
function openLyrics(id) {
    if (id !== "") {
        document.getElementById(id).classList.toggle("show");
        document.getElementById(id + "-expand-icon").classList.toggle("expand-more")
    }
}

function copyToClipboard(text) {
    /* Copy the text inside the text field */
    navigator.clipboard.writeText(text);

    var el = document.querySelector('.copied-alarm')

    el.style.transition = "opacity 0.2s linear"
    el.style.visibility = "visible"
    el.style.opacity = 1;
    setTimeout(function () {
        el.style.visibility = "hidden"
        el.style.opacity = 0
        el.style.transition = "visibility 0s 0.2s, opacity 0.2s linear"
    }, 1000);
}