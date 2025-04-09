async function get_publications(page=1) {
    publication = $('#id_publication').attr('main-publication-id');
    await fetch(`../publication/list/comment?page=${page}&publication=${publication}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $('#id_comments').append(data);
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

$(document).ready(function () {
    get_publications();
});

$(document).click(function (e) { 
    $('.main-publication__menu').hide();
});