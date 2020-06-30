$().ready(function() {
    var $options = $('select#id_pages option');
    $options.hide();

    $('#id_issue').on('change', function (e) {
        var issue = $("#id_issue option:selected").html();
        $options.show();
        $options.filter(function() { return $(this).text().indexOf(issue + ' - ') !== 0; }).hide();
    });
});
