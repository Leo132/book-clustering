
window.addEventListener("load", function () {
    main();
});

class CategorySelector {
    constructor(categories) {
        this.categories = categories;
        this.selected_categories = [];
        this.selector = document.getElementById("category");

        const update_state = function(checkbox, label_) {
            if(checkbox.checked)
                this.selected_categories.push(label_);
            else
                // remove `label_` from `this.selected_categories` array
                this.selected_categories = this.selected_categories.filter(function (label) {
                    return label !== label_;
                });
            console.log(this.selected_categories);
        }.bind(this);

        this.categories.forEach(element => {
            const li = document.createElement("li");
            const checkbox = document.createElement("input");
            const label = document.createElement("label");
            checkbox.setAttribute("type", "checkbox");
            label.innerHTML = element;
            checkbox.addEventListener("change", function () {
                update_state(checkbox, label.textContent);
            });
            label.addEventListener("click", function () {
                checkbox.checked = !checkbox.checked;
                update_state(checkbox, label.textContent);
            }.bind(this));
            li.appendChild(label);
            li.appendChild(checkbox);
            this.selector.appendChild(li);
        });
    }

}

function test() {
    // const data = require("./test.json");
    // console.log(data);
}

function main() {
    const categories = ["科學", "社會", "人文"];                // should be given by server
    const category_selector = new CategorySelector(categories);

    // test();
}