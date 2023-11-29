from flask import Flask, render_template, jsonify, Response
import serial
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import secrets
import os
import json

app = Flask(__name__)

def encrypt_rsa(data):
    key = RSA.generate(2048)

    # Obtener la clave pública
    public_key = key.publickey().export_key()
    # Crear un cifrador con la clave pública
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_data = cipher.encrypt(json.dumps(data).encode('utf-8'))
    return encrypted_data

def datos():
    ser = serial.Serial('COM5', 9600)
    line = ser.readline().decode('utf-8').strip()
    data = line.split("/")
    gas = data[0].split(",")[1]
    calidad = data[1].split(",")[1].split("-")
    data = {"gas":gas,
            "calidad":{
                calidad[0].split(":")[0] : calidad[0].split(":")[1],
                calidad[1].split(":")[0] : calidad[1].split(":")[1],
                calidad[2].split(":")[0] : calidad[2].split(":")[1]
            }
        }
    ser.close()
    return data

def obtener_datos(encrypt=False):
    try:
        while True:
            data = datos()
            if encrypt:
                data = encrypt_rsa(data)
            yield f'data: {data}\n\n'
    except Exception as e:
        print(f"Error al leer datos desde COM3: {e}")

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/datos')
def datos_gas():
    return Response(obtener_datos(), content_type='text/event-stream')

@app.route('/datosEncrypt')
def datos_encrypt():
    return Response(obtener_datos(encrypt=True), content_type='text/event-stream')

@app.route('/encrypt')
def dashboard():
    return render_template('encrypt.html')

if __name__ == '__main__':
    app.run(debug=True)

