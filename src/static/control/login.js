import { post_data, load_css } from "./utils.js";


window.addEventListener("load", () => {
    init();
});

function clear_error_info() {
    document.getElementById("username_error").textContent = '';
    document.getElementById("password_error").textContent = '';
}

async function login_check() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let check_info = await post_data("http://localhost:8000/logincheck/", {
        "username": username,
        "password": password
    });

    // console.log(check_info);
    clear_error_info();
    if(!check_info["is_username_exist"]) {
        document.getElementById("username").value = '';
        document.getElementById("username_error").textContent = "帳號不存在";
    } else if(!check_info["is_password_correct"]) {
        document.getElementById("password").value = '';
        document.getElementById("password_error").textContent = "密碼錯誤";
    } else {
        localStorage.setItem("user_info", JSON.stringify(check_info["user_info"]));
        location.href = "http://localhost:8000/index";
    }
}

function init() {
    document.getElementById("login").onclick = login_check;

    load_css("./static/style/base.css");
    load_css("./static/style/login.css");
}