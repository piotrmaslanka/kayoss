function update(data) {
    for (var key in data)
        if (data.hasOwnProperty(key)) {
            $('#mk'+key).html(data[key]);
            $('#mb'+key).css('display', (data[key]) ? 'block' : 'none');
        }
}