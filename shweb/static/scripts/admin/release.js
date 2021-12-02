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
        $(wrapper).append(html);
        return true
    }
    return false
}

var maxField = 20;

var tracklistWrapper = $('.tracklist');

function remove_track(element, e) {
    e.preventDefault();
    $(this).parent('div').parent('div').remove();
}

var trackIt = 0;
$(tracklistWrapper).on('click', "#add_track", function () {
    add_div(trackIt, tracklistWrapper, `
    <div class="add-track">
        <div class="description"> Track name*: </div>
        <div class="one-line-parameter">
            <input name="name" type="text"/>

        </div>
        <div class="description"> Lyrics: </div>
        <textarea name="lyrics"></textarea>
        <div class="one-line-parameter">
            <div style="display: flex; align-items: center;">
                <div class="description"> Explicit: </div>
                <input type="checkbox" name="explicit" />
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <button class="release-control-button" id="save_track">save</button>
                <button class="release-control-button" id="cancel_add_track">cancel</button>
            </div>
        </div>
    </div>`)
});
$(tracklistWrapper).on('click', '#cancel_add_track', function (e) {
    e.preventDefault();
    $(this).parent('div').parent('div').parent('div').remove();
});

$(tracklistWrapper).on('click', '#save_track', function (e) {
    e.preventDefault();
    $(this).parent('div').parent('div').parent('div').remove();

    add_div(trackIt, tracklistWrapper, `
    <div class="one-line-parameter, track">
        1. Марш
        <a href="javascript:void(0);" class="remove_button" id="remove_track">
            <img src="/static/images/icons/remove.svg"/>
        </a>
    </div>`)
    trackIt++
});

$(tracklistWrapper).on('click', '#remove_track', function (e) {
    e.preventDefault();
    $(this).parent('div').remove();
    trackIt--
});

var youtubeWrapper = $('.youtube-videos');
var youtubeHtml = `
<div class="one-line-parameter">
    <input name="youtube_video" type="url" placeholder="https://youtu.be/"/>
    <a href="javascript:void(0);" class="remove_button" id="remove_youtube">
        <img src="/static/images/icons/remove.svg"/>
    </a>
</div>`;
var youtubeIt = 0;
$(youtubeWrapper).on('click', '#add_youtube', function (e) {
    if (add_div(youtubeIt, youtubeWrapper, youtubeHtml)) {
        youtubeIt++
    }
});
$(youtubeWrapper).on('click', '#remove_youtube', function (e) {
    e.preventDefault();
    $(this).parent('div').remove();
    youtubeIt--
});
