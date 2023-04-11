$ (document).ready(function(){
    $('#shorten-url-button').click(function() {
        var longUrl = $('#long-url-input').val();
        $.ajax({
            url: 'http://127.0.0.1:5000/shorten_url',
            type: 'POST',
            data: {url,longUrl},
            success: function(data){
                $('#short-url').html(data.shortUrl);
            }
        });
    });
});
