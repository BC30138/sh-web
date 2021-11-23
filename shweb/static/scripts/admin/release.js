const monthNames = ["jan", "feb", "mar", "apr",
    "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
const required_string_fiedls = [
    "release_name", "type", "release_id", "bandcamp_link", "date"
]

var loadFile = function (event, id) {
    var output = document.getElementById(id);
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src);
    }
};

function url_checker(link) {
    try {
        const url = new URL(link);
        return true
    } catch (e) {
        return false
    }
}

function youtube_link_parser(link) {
    if (url_checker()) {
        const url = new URL(link);
        if (url.hostname === "www.youtube.com") {
            id = url.searchParams.get('v')
            if (id === null) {
                return ""
            }
            return id
        }
        else if (url.hostname === "youtu.be") {
            path_list = url.pathname.split('/')
            if (path_list.length !== 2) {
                return ""
            }
            return path_list[1]
        }
        return ""
    }
    return ""
}

$("#CreateRelease").on("submit", function () {
    var values = {};

    var is_error = false;
    $.each($(this).serializeArray(), function () {
        values[this.name] = this.value;
        // if (required_string_fiedls.includes(this.name) && this.value === "") {
        //     alert("Field '" + this.name + "' is emty")
        //     is_error = true;
        //     return false
        // }
    });
    if (is_error) {
        return false
    }


    var date_list = values['date'].split('-');
    var data = {
        release_name: values["release_name"],
        type: values["type"],
        release_id: values['release_id'],
        bandcamp_link: values['bandcamp_link'],
        date: date_list[2] + " " + monthNames[parseInt(date_list[1]) - 1] +
            " " + date_list[0],
        default_open_text: values['default_open_text'],
        services: [],
        tracklist: [],
        youtube_videos: []
    };

    var is_error = false;
    $('input[name^="service_"]').each(function (_index, member) {
        if (member.value !== "") {
            if (url_checker(member.value) === false) {
                alert("Invalid service link");
                is_error = true;
                return false;
            }
            data['services'].push(
                {
                    name: member.name.split("_")[1],
                    link: member.value
                }
            )
        }
    });
    if (is_error) {
        return false
    }
    if (data['services'].length === 0) {
        alert("At least one service must be not empty")
        return false
    }

    var used_names = [];
    var is_error = false;
    $('.track').each(function (_index, member) {
        var children = member.children;
        var track = {}
        for (var i = 0; i < children.length; i++) {
            if (children[i].type === "checkbox") {
                track[children[i].name] = children[i].checked
            }
            else if (children[i].tagName === "INPUT") {
                track[children[i].name] = children[i].value
            }
        }
        if (used_names.includes(track['id'])) {
            alert("Same ids for tracks not allowed")
            is_error = true
            return false
        }
        if (track['id'] === "" || track['name'] === "") {
            alert("Track's id and name must be not empty")
            is_error = true
            return false
        }
        used_names.push(track['id'])
        data['tracklist'].push(track)
    });
    if (is_error) {
        return false
    }

    var is_error = false;
    $('input[name="youtube_video"]').each(function (_index, member) {
        youtube_id = youtube_link_parser(member.value)
        if (youtube_id === "") {
            alert("Incorrect youtube link " + member.value)
            is_error = true
            return false
        }
        if (data['youtube_videos'].includes(youtube_id)) {
            alert("Youtube videos must be unique")
            is_error = true
            return false
        }
        data['youtube_videos'].push(youtube_id)
    });
    if (is_error) {
        return false
    }

    alert(JSON.stringify(data))

    var formData = new FormData();
    formData.append("cover", document.getElementById("cover").files[0]);
    formData.append("release", JSON.stringify(data))

    var base_url = window.location.origin + "/admin/release?action=" + document.getElementById("Submit").name;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE) {
            if (this.status === 200) {
                alert("a");
                return false;
            } else {
                alert('failed');
                return false;
            }
        }
    }
    xhr.open("POST", base_url);
    xhr.send(formData);
    return false
});

function add_div(it, wrapper, html) {
    if (it < maxField) {
        it++;
        $(wrapper).append(html);
    }
    return it
}

function remove_div(element, e) {
    e.preventDefault();
    $(element).parent('div').remove();
}

var maxField = 20;

var addTrack = $('#add_track');
var tracklistWrapper = $('.tracklist');
var trackHtml = `
    <div class="track">
        <div class="description"> Track name*: </div>
        <input name="name" />
        <div class="description"> Track id*: </div>
        <input name="id" />
        <div class="description"> Lyrics: </div>
        <input name="lyrics" />
        <div class="description"> Explicit: </div>
        <input type="checkbox" name="explicit" />
        <a href="javascript:void(0);" class="remove_button" id="remove_track">
            <img src="remove-icon.png"/>
        </a>
    </div>`;
var trackIt = 1;
$(addTrack).click(function () {
    trackIt = add_div(trackIt, tracklistWrapper, trackHtml)
});
$(tracklistWrapper).on('click', '#remove_track', function (e) {
    remove_div(this, e)
    trackIt--
});

var addYoutube = $('#add_youtube');
var youtubeWrapper = $('.youtube_videos');
var youtubeHtml = `
<div>
    <div class="description"> Youtube link: </div>
    <input name="youtube_video" />
    <a href="javascript:void(0);" class="remove_button" id="remove_youtube">
        <img src="remove-icon.png"/>
    </a>
</div>`;
var youtubeIt = 1;
$(addYoutube).click(function () {
    youtubeIt = add_div(youtubeIt, youtubeWrapper, youtubeHtml)
});
$(youtubeWrapper).on('click', '#remove_youtube', function (e) {
    remove_div(this, e)
    youtubeIt--
});
