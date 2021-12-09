editor = monaco.editor.create(document.getElementById('code'), {
    value: code_tabs['web']['content'],
    language: 'html',
    theme: 'vs-dark',
});

// monaco.editor.setModelLanguage(editor.getModel(), "css")


// function set_style(code) {
// }