void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // allow led to blink
  Serial.begin(115200);
  while(!Serial) {
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    digitalWrite(LED_BUILTIN, HIGH);
  }
}

void loop() {
  byte message[] = {
    0b00000000, 0b11111111, 0b01110101, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00010010,
    0b01101000, 0b01100101, 0b01101100, 0b01101100, 0b01101111, 0b00101100,
    0b00100000, 0b01110111, 0b01101111, 0b01110010, 0b01101100, 0b01100100,
    0b00100001, 0b00100000, 0b11110000, 0b10011111, 0b10011000, 0b10000011
  };

  Serial.write(message,sizeof(message));

  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
}
