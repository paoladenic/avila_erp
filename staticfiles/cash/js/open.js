document.addEventListener('DOMContentLoaded', function () {
    // Obtener referencias a los inputs
    var inputs = document.querySelectorAll('input[type="text"]');
    var totalInput = document.getElementById('total');

    // Manejar el evento de cambio para cada input
    inputs.forEach(function (input) {
        input.addEventListener('change', function () {
            // Calcular el total
            var total = 0;
            inputs.forEach(function (input) {
                var valorInput = parseFloat(input.value) || 0;
                var placeholder = input.getAttribute('placeholder');
                var valorMoneda = !isNaN(parseFloat(placeholder)) ? parseFloat(placeholder) : 0;
                if (placeholder.includes('c')) {
                    valorMoneda *= 0.01; // Convertir centavos a euros
                }
                console.log("Valor Input:", valorInput);
                console.log("Valor Moneda:", valorMoneda);
                total += valorInput * valorMoneda;
            });
            // Actualizar el input de "Total"
            console.log("Total:", total);
            totalInput.value = total.toFixed(2);
            document.getElementById('total-input').value = total.toFixed(2); // Actualizar el campo hidden
        });
    });
});
