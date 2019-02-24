const view_post_modal_content = document.getElementById('view-post-modal-content');

function view_post(post_id) {
    const request = new XMLHttpRequest();
    request.open("GET", '/post?post_id=' + post_id);
    request.send();
    request.onreadystatechange = (e) => {
        view_post_modal_content.innerHTML = request.responseText;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('.modal');
    const m = M.Modal.init(modals, {});

    document.querySelectorAll('.collection-item').forEach((item) => {
        item.addEventListener('click', () => {
            view_post(item.id.split('view-post-')[1])
        });
    });

    const url = new URL(window.location.href);
    if (url.searchParams.get('post_id')) {
        view_post(url.searchParams.get('post_id'));
        m.forEach((modal) => {
            if (modal['el'] === document.getElementById('view-post-modal')) {
                modal.open();
            }
        });
    }
});
