import {
    load_css,
    word_segment,
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
        let ws = await word_segment(search_str)
            .then((response) => response.seg_words);
        let categories = Array.from(document.querySelectorAll("input[name=category]:checked"))
            .map((checkbox) => checkbox.value);
        console.log(search_str, ws, categories);
        var category_condition = [];
        var keyword_condition = [`book_name like "%${search_str}%"`];
        for(let category of categories)
            category_condition.push(`category = "${category}"`);
        if(category_condition.length > 0)
            category_condition = `(${category_condition.join(" or ")})`;
        for(let keyword of ws) {
            if(keyword === search_str) continue;
            keyword_condition.push(`book_name like "%${keyword}$"`);
        }
        keyword_condition = `(${keyword_condition.join(" or ")})`;
        result_block.update_result_block([keyword_condition].concat(typeof category_condition === "string" ? [category_condition] : []));
    };
}

async function main() {
    await init();

    load_css("./static/style/base.css");
    load_css("./static/style/index.css");
}