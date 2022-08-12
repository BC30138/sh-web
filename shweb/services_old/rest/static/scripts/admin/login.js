function valid(ifcase, element) {
    if (ifcase) {
        element.classList.remove("invalid")
        element.classList.add("valid")
    } else {
        element.classList.remove("valid")
        element.classList.add("invalid")
    }
}

function cur_credentials_checker() {
    var username_element = document.getElementById("username")
    var cur_passwd_element = document.getElementById("cur_password")
    var checkers = [
        username_element.value !== "",
        cur_passwd_element.value !== ""
    ]
    return checkers
}

function code_checker() {
    var code_element = document.getElementById("code")
    var checkers = [code.value !== ""]
    return checkers
}

function new_password_checker() {
    var password_element = document.getElementById("password")
    var confirm_element = document.getElementById("confirm")

    var equal_passwords_element = document.getElementById("equal_passwords")
    var lower_case_element = document.getElementById("lower_case")
    var upper_case_element = document.getElementById("upper_case")
    var is_number_element = document.getElementById("is_number")
    var min_char_element = document.getElementById("min_char")


    valid(
        password_element.value === confirm_element.value && password_element.value.length !== 0,
        equal_passwords_element
    )
    valid(/[a-z]/.test(password_element.value), lower_case_element)
    valid(/[A-Z]/.test(password_element.value), upper_case_element)
    valid(/[0-9]/.test(password_element.value), is_number_element)
    valid(password_element.value.length >= 8, min_char_element)


    var statuses = [
        equal_passwords_element.classList.contains("valid"),
        lower_case_element.classList.contains("valid"),
        upper_case_element.classList.contains("valid"),
        is_number_element.classList.contains("valid"),
        min_char_element.classList.contains("valid")
    ]
    return statuses
}

function disable_checker(checkers, button_id) {
    var statuses = []
    checkers.forEach((item, index) => statuses = statuses.concat(item()));
    var button_element = document.getElementById(button_id)
    if (statuses.includes(false)) {
        button_element.disabled = true;
    } else {
        button_element.disabled = false;
    }
}