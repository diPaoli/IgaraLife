document.addEventListener("DOMContentLoaded", function() {
    var elements = document.getElementsByTagName("INPUT");
    for (var i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function(e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                switch (e.target.id) {
                    case "i_ap": e.target.setCustomValidity("Registre o QRCode do Apartamento."); break;
                    case "i_gas": e.target.setCustomValidity("Digite a leitura de gás.\nApenas números."); break;
                    case "i_agua": e.target.setCustomValidity("Digite a leitura da água.\nApenas números.");
                }
            }
        };
        elements[i].oninput = function(e) {
            e.target.setCustomValidity("");
        };
    }
})