var menu = document.querySelector(".menu")
var ham = document.querySelector(".ham")
var xIcon = document.querySelector(".xIcon")
var menuIcon = document.querySelector(".menuIcon")
var release_links = document.getElementById('discogs')

ham.addEventListener("click", toggleMenu)
release_links.addEventListener("click", open_release_menu)

function toggleMenu() {
    if (menu.classList.contains("showMenu")) {
        menu.classList.remove("showMenu");
        xIcon.style.display = "none";
        menuIcon.style.display = "block";
    } else {
        menu.classList.add("showMenu");
        xIcon.style.display = "block";
        menuIcon.style.display = "none";
    }
}

function open_release_menu() {
    el = document.getElementById('release-links')

    links = document.getElementById('discogs')
    social = document.querySelector(".menu-social")

    el.style.height = social.offsetTop - links.offsetTop - links.clientHeight + "px"
    document.getElementById('release-links').classList.toggle("show");
    document.getElementById("release-expand-icon").classList.toggle("expand-more")
}

function change_lang(lang) {
    window.location.href = window.location.href.split('?')[0] + "?lang=" + lang;
}