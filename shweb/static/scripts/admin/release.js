// GLOBALS

const monthNames = ["jan", "feb", "mar", "apr",
    "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
const required_string_fiedls = [
    "release_name", "type", "release_id", "bandcamp_link", "date"
]
var maxField = 20;
var tracklist = {}

function make_id(word) {
    var answer = "";
    var a = {};

    a["Ё"] = "YO"; a["Й"] = "I"; a["Ц"] = "TS"; a["У"] = "U"; a["К"] = "K"; a["Е"] = "E"; a["Н"] = "N"; a["Г"] = "G"; a["Ш"] = "SH"; a["Щ"] = "SCH"; a["З"] = "Z"; a["Х"] = "H"; a["Ъ"] = "'";
    a["ё"] = "yo"; a["й"] = "i"; a["ц"] = "ts"; a["у"] = "u"; a["к"] = "k"; a["е"] = "e"; a["н"] = "n"; a["г"] = "g"; a["ш"] = "sh"; a["щ"] = "sch"; a["з"] = "z"; a["х"] = "h"; a["ъ"] = "'";
    a["Ф"] = "F"; a["Ы"] = "I"; a["В"] = "V"; a["А"] = "a"; a["П"] = "P"; a["Р"] = "R"; a["О"] = "O"; a["Л"] = "L"; a["Д"] = "D"; a["Ж"] = "ZH"; a["Э"] = "E";
    a["ф"] = "f"; a["ы"] = "i"; a["в"] = "v"; a["а"] = "a"; a["п"] = "p"; a["р"] = "r"; a["о"] = "o"; a["л"] = "l"; a["д"] = "d"; a["ж"] = "zh"; a["э"] = "e";
    a["Я"] = "Ya"; a["Ч"] = "CH"; a["С"] = "S"; a["М"] = "M"; a["И"] = "I"; a["Т"] = "T"; a["Ь"] = "'"; a["Б"] = "B"; a["Ю"] = "YU";
    a["я"] = "ya"; a["ч"] = "ch"; a["с"] = "s"; a["м"] = "m"; a["и"] = "i"; a["т"] = "t"; a["ь"] = "'"; a["б"] = "b"; a["ю"] = "yu";
    a[" "] = "_"; a["-"] = "_";

    for (i in word) {
        if (word.hasOwnProperty(i)) {
            if (a[word[i]] === undefined) {
                answer += word[i];
            } else {
                answer += a[word[i]];
            }
        }
    }
    return answer;
}

function add_div(it, wrapper, html) {
    if (it < maxField) {
        $(wrapper).append(html);
        return true
    }
    return false
}

// IMAGES

var loadFile = function (event, id) {
    var output = document.getElementById(id);
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src);
    }
};

// TRACKLIST

function create_track(track_blank) {
    var track = {
        "name": track_blank.find('#track_name').val(),
        "lyrics": track_blank.find('#track_lyrics').val(),
        "explicit": track_blank.find('#track_explicit').is(':checked')
    }

    if (track['name'] == "") {
        alert("Track name is empty")
        return false
    }

    track['id'] = make_id(track['name'])
    return track
}

function get_track_html(track, track_it) {
    return `
    <div class="track" style="order:${track_it}" id="track_${track['id']}">
        <div id="track_head">
            ${track_it}. ${track['name']}
        </div>

        <div class="track-controls">
            <a href="javascript:void(0);" class="remove_button" id="edit_track">
                <img src="/static/images/icons/edit.svg"/>
            </a>
            <a href="javascript:void(0);" class="remove_button" id="remove_track">
                <img src="/static/images/icons/remove.svg"/>
            </a>
            <div class="order-buttons">
                <div class="change-order-up">
                    <img src="/static/images/icons/up.svg" alt="" class="up-icon">
                </div>
                <div class="change-order-down">
                    <img src="/static/images/icons/down.svg" alt="" class="up-icon">
                </div>
            </div>
        </div>
    </div>`
}

function get_add_track_html(track, track_it, is_update) {
    var order_css = ""
    var track_args = {
        "track_name": "",
        "track_lyrics": "",
        "track_explicit": ""
    }
    var save_id = "save_track"
    var cancel_id = "cancel_add_track"
    var current_id_input = ""

    if (is_update === true) {
        order_css = `style="order:${track_it}"`;
        track_args['track_name'] = `value="${track['name']}"`
        track_args['track_lyrics'] = track['lyrics']
        if (track['explicit']) {
            track_args['track_explicit'] = "checked";
        }
        save_id = "update_track"
        cancel_id = "cancel_update_track"
        current_id_input = `<input name="current_id" type="hidden" id="current_id" value="${track['id']}"/>`
    }

    return `
    <div class="add-track" ${order_css}>
        ${current_id_input}
        <div class="description"> Track name*: </div>
        <div class="one-line-parameter">
            <input name="name" type="text" id="track_name" ${track_args['track_name']}/>
        </div>
        <div class="description"> Lyrics: </div>
        <textarea name="lyrics" id="track_lyrics">${track_args['track_lyrics']}</textarea>
        <div class="one-line-parameter">
            <div style="display: flex; align-items: center;">
                <div class="description"> Explicit: </div>
                <input type="checkbox" name="explicit" id="track_explicit" ${track_args['track_explicit']}/>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <button class="release-control-button" id="${save_id}">save</button>
                <button class="release-control-button" id="${cancel_id}">cancel</button>
            </div>
        </div>
    </div>`
}

