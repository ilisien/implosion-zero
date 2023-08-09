void setup() {
  Serial.begin(115200); // init serial port with a baudrate of 115200
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  byte a_byte = 97; // "a" in ascii
  byte b_byte = 98; // "b" in ascii

  Serial.write(a_byte); // write "a" byte to the serial port
  Serial.write(b_byte); // write "b" byte to the serial port
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500); // wait a second before looping again
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}