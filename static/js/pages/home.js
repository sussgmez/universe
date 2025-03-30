async function get_publications(page=1) {
    await fetch(`./publication/list?page=${page}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $('#id_publications').append(data);
    })
    .finally(() => {

        let publications = $('.publication').get();

        publications.forEach(publication => {
            let publication_id = publication.getAttribute('publication-id');
            let aux_publications = $(`.publication[publication-id=${publication_id}]`);
            if (aux_publications.length > 1) {
                aux_publications[1].remove();
            }
        });

    })
}

function show_menu(div) {
    $(div).children('.publication-menu').show();
}

$(document).ready(function () {
    get_publications();
});