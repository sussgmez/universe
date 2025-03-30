async function get_publications(page=1) {
    console.log(window.location.pathname);
        
    await fetch(`../publication/list${window.location.pathname}?page=${page}`)
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

$(document).ready(function () {
    
    $("#id_button_close_form").click(function (e) { 
        e.preventDefault();
        $("#id_profile_modal_update").hide();
    });

    $("#id_profile_button_update").click(function (e) { 
        e.preventDefault();
        $("#id_profile_modal_update").show();
    });
 
    get_publications();
});