// GLOBALS

const monthNames = ["jan", "feb", "mar", "apr",
    "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
var maxField = 20;

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
var tracklist = {}

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
    $('#default_open_track').append($('<option>', {
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

    $('#default_open_track option').each(function () {
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
            $('#default_open_track option').each(function () {
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
        <input name="youtube_video" type="url" placeholder="https://youtu.be/" id="youtube_video"/>
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
const blank_parameters = {
    '#cover': {
        name: "cover",
        type: "file",
        required: true
    },
    '#og': {
        name: "og",
        type: "file",
        required: true
    },
    'input[name^="service_"]': {
        name: "services",
        type: "list",
        element_type: "url",
        at_least_one: true
    },
    'input[name="youtube_video"]': {
        name: "youtube_videos",
        type: "list",
        element_type: "youtube_url"
    },
    '#release_name': {
        name: "release_name",
        type: "string",
        required: true
    },
    '#release_type': {
        name: "type",
        type: "string",
        required: true
    },
    '#release_date': {
        name: "date",
        type: "date",
        required: true
    },
    '#release_bandcamp_link': {
        name: "bandcamp_link",
        type: "url",
        required: true
    },
    '#default_open_track': {
        name: "default_open_text",
        type: "string"
    }
}

function url_checker(link) {
    try {
        const url = new URL(link);
        return true
    } catch (e) {
        return false
    }
}

function youtube_link_parser(link) {
    if (url_checker(link)) {
        const url = new URL(link);
        if (url.hostname === "www.youtube.com") {
            id = url.searchParams.get('v')
            if (id === null) {
                return false
            }
            return id
        }
        else if (url.hostname === "youtu.be") {
            path_list = url.pathname.split('/')
            if (path_list.length !== 2) {
                return false
            }
            return path_list[1]
        }
        return false
    }
    return false
}

function type_converter(object_value, type) {
    if (type === "url") {
        if (url_checker(object_value)) {
            return object_value
        }
        return false
    }
    else if (type === "youtube_url") {
        return youtube_link_parser(object_value)
    }
    else if (type === "date") {
        date_list = object_value.split('-')
        return date_list[2] + " " + monthNames[parseInt(date_list[1]) - 1] +
            " " + date_list[0]
    }
    else {
        return object_value
    }
}

function json_data_builder() {
    var formData = new FormData();
    var data = {}

    for (const [key, properties] of Object.entries(blank_parameters)) {
        object = $(key)

        // FILES IN FORM-DATA
        if (properties['type'] === "file") {
            files = object.prop('files')
            if (properties['required'] && files.length === 0) {
                return [1, `File "${object.attr('id')}" is required`]
            }
            formData.append(properties['name'], object.prop('files')[0]);
            continue
        }

        // JSON-DATA
        // EMPTY STRING CHECK
        if (properties["required"] && object.val() === "") {
            return [1, `Field "${object.attr('id')}" is empty`]
        }

        if (properties['type'] === "list") {
            result_object = []
            item_values = []

            for (let item of object) {
                if (item.value !== "") {
                    item_value = type_converter(item.value, properties['element_type'])
                    if (item_value === false) {
                        return [1, `Link "${item.id}" is invalid`]
                    }
                    item_values.push([item.name, item_value])
                }
            }

            if (properties['name'] === "services") {
                item_values.forEach(function (item) {
                    list_item = {
                        name: item[0].split("_")[1]
                    }
                    list_item['link'] = item[1]
                    result_object.push(list_item)
                });
            }
            else {
                item_values.forEach(function (item) {
                    result_object.push(item[1])
                });
            }

            if (properties["at_least_one"] && result_object.length === 0) {
                return [1, `At least one field required in "${properties['name']}"`]
            }
        }
        else {
            result_object = type_converter(object.val(), properties['type'])
            if (result_object === false) {
                return [1, `Incorrect value of ${object.attr('id')}`]
            }
        }
        data[properties['name']] = result_object
    }

    if (Object.keys(tracklist).length === 0) {
        return [1, `At least one track is required`]
    }
    data['release_id'] = make_id(data['release_name'])
    data['tracklist'] = Object.values(tracklist)

    formData.append("release", JSON.stringify(data))
    return [0, formData]
}

$("#submit-release").on("click", function () {
    building_result = json_data_builder()

    if (building_result[0] !== 0) {
        alert(building_result[1])
        return false
    }
    formData = building_result[1]

    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert("Success! Changes will be applied soon");
            window.location.href = xhr.responseURL
        }
        else {
            alert('Cannot make request, try again later');
            return false;
        }
    }
    xhr.open("POST", window.location.href);
    xhr.send(formData);
    return false
});