import {
    load_data,
    query
} from "./utils.js";

export class CategorySelector {
    constructor() {
        this.categories = null;
        this.selector = document.getElementById("category_list");
        
        this.#init_list();
    }

    async #load_category() {
        this.categories = await load_data("data", "category.json")
            .then((data) => { return data["category"]; });
    }

    async #init_list() {
        await this.#load_category();

        this.categories.forEach((element) => {
            let li = document.createElement("li");
            let checkbox = document.createElement("input");
            let label = document.createElement("label");
            checkbox.type = "checkbox";
            li.classList.add("category");
            checkbox.name = "category";
            checkbox.value = element;
            label.innerHTML = element;
            label.addEventListener("click", function () {
                checkbox.checked = !checkbox.checked;
            }.bind(this));
            li.appendChild(label);
            li.appendChild(checkbox);
            this.selector.appendChild(li);
        });
    }
}

export class ResultDisplay {
    static #ROW_MAX = 3;

    constructor() {
        this.result = null;
        this.clusters_n = 8;
        this.result_block = document.getElementById("result");
        // true: category, false: list
        this.category_mode = true;
        this.category_block = null;
        this.list_block = null;

        this.#init_result_block();
    }

    async #load_result() {
        this.result = [];
        for(var i = 1; i <= this.clusters_n; i++)
            this.result.push(await query("books", null, [`cluster_id > ${i}`]));
        // console.log("load result");
        // console.log(this.result);
    }

    #create_cluster(title, idx) {
        let td = document.createElement("td");
        let div = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${title}_${idx}`;
        div.classList.add("cluster");
        td.classList.add("cluster");
        div.appendChild(label);
        td.appendChild(div);
        td.addEventListener("click", () => {
            location.hash = label.textContent;
            this.#load_cluster_block();
        });

        return td;
    }

    async #init_result_block() {
        await this.#load_result();
        this.#load_result_block(this.result);
    }

    #load_cluster_block() {
        let cluster = location.hash.split('_')[1];      // cluster_id (result's index + 1)
        this.category_mode = false;                     // list mode
        this.#clear_result_block();
        this.#load_result_block(this.result[cluster - 1]);
        let previous_page = document.createElement("button");
        previous_page.textContent = "上一頁";
        previous_page.classList.add("button");
        previous_page.addEventListener("click", () => {
            let url = new URL(location.href);
            url.hash = '';
            location.href = url.toString();
        });
        document.getElementById("function_bar").appendChild(previous_page);
    }

    #clear_result_block() {
        if(this.category_block != null)
            this.category_block.remove();
        if(this.list_block != null)
            this.list_block.remove();
    }

    #load_result_block(result) {
        if(this.category_mode) {                                                    // category block
            var idx = 1;
            let tr = document.createElement("tr");
            this.category_block = document.createElement("table");
            this.category_block.classList.add("result_table");
            result.forEach((_, key) => {
                tr.appendChild(this.#create_cluster("Cluster", key + 1));
                if(idx >= ResultDisplay.#ROW_MAX || key + 1 == result.length) {
                    this.category_block.appendChild(tr);
                    tr = document.createElement("tr");
                    idx = 0;
                }
                idx++;
            });
            
            this.result_block.appendChild(this.category_block);
        } else {                                                                    // list block
            this.list_block = document.createElement("ol");
            this.list_block.classList.add("result_list");
            for(let book_info of result) {
                // console.log("load book_info");
                // console.log(book_info);
                let li = document.createElement("li");
                let details = document.createElement("details");
                let summary = document.createElement("summary");
                let label = document.createElement("label");
                let book_details = `&emsp;ISBN13: ${book_info["ISBN13"]}<br>` +
                                   `&emsp;出版社: ${book_info["phouse_name"]}<br>` +
                                   `&emsp;出版時間: ${book_info["published_date"]}<br>` +
                                   `&emsp;作者: ${book_info["author_name"].join(", ")}<br>` +
                                   `&emsp;價錢: ${book_info["price"]}<br>` +
                                   `&emsp;頁數: ${book_info["pages"]} 頁<br>` +
                                   `&emsp;類別: ${book_info["category"]}<br>`;
                summary.textContent = book_info["book_name"];
                label.innerHTML = book_details;
                details.classList.add("result")
                details.appendChild(summary);
                details.appendChild(label);
                li.appendChild(details);
                this.list_block.appendChild(li);
            }

            this.result_block.appendChild(this.list_block);
        }
    }
}