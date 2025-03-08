async function get_posts(page=1) {
    post = $('#id_post').val();
    await fetch(`../post/list/comment?page=${page}&post=${post}`)
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
    get_posts();
});