async function like_post(url, button) {
    await fetch(`${url}`)
    .then(response => {
        return response.text();
    })    
    .then(data => {
        button.innerHTML = data; 
    })
}

async function open_image(url) {
    await fetch(`${url}`)
    .then(response => {
        return response.blob();
    })    
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        $('#id_open_image').attr('src', imageUrl);
    })
    .finally(() => {
        $('#id_modal_image').show();
    })
}

$(document).ready(function () {
    
    $("#id_btn_close_image").click(function (e) { 
        e.preventDefault();
        $("#id_modal_image").hide();
    });

    $("#id_modal_image").click(function (e) { 
        e.preventDefault();
        $("#id_modal_image").hide();
    });
    
    $('#id_btn_search').click(function (e) { 
        e.preventDefault();
        $('#id_search_modal').show();
    });
    $('#id_btn_close_search').click(function (e) { 
        e.preventDefault();
        $('#id_search_modal').hide();
    });
    
    $('#id_btn_menu').click(function (e) { 
        e.preventDefault();
        $('#id_navbar_aside').show();
    });
    $('#id_btn_close_menu').click(function (e) { 
        e.preventDefault();
        $('#id_navbar_aside').hide();
    });

});

