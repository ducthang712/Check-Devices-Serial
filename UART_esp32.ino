#define WATER_DEVICE_CHECK        "aaa-water"
#define WATER_DEVICE_CODE         "seri:aaa-water"
#define WATER_DEVICE_NAME         "name:banana"
#define WATER_DEVICE_TYPE         "type:U01"
#define WATER_DEVICE_DEVID        "deid:U2024"
#define WATER_DEVICE_UUID         "uuid:2U3U4U"
#define WATER_DEVICE_SECRET       "secr:4secret4"
#define WATER_DEVICE_DEVEUI       "deui:22222222"
#define WATER_DEVICE_DESCRIPTION  "stat:THIS IS WATER DEVICE"

void setup() {
  // Initialize Serial communication at 115200 baud rate
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for the serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte
    String incomingMessage = Serial.readStringUntil('\n');
    incomingMessage.trim(); // Remove any extra whitespace
    //check incoming data
    if (incomingMessage == "hello") {
      Serial.println("world");
    }
    else if (incomingMessage == "HI ESP") {
      Serial.println("HI PYTHON");
    }
    else if (incomingMessage == "hi") {
      Serial.println("five");
    }


    // else if (incomingMessage == WATER_DEVICE_CHECK) {
    //   Serial.println(String(WATER_DEVICE_CODE) + "||"
    //                 + String(WATER_DEVICE_NAME) + "||"
    //                 + String(WATER_DEVICE_DEVID) + "||"
    //                 + String(WATER_DEVICE_SECRET) + "||"
    //                 + String(WATER_DEVICE_TYPE) + "||" 
    //                 + String(WATER_DEVICE_UUID) + "||"
    //                 + String(WATER_DEVICE_DESCRIPTION));
    //                 }

    else if (incomingMessage == WATER_DEVICE_CHECK) {
      Serial.println("accepted");
    }
    
    else if (incomingMessage == "name") {
      Serial.println(WATER_DEVICE_NAME);
    }

    else if (incomingMessage == "deid") {
      Serial.println(WATER_DEVICE_DEVID);
    }
    else if (incomingMessage == "type") {
      Serial.println(WATER_DEVICE_TYPE);
    }
    else if (incomingMessage == "stat") {
      Serial.println(WATER_DEVICE_DESCRIPTION);
    }
    
    else {
      Serial.println("???");
    }
  }
}
