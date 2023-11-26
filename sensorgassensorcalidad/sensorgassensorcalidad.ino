#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11

#define SENSOR_ANALOGICO_ID 1
#define SENSOR_DHT11_ID 2

DHT dht(DHTPIN, DHTTYPE);
const int sensorAnalogicoPin1 = A0;
int valorSensorAnalogico;
float humedad, temperatura, indiceCalor;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Leer valor del sensor analógico
  valorSensorAnalogico = analogRead(sensorAnalogicoPin1);
  
  // Imprimir valor del sensor analógico
  Serial.print(SENSOR_ANALOGICO_ID);
  Serial.print(",");
  Serial.print(valorSensorAnalogico);
  Serial.print("/");

  // Leer datos del sensor DHT11
  leerDatosDHT();

  // Esperar un tiempo antes de la próxima lectura
  delay(5000);
}

void leerDatosDHT() {
  // Leer la humedad relativa
  humedad = dht.readHumidity();
  // Leer la temperatura en grados centígrados (por defecto)
  temperatura = dht.readTemperature();
  // Leer la temperatura en grados Fahrenheit
  float temperaturaFahrenheit = dht.readTemperature(true);

  // Comprobar si ha habido algún error en la lectura
  if (isnan(humedad) || isnan(temperatura) || isnan(temperaturaFahrenheit)) {
    Serial.println("Error obteniendo los datos del sensor DHT11");
    return;
  }

  // Calcular el índice de calor en Fahrenheit
  float indiceCalorFahrenheit = dht.computeHeatIndex(temperaturaFahrenheit, humedad);
  // Calcular el índice de calor en grados centígrados
  indiceCalor = dht.computeHeatIndex(temperatura, humedad, false);

  // Imprimir los datos del sensor DHT11
  Serial.print(SENSOR_DHT11_ID);
  Serial.print(",");
  Serial.print("H:");
  Serial.print(humedad);
  Serial.print("-T:");
  Serial.print(temperatura);
  Serial.print("-I:");
  Serial.println(indiceCalor);
}
