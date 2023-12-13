import { post_data, load_css } from "./utils.js";


window.addEventListener("load", () => {
    init();
});

function clear_error_info() {
    document.getElementById("name_error").textContent = '';
    document.getElementById("username_error").textContent = '';
    document.getElementById("password_confirm_error").textContent = '';
}

async function register_check() {
    let name = document.getElementById("name").value;
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let password_confirm = document.getElementById("password_confirm").value;
    let check_info = await post_data("http://localhost:8000/registercheck/", {
        "name": name,
        "username": username,
        "password": password,
        "password_confirm": password_confirm
    })

    // console.log(check_info);
    clear_error_info();
    if(check_info["is_name_exist"]) {
        document.getElementById("name").value = '';
        document.getElementById("name_error").textContent = "此名稱已存在";
    } else if(check_info["is_username_exist"]) {
        document.getElementById("username").value = '';
        document.getElementById("username_error").textContent = "此帳號已存在";
    } else if(password !== password_confirm) {
        document.getElementById("password_confirm").value = '';
        document.getElementById("password_confirm_error").textContent = "密碼不一致";
    } else {
        location.href = "http://localhost:8000/login";
    }
}

function init() {
    document.getElementById("register").onclick = register_check;

    load_css("./static/style/base.css");
    load_css("./static/style/register.css");
}