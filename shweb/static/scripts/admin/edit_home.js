// EDITOR

editor = monaco.editor.create(document.getElementById('code'), {
    value: code_tabs['web']['content'],
    language: 'html',
    theme: 'vs-dark',
});

languages = {
    "style": "css",
    "content": "html"
}

open_tab = ['web', 'content']

var editor_wrapper = $('#code-editor');

function save_code() {
    code_tabs[open_tab[0]][open_tab[1]] = editor.getValue()
}

function toggle_select(clicked_tab) {
    for (var i = 0; i < open_tab.length; i++) {
        if (clicked_tab[i] !== open_tab[i]) {
            $(`#${clicked_tab[i]}`).toggleClass("selected")
            $(`#${open_tab[i]}`).toggleClass("selected")
            open_tab[i] = clicked_tab[i]
        }
    }
}

function change_tab(tab) {
    save_code()
    editor.getModel().setValue(code_tabs[tab[0]][tab[1]]);
    monaco.editor.setModelLanguage(editor.getModel(), languages[tab[1]]);
    toggle_select(tab)
}
$(editor_wrapper).on('click', ".code-tabs .tab-button", function () {
    change_tab([open_tab[0], this.id])
});

$(editor_wrapper).on('click', ".device-tabs .tab-button", function () {
    change_tab([this.id, open_tab[1]])
});

// FILES

files = {}
delete_from_cloud = []
var files_wrapper = $('#image-list-display');
var files_it = 1;
var maxField = 20;

$("#file-container").change(function () {
    file = $(this).prop('files')[0]
    $(this).val("")
    if (file.name in files) {
        alert("Such file alredy exists")
        return false
    }
    add_files([[file.name, file]])
});

function init_files(files) {
    add_files(files)
}

function add_div(it, wrapper, html) {
    if (it < maxField) {
        $(wrapper).append(html);
        return true
    }
    return false
}

function add_files(file_list) {
    for (const file of file_list) {
        if (add_div(files_it, files_wrapper, `
        <div class="one-line-parameter" id="${file[0]}">
            <div>${file[0]}</div>
            <a href="javascript:void(0);" class="remove_button" id="remove_file">
                <img src="/static/images/icons/remove.svg"/>
            </a>
        </div>`)) {
            code_tabs['files_list'].push(file[0])
            files[file[0]] = file[1]
            files_it++
        }
        else {
            break
        }
    }
}

$(files_wrapper).on('click', '#remove_file', function (e) {
    e.preventDefault();
    var file_div = $(this).parent('div')
    var file_id = file_div.attr('id')
    if (typeof files[file_id] === "string") {
        delete_from_cloud.push(file_id)
    }
    delete files[file_id]

    code_tabs['files_list'].splice(code_tabs['files_list'].indexOf(file_id), 1);

    file_div.remove();
    files_it--
});

// CONTROLS

var controls_wrapper = $('.index-control-buttons');

function toggle_modal_loading() {
    $("body").toggleClass("loading")
}

$(document).bind('keydown', function (e) {
    if (e.ctrlKey && (e.which == 83)) {
        e.preventDefault();
        return false;
    }
});

$(controls_wrapper).on('click', '#download-template', function (e) {
    toggle_modal_loading()
    save_code()
    var zip = new JSZip();
    zip.file("index.json", JSON.stringify(code_tabs, null, 4));
    promises = []
    for (let [key, value] of Object.entries(files)) {
        if (typeof value === "string") {
            promises.push(new Promise(function (resolve, reject) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', value);
                xhr.responseType = 'blob';
                xhr.onload = function (e) {
                    var blob = e.currentTarget.response;
                    zip.file(`files/${key}`, blob, { base64: true });
                    resolve(xhr.response)
                }
                xhr.send();
            }))
        } else {
            zip.file(`files/${key}`, value, { base64: true });
        }
    }

    Promise.all(promises).then((values) => {
        zip.generateAsync({ type: "blob" })
            .then(function (content) {
                toggle_modal_loading()
                saveAs(content, "template.zip");
            });
    });
});

$(controls_wrapper).on('click', '#submit-changes', function (e) {
    var formData = new FormData();
    for (let [key, value] of Object.entries(files)) {
        if (typeof value !== "string") {
            formData.append(key, value);
        }
    }
    formData.append("index_code", JSON.stringify(code_tabs))
    formData.append("delete", JSON.stringify(delete_from_cloud))

    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.onload = function () {
        if (xhr.responseURL !== window.location.href) {
            window.location.href = xhr.responseURL
        }
        else if (xhr.status === 200) {
            alert("Success! Changes will be applied soon");
            window.location.href = window.location.origin + "/admin/"
        }
        else if (xhr.status === 400 && "status" in xhr.response) {
            alert(xhr.response['status']);
        }
        else {
            alert('Cannot make request, try again later');
            return false;
        }
    }

    xhr.open("PUT", window.location.href);
    xhr.send(formData);
});
