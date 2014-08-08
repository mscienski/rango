/**
 * Created by idfl on 8/7/14.
 */

$(function() {
    $('#likes').click(function() {
        var $this = $(this);
        var catid;
        catid = $this.attr('data-catid');
        $.get('/rango/like_category/', {category_id: catid}, function(data) {
            $('#like_count').html(data);
            $this.hide();
        });
    });

    $('#suggestion').keyup(function(){
        var $this = $(this);
        var query;
        query = $this.val();
        $.get('/rango/suggest_category/',
            {suggestion: query},
            function(data) {
                $('#cats').html(data);
            });
    });

    $('.rango-add').click(function() {
        var $this = $(this);
        var catid = $this.attr('data-catid');
        var url = $this.attr('data-url');
        var title = $this.attr('data-title');
        $.get('/rango/auto_add_page/',
            {
                category_id: catid,
                url: url,
                title: title},
            function(data) {
                $('#pages').html(data);
                $this.hide();
            });
    })
});
