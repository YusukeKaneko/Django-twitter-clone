$(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.like').on('click', function (event) {
        event.preventDefault();
        const url = $(this).attr('data-url');
        const csrftoken = getCookie('csrftoken');
        const selector = $(this)
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            type: 'POST',
            url: url,
            dataType: 'json',
            success: function (response) {
                selector.children('span').text(response.likes_count);
                if (response.liked) {
                    selector.attr('data-url', 'http://127.0.0.1:8000/unlike/num/'.replace(/num/, response.post_pk));
                    selector.children('i').attr('class', 'fas fa-thumbs-up')
                } else {
                    selector.attr('data-url', 'http://127.0.0.1:8000/like/num/'.replace(/num/, response.post_pk));
                    selector.children('i').attr('class', 'far fa-thumbs-up')
                }
            }
        });
    });
});
