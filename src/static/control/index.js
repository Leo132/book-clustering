import {
    load_css,
    search,
} from "./utils.js"

import {
    CategorySelector,
    ResultDisplay,
} from "./conponents.js"


window.addEventListener("load", () => {
    main();
});

// for testing
function update_result(data) {
    document.getElementById("test").innerText = `seg_words: ${data["seg_words"]}\ncategories: ${data["categories"].join(", ")}\nresult: ${data["result"]}`;
}

async function init() {
    let category_selector = await new CategorySelector();
    let result_block = await new ResultDisplay();

    document.getElementById("search_form").onsubmit = async (e) => {
        e.preventDefault();             // important
        let search_str = document.getElementById("search_str").value;
        let categories = Array.from(document.querySelectorAll("input[name=category]:checked"))
            .map((checkbox) => { return checkbox.value; });
        console.log(search_str, categories);
        let data = await search(search_str, categories);
        update_result(data);
    };
}

async function main() {
    await init();

    load_css("./static/style/base.css");
    load_css("./static/style/index.css");
}