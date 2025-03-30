async function get_publications(page=1) {
    text = $('#id_search_text').val();
    category = $('#id_category_input').val();
    await fetch(`../publication/list/search?page=${page}&text=${text}&category=${category}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $('#id_publications').append(data);
    })
    .finally(() => {

        let publications = $('.publication').get();

        publications.forEach(publication => {
            publication_id = publication.getAttribute('publication-id');
            aux_publications = $(`.publication[publication-id=${publication_id}]`);
            if (aux_publications.length > 1) {
                aux_publications[1].remove();
            }
        });

    })
}

async function get_profiles(page=1) {
    text = $('#id_search_text').val();
    await fetch(`../profile/list/search?page=${page}&text=${text}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $("#id_button_get_profiles").remove();
        $('#id_profiles').append(data);
    })
}


$(document).ready(function () {
    get_publications();
    get_profiles();
});