async function like_publication(url, button) {
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
        $('#id_image_modal').show();
    })
}

$(document).ready(function () {
    // search-aside
    $('#id_button_search').click(function (e) { 
        e.preventDefault();
        $('#id_search_modal').show();
    });
    $('#id_button_back_search').click(function (e) { 
        e.preventDefault();
        $('#id_search_modal').hide();
    });

    // menu
    $('#id_button_menu').click(function (e) { 
        e.preventDefault();
        $('#id_navbar_modal').show();
    });
    $('#id_button_back_navbar').click(function (e) { 
        e.preventDefault();
        $('#id_navbar_modal').hide();
    });

    // chat 
    $('#id_button_chat').click(function (e) { 
        e.preventDefault();
        $('#id_chat_modal').show();
    });
    $('#id_button_back_chat').click(function (e) { 
        e.preventDefault();
        $('#id_chat_modal').hide();
    });


    // image-modal
    $("#id_image_modal").click(function (e) { 
        e.preventDefault();
        $("#id_image_modal").hide();
    });
        
    setTimeout(() => {
        $('.messages').fadeOut(2000);
    }, "8000")

});

