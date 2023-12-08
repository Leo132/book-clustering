

export async function search(search_str, categories) {
    let categories_str = categories.join(';');
    // console.log(categories_str)
    return await load_data(`search?search_str=${search_str}&categories=${categories_str}`);
}

export async function query(type_, cols, conditions) {
    let args = (cols != null ? `cols=${cols.join(';')}` : '') +
               (conditions != null ? `&conditions=${conditions.join(';')}` : '');
    return await fetch(`http://localhost:8000/query/${type_}?${args}`)
        .then((response) => { return response.json(); });
}

export async function load_data(type_, file='') {
    if(file !== '')
        file = '/' + file;
    return await fetch(`http://localhost:8000/${type_}${file}`)
        .then((response) => { return response.json(); });
}

export function load_css(file) {
    let link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = file;
    document.getElementsByTagName("head")[0].appendChild(link);
}
