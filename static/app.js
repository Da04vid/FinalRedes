document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('lineChart').getContext('2d');
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Datos Sensor de Gas',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: [{
                    type: 'linear',
                    position: 'bottom'
                }],
                y: [{
                    type: 'linear',
                    position: 'left'
                }]
            }
        }
    });

    // Maneja eventos de Server-Sent Events
    var eventoSource = new EventSource('/datos');
    eventoSource.onmessage = function (event) {
        //aqui desencriptar
        //npm install crypto-js
        const CryptoJS = require('crypto-js');
        var datos = event.data;
        const key = 'mysecretpassword1';
        const iv = 'mysecretpassword2';

        // Decodificación desde Base64
        const ct = Buffer.from(datos, 'base64');

        // Configuración para desencriptar usando AES
        const decrypted = CryptoJS.AES.decrypt(
            { ciphertext: CryptoJS.enc.Hex.parse(ct.toString('hex')) },
                CryptoJS.enc.Utf8.parse(key),
            { iv: CryptoJS.enc.Utf8.parse(iv) }
        );

        // Convertir de string a JSON
        const decryptedJson = JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
        var datos2 = decryptedJson.replace(/'/g, '"')
        var datosjson = JSON.parse(datos2)
        actualizarGrafica(lineChart, datosjson.gas);
        actualizarHumedad(datosjson.calidad.H);
        actualizarTemperatura(datosjson.calidad.T);
        actualizarIndicador(datosjson.calidad.I);
    };

    // Función para actualizar la gráfica y la tabla
    function actualizarGrafica(chart, datos) {
        var tiempo = new Date().toLocaleTimeString();
        chart.data.labels.push(tiempo);
        chart.data.datasets[0].data.push(parseFloat(datos));

        // Asegúrate de limitar la cantidad de datos según sea necesario
        if (chart.data.labels.length > 15) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        // Actualiza la gráfica
        chart.update();

        // Actualiza la tabla
        actualizarTabla(tiempo, datos);
    }

    // Inicializa el número de fila
    var numeroDeFila = 1;

    // Función para agregar una nueva fila a la tabla y mantener un máximo de 15 filas
    function actualizarTabla(tiempo, dato) {
        var cuerpoTabla = document.getElementById('cuerpoTabla');
        var tablaContenedor = document.getElementById('tablaContenedor');

        var nuevaFila = document.createElement('tr');

        // Crea las celdas para la nueva fila
        var celdaNumero = document.createElement('td');
        celdaNumero.textContent = numeroDeFila++;

        var celdaTiempo = document.createElement('td');
        celdaTiempo.textContent = tiempo;

        var celdaDato = document.createElement('td');
        celdaDato.textContent = dato;

        // Agrega las celdas a la fila
        nuevaFila.appendChild(celdaNumero);
        nuevaFila.appendChild(celdaTiempo);
        nuevaFila.appendChild(celdaDato);

        // Agrega la nueva fila al cuerpo de la tabla
        cuerpoTabla.appendChild(nuevaFila);

        // Desplázate hacia abajo para mostrar las filas más recientes
        tablaContenedor.scrollTop = tablaContenedor.scrollHeight;
    }




    function actualizarHumedad(dato) {
        document.getElementById('Humedad').textContent = 'Humedad: ' + dato;
    }
    function actualizarTemperatura(dato) {
        document.getElementById('Temperatura').textContent = 'Temperatura: ' + dato;
    }
    function actualizarIndicador(dato) {
        document.getElementById('Indicador').textContent = 'Indicador: ' + dato;
    }
});
