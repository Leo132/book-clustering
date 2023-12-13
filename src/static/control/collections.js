import {
    load_css,
} from "./utils.js"

import {
    ResultDisplayList,
} from "./conponents.js"


window.addEventListener("load", () => {
    main();
});

async function init() {
    let user_info = JSON.parse(localStorage.getItem("user_info"));
    let result_block = await new ResultDisplayList(user_info["user_id"]);
}

async function main() {
    await init();

    load_css("./static/style/base.css");
    load_css("./static/style/collections.css");
}