var tracklistWrapper = $('.tracklist');
var trackIt = 0;
$(tracklistWrapper).on('click', "#add_track", function () {
    add_div(trackIt, tracklistWrapper, get_add_track_html(null, null, false))
});

$(tracklistWrapper).on('click', '#cancel_add_track', function (e) {
    e.preventDefault();
    $(this).parent('div').parent('div').parent('div').remove();
});

$(tracklistWrapper).on('click', '#save_track', function (e) {
    e.preventDefault();
    var track_blank = $(this).parent('div').parent('div').parent('div')
    var track = create_track(track_blank)
    if (track === false) {
        return false
    }
    if (Object.keys(tracklist).find(key => tracklist[key]['id'] === track['id'])) {
        alert("Such track id is alredy exists")
        return false
    }

    track_blank.remove()

    trackIt++
    tracklist[trackIt] = track
    add_div(trackIt, tracklistWrapper, get_track_html(track, trackIt))
    $('#default-open-track').append($('<option>', {
        value: track['id'],
        text: track['name']
    }));
});

$(tracklistWrapper).on('click', '#edit_track', function (e) {
    e.preventDefault();
    var track_div = $(this).parent('div').parent('div');
    var order = track_div.css("order");
    var track = tracklist[order];

    $(track_div).replaceWith(get_add_track_html(track, order, true));
});

$(tracklistWrapper).on('click', '#update_track', function (e) {
    e.preventDefault();
    var track_blank = $(this).parent('div').parent('div').parent('div')
    var current_id = track_blank.find('#current_id').val()
    var track_it = track_blank.css("order")
    var track = create_track(track_blank)
    if (track === false) {
        return false
    }

    track_blank.remove()

    tracklist[track_it] = track

    add_div(track_it, tracklistWrapper, get_track_html(track, track_it))

    $('#default-open-track option').each(function () {
        if ($(this).val() == `${current_id}`) {
            $(this).attr("value", track['id']);
            $(this).text(track['name']);
        }
    });
});

$(tracklistWrapper).on('click', '#cancel_update_track', function (e) {
    e.preventDefault();
    var track_blank = $(this).parent('div').parent('div').parent('div')
    var track_it = track_blank.css("order")
    var track = tracklist[track_it]
    track_blank.remove()

    add_div(track_it, tracklistWrapper, get_track_html(track, track_it))
});

$(tracklistWrapper).on('click', '#remove_track', function (e) {
    e.preventDefault();
    var track = $(this).parent('div').parent('div')

    var track_order = parseInt(track.css("order"))
    new_tracklist = {}
    for (var key in tracklist) {
        if (parseInt(key) < track_order) {
            new_tracklist[key] = tracklist[key]
        }
        else if (parseInt(key) > track_order) {
            new_order = parseInt(key) - 1
            new_tracklist[new_order] = tracklist[key]

            iter_track = $(`#track_${tracklist[key]['id']}`)

            iter_track.css("order", `${new_order}`)
            track_head_link = iter_track.find("#track_head").text(`${new_order}. ${tracklist[key]['name']}`)
        }
        else {
            $('#default-open-track option').each(function () {
                if ($(this).val() == `${tracklist[key]['id']}`) {
                    $(this).remove();
                }
            });
        }
    }
    tracklist = new_tracklist
    track.remove();
    trackIt--
});

function change_order(element, type) {
    var order = parseInt($(element).parent().parent().parent().css("order"))
    var left_string = ""
    var right_string = ""

    if (type === "up") {
        if (order === 1) {
            return false
        }

        left_string = "" + (order - 1)
        right_string = "" + order
    }
    else if (type === "down") {
        if (order === Object.keys(tracklist).length) {
            return false
        }

        left_string = "" + (order + 1)
        right_string = "" + order
    }


    tmp_obj = tracklist[right_string]
    tracklist[right_string] = tracklist[left_string]
    tracklist[left_string] = tmp_obj

    left_track = $("#track_" + tracklist[left_string]['id'])
    left_track.css('order', left_string)
    left_track.find("#track_head").text(`${left_string}. ${tracklist[left_string]['name']}`)

    right_track = $("#track_" + tracklist[right_string]['id'])
    right_track.css('order', right_string)
    right_track.find("#track_head").text(`${right_string}. ${tracklist[right_string]['name']}`)
}

$(tracklistWrapper).on('click', ".change-order-up", function () {
    change_order($(this), "up")
});

$(tracklistWrapper).on('click', ".change-order-down", function () {
    change_order($(this), "down")
});

// YOUTUBE

var youtubeWrapper = $('.youtube-videos');
var youtubeIt = 0;
$(youtubeWrapper).on('click', '#add_youtube', function (e) {
    if (add_div(youtubeIt, youtubeWrapper, `
    <div class="one-line-parameter">
        <input name="youtube_video" type="url" placeholder="https://youtu.be/"/>
        <a href="javascript:void(0);" class="remove_button" id="remove_youtube">
            <img src="/static/images/icons/remove.svg"/>
        </a>
    </div>`)) {
        youtubeIt++
    }
});
$(youtubeWrapper).on('click', '#remove_youtube', function (e) {
    e.preventDefault();
    $(this).parent('div').remove();
    youtubeIt--
});


// POST REQUEST
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
        if (required_string_fiedls.includes(this.name) && this.value === "") {
            alert("Field '" + this.name + "' is emty")
            is_error = true;
            return false
        }
        values[this.name] = this.value;
    });
    if (is_error) {
        return false
    }


    var date_list = values['date'].split('-');
    var data = {
        release_name: values["release_name"],
        release_id: make_id(values["release_name"]),
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