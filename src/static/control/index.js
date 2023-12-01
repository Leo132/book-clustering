import {
    load_css,
    load_data,
    search,
} from "./utils.js"

import {
    CategorySelector,
    SearchResult,
} from "./conponents.js"


window.addEventListener("load", () => {
    main();
});


async function load_category_list() {
    let categories = await load_data("data", "category.json")
        .then((data) => { return data["category"]; });
    let category_selector = new CategorySelector(categories);
}

function load_search_result() {
    ;
}

// for testing
function update_result(data) {
    document.getElementById("result").innerText = `seg_words: ${data["seg_words"]}\ncategories: ${data["categories"].join(", ")}\nresult: ${data["result"]}`;
}

async function init() {
    await load_category_list();
    load_search_result();
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