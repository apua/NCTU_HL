(function () {
    var order_tag = Array.prototype.filter.call(
        document.getElementsByTagName('select'),
        function (elem) {
            return elem.id.slice(0, 8) == 'id_order';
        });

    var sumup = function () {
        var count_tag = document.getElementsByClassName('count');
        var total = 0;
        for (var a = 0; a < count_tag.length; a++) {
            total += parseInt(count_tag[a].value);
        }
        //document.getElementById('total').value = total;
        document.getElementById('display-total').innerHTML = total;
    };

    var update = function (i) {
        var new_amount = parseInt(order_tag[i].value);
        var price = parseInt(document.getElementById('price' + i).value);
        document.getElementById('count' + i).value = new_amount * price;
        document.getElementById('display-count' + i).innerHTML = new_amount * price;
        sumup();
    };

    for (var a = 0; a < order_tag.length; a++) {
        order_tag[a].onchange = function () {
            var change_id = this.parentNode.id.slice(6);
            update(change_id);
            document.getElementById('order-success').className = 'order-dirty';
            document.getElementById('display-count' + change_id).className = 'order-item-dirty';
            document.getElementById('display-total').className = 'order-item-dirty';
        };
        update(a);
    }
})();
