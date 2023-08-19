#include "esp_camera.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"

#define CAMERA_MODEL_XIAO_ESP32S3

#include "camera_pins.h"

uint32_t image_count = 0; 
uint pos;
byte header[15];

uint32_t insertUint32(byte buffer[], uint32_t position, uint32_t value)
{
    // position++ increments position after using it as an index
    // if you were to use ++position, the position would be incremented first and then use that incremented value as the index
    buffer[position++] = byte(value >> 24 & 0xff);
    buffer[position++] = byte(value >> 16 & 0xff);
    buffer[position++] = byte(value >> 8 & 0xff);
    buffer[position++] = byte(value & 0xff);
    return position;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // allow led to blink
  Serial.begin(115200);
  while(!Serial) {
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    digitalWrite(LED_BUILTIN, HIGH);
  }

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_CIF;
  config.pixel_format = PIXFORMAT_RGB565;
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // camera init
  esp_err_t err = esp_camera_init(&config);

    sensor_t * s = esp_camera_sensor_get();
  s->set_brightness(s, 0);     // -2 to 2
  s->set_contrast(s, 0);       // -2 to 2
  s->set_saturation(s, 0);     // -2 to 2
  s->set_special_effect(s, 0); // 0 to 6 (0 - No Effect, 1 - Negative, 2 - Grayscale, 3 - Red Tint, 4 - Green Tint, 5 - Blue Tint, 6 - Sepia)
  s->set_whitebal(s, 1);       // 0 = disable , 1 = enable
  s->set_awb_gain(s, 1);       // 0 = disable , 1 = enable
  s->set_wb_mode(s, 0);        // 0 to 4 - if awb_gain enabled (0 - Auto, 1 - Sunny, 2 - Cloudy, 3 - Office, 4 - Home)
  s->set_exposure_ctrl(s, 0);  // 0 = disable , 1 = enable
  s->set_aec2(s, 0);           // 0 = disable , 1 = enable
  s->set_ae_level(s, 0);       // -2 to 2
  s->set_aec_value(s, 10);    // 0 to 1200
  s->set_gain_ctrl(s, 1);      // 0 = disable , 1 = enable
  s->set_agc_gain(s, 0);       // 0 to 30
  s->set_gainceiling(s, (gainceiling_t)0);  // 0 to 6
  s->set_bpc(s, 0);            // 0 = disable , 1 = enable
  s->set_wpc(s, 1);            // 0 = disable , 1 = enable
  s->set_raw_gma(s, 1);        // 0 = disable , 1 = enable
  s->set_lenc(s, 1);           // 0 = disable , 1 = enable
  s->set_hmirror(s, 0);        // 0 = disable , 1 = enable
  s->set_vflip(s, 1);          // 0 = disable , 1 = enable
  s->set_dcw(s, 1);            // 0 = disable , 1 = enable
  s->set_colorbar(s, 0);       // 0 = disable , 1 = enable
}

void loop() {
  // get to a message
  if (Serial.available() >= 12) {
    if (Serial.read() == 0b11111111) { // first byte of sync: "1" byte
      if (Serial.read() == 0b00000000) { // second byte of sync: "0" byte
        digitalWrite(LED_BUILTIN, LOW);
        switch (char(Serial.read())) { // first byte of header: char8_t "type"
          case 'u':
            break;
          case 'e':
            break;
          case 'r': // is this a request image message?
            switch (Serial.read()) { // second byte of header: uint8_t "version"
              case 0: // is this message of the 0th version?
                image_count++;

                digitalWrite(LED_BUILTIN, LOW);

                camera_fb_t *fb = esp_camera_fb_get();

                digitalWrite(LED_BUILTIN, HIGH);

                header[0] = 0b11111111;
                header[1] = 0b00000000;
                header[2] = 0b01101001;
                header[3] = 0b00000000;
                pos = 4;
                pos = insertUint32(header, pos, image_count);
                pos = insertUint32(header, pos, fb->len + 3);
                header[12] = 0b01100011;
                header[13] = 0b01000011;
                header[14] = 0b01001001;
                Serial.write(header,15);

                Serial.write(fb->buf,fb->len);

                esp_camera_fb_return(fb);
                break;
            }
            break;
          case 'i':
            break;
        }
        digitalWrite(LED_BUILTIN, HIGH);
      }
    }
  }

}
