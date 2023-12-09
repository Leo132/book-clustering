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

async function init() {
    let category_selector = await new CategorySelector();
    let result_block = await new ResultDisplay();

    // keyword searching and category filtering
    document.getElementById("search_form").onsubmit = async (e) => {
        e.preventDefault();                                                 // important
        let search_str = document.getElementById("search_str").value;
        let ws = await word_segment(search_str)
            .then((response) => response.seg_words);
        let categories = Array.from(document.querySelectorAll("input[name=category]:checked"))
            .map((checkbox) => checkbox.value);
        let cluster = location.hash.split('_')[1];                          // cluster_id
        // console.log(search_str, ws, categories);                            // for debugging

        // category filtering condition
        var category_condition = [];
        for(let category of categories)
            category_condition.push(`category = "${category}"`);
        if(category_condition.length > 0)
            category_condition = `(${category_condition.join(" or ")})`;

        // keyword searching condition
        var keyword_condition = [`book_name like "%${search_str}%"`];
        for(let keyword of ws) {
            if(keyword === search_str) continue;
            keyword_condition.push(`book_name like "%${keyword}$"`);
        }
        keyword_condition = `(${keyword_condition.join(" or ")})`;

        // cluster condition
        var cluster_condition = [];
        if(cluster != undefined)
            cluster_condition.push(`cluster_id = ${cluster}`);

        // switch to list mode
        result_block.category_mode = false;
        // update result block with conditions
        result_block.update_result_block([].concat(
            [keyword_condition],
            cluster_condition,
            typeof category_condition === "string" ? [category_condition] : []
        ));
    };
}

async function main() {
    await init();

    load_css("./static/style/base.css");
    load_css("./static/style/index.css");
}