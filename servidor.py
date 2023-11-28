from flask import Flask, render_template, jsonify, Response
import ast
import serial
#pip install cryptography
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

app = Flask(__name__)


def obtener_datos():
    try:
        # ser = serial.Serial('COM3', 9600)
        # line = ser.readline().decode('utf-8').strip()
        # data = line.split("/")
        # gas = data[0].split(",")[1]
        # calidad = data[1].split(",")[1].split("-")
        # data = {"gas":gas,
        #         "calidad":{
        #             calidad[0].split(":")[0] : calidad[0].split(":")[1],
        #             calidad[1].split(":")[0] : calidad[1].split(":")[1],
        #             calidad[2].split(":")[0] : calidad[2].split(":")[1]
        #         }
        #     }
        data = {
            "gas": 1,
            "calidad": {
                "H": 28.6,
                "T": 18.7,
                "I": 20
            }
        }

        # Convertir el JSON a un string
        json_str = json.dumps(data).encode('utf-8')

        # Clave y vector para la inicialización de AES
        key = b"mysecretpassword1"
        iv = b"mysecretpassword2"

        # Padding del mensaje
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(json_str) + padder.finalize()

        # Configuración del cifrado AES con una clave de 128 bits
        cipher = Cipher(algorithms.AES(key[:16]), modes.CBC(iv[:16]), backend=default_backend())

        # Creación del encriptador
        encryptor = cipher.encryptor()

        # Encriptación del mensaje
        ct = encryptor.update(padded_data) + encryptor.finalize()

        # Codificación en Base64 para transferencia
        encrypted_message = base64.b64encode(ct).decode('utf-8')
        yield 'data: {}\n\n'.format(encrypted_message)
    except Exception as e:
        print(f"Error al leer datos desde COM3: {e}")


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/datos')
def datos_gas():
    return Response(obtener_datos(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)

