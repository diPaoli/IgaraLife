function filtrar() {
    tx = document.getElementById('tx_ap').value;
    if (tx.length > 0) {
        //alert("/lista/ap/" + tx);
        location.href = "/lista/ap/" + tx;
    } else
        return null;
}

function limpar() {
    location.href = "/lista";
}