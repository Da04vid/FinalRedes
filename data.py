SENSOR_ANALOGICO_ID = 1
SENSOR_DHT11_ID = 2

import serial

ser = serial.Serial('COM3', 9600)  # Ajusta el puerto COM según tu configuración

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        sensor_id, data = line.split(",")
        print(sensor_id)
        sensor_id = int(sensor_id)

        if sensor_id == SENSOR_ANALOGICO_ID:
            print(f"Datos del Sensor Analógico (A0): {data}")
        elif sensor_id == SENSOR_DHT11_ID:
            print(f"Datos del Sensor DHT11: {data}")
        else:
            print("Identificador de sensor desconocido")

    except ValueError as ve:
        print(f"Error al procesar la línea: {ve}")
    except IndexError as ie:
        print(f"Error de índice al procesar la línea: {ie}")