function success_res(data, textStatus, xhr) {
    document.getElementById('status').innerHTML = textStatus;
    document.getElementById('msg').innerHTML = data;
}

function fail_res(xhr, textStatus, errorThrown) {
    var msg,
        i,
        table,
        row,
        cell;

    table = document.createElement('table');
    for ( i in xhr ) {
        row = document.createElement('tr');

        cell = document.createElement('td');
        cell.innerHTML = i;
        row.appendChild(cell);

        cell = document.createElement('td');
        cell.innerHTML = xhr[i];
        row.appendChild(cell);

        table.appendChild(row);
    }
    document.getElementById('status').innerHTML = errorThrown;
    msg = document.getElementById('msg');
    msg.innerHTML = '';
    msg.appendChild(table);
}

function get_biz() {
    $.ajax({
        type: 'GET',
        url: '/api/business',
        data: {
            name: document.forms[0]['name'].value,
            lat: document.forms[0]['lat'].value,
            lon: document.forms[0]['lon'].value,
        },
    }).done(success_res).fail(fail_res);
}

function post_biz() {
    $.ajax({
        type: 'POST',
        url: '/api/business',
        data: {
            name: document.forms[1]['name'].value,
            lat: document.forms[1]['lat'].value,
            lon: document.forms[1]['lon'].value
        },
    }).done(success_res).fail(fail_res);
}

function get_bizid() {
    $.ajax({
        type: 'GET',
        url: '/api/business/' + document.forms[2]['id'].value
    }).done(success_res).fail(fail_res);
}

function put_bizid() {
    $.ajax({
        type: 'PUT',
        url: '/api/business/' + document.forms[3]['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms[3]['naem'].value,
            lat: document.forms[3]['lat'].value,
            lon: document.forms[3]['lon'].value
        })
    }).done(success_res).fail(fail_res);
}

function delete_bizid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/business/' + document.forms[4]['id'].value
    }).done(success_res).fail(fail_res);
}
