var toInt,
    toFloat;

(function() {
    var _dispatch;
    _dispatch = function(fn, val, def) {
        if (!def) {
            def = '';
        }
        if (isNaN( val = fn(val) )) {
            return def;
        }
        return val;
    }

    toInt = function(val, def) {
        return _dispatch(parseInt, val, def);
    }
    toFloat = function(val, def) {
        return _dispatch(parseFloat, val, def);
    }
})();


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
            name: document.forms['get_biz']['name'].value,
            lat: toFloat(document.forms['get_biz']['lat'].value),
            lon: toFloat(document.forms['get_biz']['lon'].value)
        },
    }).done(success_res).fail(fail_res);
}


function post_biz() {
    $.ajax({
        type: 'POST',
        url: '/api/business',
        data: {
            name: document.forms['post_biz']['name'].value,
            lat: toFloat(document.forms['post_biz']['lat'].value),
            lon: toFloat(document.forms['post_biz']['lon'].value)
        },
    }).done(success_res).fail(fail_res);
}


function get_bizid() {
    $.ajax({
        type: 'GET',
        url: '/api/business/' + document.forms['get_bizid']['id'].value
    }).done(success_res).fail(fail_res);
}


function put_bizid() {
    $.ajax({
        type: 'PUT',
        url: '/api/business/' + document.forms['put_bizid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_bizid']['name'].value,
            lat: toFloat(document.forms['put_bizid']['lat'].value),
            lon: toFloat(document.forms['put_bizid']['lon'].value)
        })
    }).done(success_res).fail(fail_res);
}


function delete_bizid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/business/' + document.forms['delete_bizid']['id'].value
    }).done(success_res).fail(fail_res);
}


function get_coup() {
    $.ajax({
        type: 'GET',
        url: '/api/coupon',
        data: {
            user: parseInt(document.forms['get_coup']['user'].value),
            business: parseInt(document.forms['get_coup']['business'].value)
        }
    }).done(success_res).fail(fail_res);
}


function post_coup() {
    $.ajax({
        type: 'POST',
        url: '/api/coupon',
        data: {
            name: document.forms['post_coup']['name'].value,
            business: parseInt(document.forms['post_coup']['business'].value)
        }
    }).done(success_res).fail(fail_res);
}


function get_coupid() {
    $.ajax({
        type: 'GET',
        url: '/api/coupon/' + document.forms['get_coupid']['id'].value
    }).done(success_res).fail(fail_res);
}


function put_coupid() {
    $.ajax({
        type: 'PUT',
        url: '/api/coupon/' + document.forms['put_coupid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_coupid']['name'].value,
            business: parseInt(document.forms['put_coupid']['business'].value)
        })
    }).done(success_res).fail(fail_res);
}


function delete_coupid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/coupon/' + document.forms['delete_coupid']['id'].value
    }).done(success_res).fail(fail_res);
}


function get_user() {
    $.ajax({
        type: 'GET',
        url: '/api/user'
    }).done(success_res).fail(fail_res);
}

function post_user() {
    $.ajax({
        type: 'POST',
        url: '/api/user',
        data: {
            name: document.forms['post_user']['name'].value
        }
    }).done(success_res).fail(fail_res);
}


function get_userid() {
    $.ajax({
        type: 'GET',
        url: '/api/user/' + document.forms['get_userid']['id'].value
    }).done(success_res).fail(fail_res);
}


function post_userid() {
    $.ajax({
        type: 'POST',
        url: '/api/user/' + document.forms['post_userid']['id'].value,
        data: {
            coupon: parseInt(document.forms['post_userid']['coupon'].value)
        }
    }).done(success_res).fail(fail_res);
}


function put_userid() {
    $.ajax({
        type: 'PUT',
        url: '/api/user/' + document.forms['put_userid']['id'].value,
        processData: false,
        contentType: 'text/json',
        data: JSON.stringify({
            name: document.forms['put_userid']['name'].value
        })
    }).done(success_res).fail(fail_res);
}


function delete_userid() {
    $.ajax({
        type: 'DELETE',
        url: '/api/user/' + document.forms['delete_userid']['id'].value
    }).done(success_res).fail(fail_res);
}


$(document).ready(function() {
    document.getElementById('clear').addEventListener('click', function() {
        document.getElementById('status').innerHTML = '';
        document.getElementById('msg').innerHTML = '';
    }, false)
});
