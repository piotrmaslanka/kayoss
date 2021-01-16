function update(data) {
    for (var key in data)
        if (data.hasOwnProperty(key)) {
			var truth = data[key] ? true : false;
            $('#mk'+key).html(data[key]);
            $('#mb'+key).css('display', (truth) ? 'block' : 'none');			
            $('#mscr'+key).css('background-color', (truth) ? 'red' : 'green');			
        }
}