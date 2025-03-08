async function get_posts(page=1) {
    text = $('#id_search_text').val();
    category = $('#id_category_input').val();
    await fetch(`../post/list/search?page=${page}&text=${text}&category=${category}`)
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

async function get_profiles(page=1) {
    text = $('#id_search_text').val();
    await fetch(`../profile/list/search?page=${page}&text=${text}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        $("#id_btn_get_profiles").remove();
        $('#id_profiles').append(data);
    })
}


$(document).ready(function () {
    get_posts();
    get_profiles();
});