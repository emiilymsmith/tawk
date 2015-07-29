function modify_qty(val) {
    var qty = document.getElementById('qty').value;
    var new_qty = parseInt(qty,10) + val;


    document.getElementById('qty').value = new_qty;
    return new_qty;
}
