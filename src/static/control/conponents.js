
export class CategorySelector {
    constructor(categories) {
        this.categories = categories;
        this.selected_categories = [];
        this.selector = document.getElementById("category_list");

        this.#init_list();
    }

    #update_state(checkbox, label_) {
        if(checkbox.checked)
            this.selected_categories.push(label_);
        else
            // remove `label_` from `this.selected_categories` array
            this.selected_categories = this.selected_categories.filter(function (label) {
                return label !== label_;
            });
        // console.log(this.selected_categories);
    }

    #init_list() {
        this.categories.forEach(element => {
            let li = document.createElement("li");
            let checkbox = document.createElement("input");
            let label = document.createElement("label");
            checkbox.type = "checkbox";
            // checkbox.classList.add("category");
            checkbox.name = "category";
            checkbox.value = element;
            label.innerHTML = element;
            checkbox.addEventListener("change", function () {
                this.#update_state(checkbox, label.textContent);
            }.bind(this));
            label.addEventListener("click", function () {
                checkbox.checked = !checkbox.checked;
                this.#update_state(checkbox, label.textContent);
            }.bind(this));
            li.appendChild(label);
            li.appendChild(checkbox);
            this.selector.appendChild(li);
        });
    }
}

export class SearchResult {
    constructor() {
        ;
    }
}