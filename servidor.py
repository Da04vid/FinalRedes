from flask import Flask, render_template, jsonify, Response
import ast
import serial

app = Flask(__name__)


def obtener_datos():
    try:
        ser = serial.Serial('COM3', 9600)
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
        yield 'data: {}\n\n'.format(data)
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

