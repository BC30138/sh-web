var share_btn = document.querySelector(".share")

share_btn.addEventListener("click", share)

function openLyrics(id) {
    document.getElementById(id).classList.toggle("show");
    document.getElementById(id + "-expand-icon").classList.toggle("expand-more")
}

function share() {
    navigator.share({
        url: window.location.href,
    })
}