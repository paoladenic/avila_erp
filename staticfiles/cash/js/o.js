// document.addEventListener('DOMContentLoaded', function () {
//     // Obtener referencias a los inputs
//     var inputs = document.querySelectorAll('input[type="text"]');
//     var totalInput = document.getElementById('total');

//     // Manejar el evento de cambio para cada input
//     inputs.forEach(function (input) {
//         input.addEventListener('change', function () {
//             // Calcular el total
//             var total = 0;
//             inputs.forEach(function (input) {
//                 var valorInput = parseFloat(input.value) || 0;
//                 var placeholder = input.getAttribute('placeholder');
//                 var valorMoneda = 0;
//                 // Verificar si el placeholder es numérico
//                 if (!isNaN(placeholder)) {
//                     // Convertir el placeholder a un valor numérico para la moneda
//                     valorMoneda = parseFloat(placeholder);
//                 } else if (placeholder.includes('c')) {
//                     valorMoneda = parseFloat(placeholder.replace(/[^\d.-]/g, '')) * 0.01; // Convertir centavos a euros
//                 } else {
//                     valorMoneda = parseFloat(placeholder.replace(/[^\d.-]/g, '')); // Euros
//                 }
//                 console.log("Valor Input:", valorInput);
//                 console.log("Valor Moneda:", valorMoneda);
//                 total += valorInput * valorMoneda;
//             });

//             // Actualizar el input de "Total"
//             console.log("Total:", total);
//             totalInput.value = total.toFixed(2);
//         });
//     });
// });

