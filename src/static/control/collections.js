import { load_css } from "./utils.js";
import { ResultDisplay } from "./conponents.js";


window.addEventListener("load", () => {
    main();
});

async function init() {
    let result_block = await new ResultDisplay();
}

async function main() {
    await init();

    load_css("./static/style/base.css");
    load_css("./static/style/index.css");
}