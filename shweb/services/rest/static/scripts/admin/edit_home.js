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

$(controls_wrapper).on('click', '#submit-changes', function (e) {
    toggle_modal_loading()
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
        toggle_modal_loading()
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

function getBase64(filename, file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve([filename, reader.result]);
        reader.onerror = error => reject(error);
    });
}

$(controls_wrapper).on('click', '#preview-template', function (e) {
    save_code()

    var request_data = code_tabs[open_tab[0]]
    request_data['images'] = {}
    promises = []
    for (let [key, value] of Object.entries(files)) {
        if (typeof value !== "string") {
            promises.push(getBase64(key, value))
        }
    }

    Promise.all(promises).then(
        b64images => {
            b64images.forEach(image_object => {
                if (image_object) {
                    request_data['images'][image_object[0]] = image_object[1]
                }
            })
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'document';
            xhr.onload = function () {
                if (xhr.status === 304) {
                    window.location.href = xhr.responseURL
                }
                else if (xhr.status === 200) {
                    $("#previewFrame").remove();
                    var iframe = document.createElement('iframe');
                    if (open_tab[0] === "web") {
                        height = "500px"
                        width = "1000px"
                    }
                    else {
                        height = "667px"
                        width = "375px"
                    }

                    iframe.setAttribute("id", "previewFrame");
                    iframe.setAttribute("height", height);
                    iframe.setAttribute("width", width);
                    iframe.setAttribute("style", 'style="-webkit-transform:scale(0.5);-moz-transform-scale(0.5);')
                    var html = new XMLSerializer().serializeToString(xhr.response);
                    document.getElementById("frame-wrapper").appendChild(iframe)
                    iframe.contentWindow.document.open();
                    iframe.contentWindow.document.write(html);
                    iframe.contentWindow.document.close();
                }
                else {
                    alert('error');
                    return false;
                }
            }

            xhr.open("POST", window.location.origin + "/admin/index-edit/preview?device=" + open_tab[0]);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(JSON.stringify({
                "index_code": {
                    "style": request_data['style'],
                    "content": request_data['content']
                },
                "images": request_data['images']
             }));
        }

    )
});

// TEMPLATES

var templates_wrapper = $('.template-control-buttons');

$(templates_wrapper).on('click', '#download-template', function (e) {
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

$("#upload-template").change(function () {
    file = $(this).prop('files')[0]
    $(this).val("")

    var zip = new JSZip();
    zip.loadAsync(file).then(function (zip) {
        var promises = []
        Object.keys(zip.files).forEach(function (filename) {
            if (!filename.endsWith("/")) {
                if (filename === "index.json") {
                    promise = zip.files[filename].async('string').then(
                        file_data => {
                            return new Promise(function (resolve, reject) {
                                code = JSON.parse(file_data)
                                code_tabs["web"] = code['web']
                                code_tabs["mobile"] = code['mobile']
                                editor.getModel().setValue(code_tabs[open_tab[0]][open_tab[1]]);
                                resolve()
                            })
                        }
                    )
                    promises.push(promise)
                }
                else {
                    promise = zip.files[filename].async('blob').then(
                        file_data => {
                            return new Promise(function (resolve, reject) {
                                filename = filename.split("/").pop();
                                resolve([filename, new File([file_data], filename, { type: `image/${filename.split('.').pop()}` })])
                            })
                        }
                    )
                    promises.push(promise)
                }
            }
        })
        Promise.all(promises).then(result => {
            document.getElementById("image-list-display").textContent = ''
            files = {}
            delete_from_cloud = code_tabs['files_list']
            code_tabs['files_list'] = []
            files_list = []
            result.forEach(file_object => {
                if (file_object) {
                    files_list.push(file_object)
                }
            })
            add_files(files_list)
        })
    })
});