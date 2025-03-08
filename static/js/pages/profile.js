async function get_posts(page=1) {
    profile = $('#id_profile').val();
    await fetch(`../post/list/profile?page=${page}&profile=${profile}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $('#id_posts').append(data);
    })
    .finally(() => {

        let posts = $('.post').get();

        posts.forEach(post => {
            post_id = post.getAttribute('post-id');
            aux_posts = $(`.post[post-id=${post_id}]`);
            if (aux_posts.length > 1) {
                aux_posts[1].remove();
            }
        });

    })
}

$(document).ready(function () {
    
    $("#id_btn_close_form").click(function (e) { 
        e.preventDefault();
        $("#id_modal_profile_update").hide();
    });
    $("#id_btn_update_profile").click(function (e) { 
        e.preventDefault();
        $("#id_modal_profile_update").show();
    });
    
 
    get_posts();
});