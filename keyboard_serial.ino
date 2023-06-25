#include <Mouse.h>
#include <Keyboard.h>
String cmd = "";
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  cmd = "";
  char temp = -1;
  while (Serial.available()) {
    temp = Serial.read();
    cmd.concat(temp);
  }
 
  if (cmd != "") {
    String m = cmd.substring(0, 1);
 
    if (m == "X") {
      int p = cmd.substring(1).toInt();
      Mouse.move(p, 0);
    }
    else if (m == "Y") {
      int p = cmd.substring(1).toInt();
      Mouse.move(0, p);
    }
    else if (m == "V" || m == "H") {
      int p = cmd.substring(1).toInt();
      Mouse.move(0, 0, p);
    }
    else if (m == "K") {
      String c = cmd.substring(0, 2);
      String v = cmd.substring(2);
      if (v == "LS") {
        keyAction(c, KEY_LEFT_SHIFT);
      }
      else if (v == "RS") {
        keyAction(c, KEY_RIGHT_SHIFT);
      }
      else if (v == "LC") {
        keyAction(c, KEY_LEFT_CTRL);
      }
      else if (v == "RC") {
        keyAction(c, KEY_RIGHT_CTRL);
      }
      else if (v == "LA") {
        keyAction(c, KEY_LEFT_ALT);
      }
      else if (v == "RA") {
        keyAction(c, KEY_RIGHT_ALT);
      }
      else if (v == "LW") {
        keyAction(c, KEY_LEFT_GUI);
      }
      else if (v == "RW") {
        keyAction(c, KEY_RIGHT_GUI);
      }
      else if (v == "AL") {
        keyAction(c, KEY_LEFT_ARROW);
      }
      else if (v == "AU") {
        keyAction(c, KEY_UP_ARROW);
      }
      else if (v == "AR") {
        keyAction(c, KEY_RIGHT_ARROW);
      }
      else if (v == "AD") {
        keyAction(c, KEY_DOWN_ARROW);
      }
      else if (v == "BS") {
        keyAction(c, KEY_BACKSPACE);
      }
      else if (v == "SB") {
        keyAction(c, ' ');
      }
      else if (v == "TB") {
        keyAction(c, KEY_TAB);
      }
      else if (v == "ET") {
        keyAction(c, KEY_RETURN);
      }
      else if (v == "EC") {
        keyAction(c, KEY_ESC);
      }
      else if (v == "IT") {
        keyAction(c, KEY_INSERT);
      }
      else if (v == "DT") {
        keyAction(c, KEY_DELETE);
      }
      else if (v == "PU") {
        keyAction(c, KEY_PAGE_UP);
      }
      else if (v == "PD") {
        keyAction(c, KEY_PAGE_DOWN);
      }
      else if (v == "HM") {
        keyAction(c, KEY_HOME);
      }
      else if (v == "ED") {
        keyAction(c, KEY_END);
      }
      else if (v == "CL") {
        keyAction(c, KEY_CAPS_LOCK);
      }
      else if (v == "F1") {
        keyAction(c, KEY_F1);
      }
      else if (v == "F2") {
        keyAction(c, KEY_F2);
      }
      else if (v == "F3") {
        keyAction(c, KEY_F3);
      }
      else if (v == "F4") {
        keyAction(c, KEY_F4);
      }
      else if (v == "F5") {
        keyAction(c, KEY_F5);
      }
      else if (v == "F6") {
        keyAction(c, KEY_F6);
      }
      else if (v == "F7") {
        keyAction(c, KEY_F7);
      }
      else if (v == "F8") {
        keyAction(c, KEY_F8);
      }
      else if (v == "F9") {
        keyAction(c, KEY_F9);
      }
      else if (v == "F10") {
        keyAction(c, KEY_F10);
      }
      else if (v == "F11") {
        keyAction(c, KEY_F11);
      }
      else if (v == "F12") {
        keyAction(c, KEY_F12);
      }
      else if (v == "N0") {
        keyAction(c, 234);
      }
      else if (v == "N1") {
        keyAction(c, 225);
      }
      else if (v == "N2") {
        keyAction(c, 226);
      }
      else if (v == "N3") {
        keyAction(c, 227);
      }
      else if (v == "N4") {
        keyAction(c, 228);
      }
      else if (v == "N5") {
        keyAction(c, 229);
      }
      else if (v == "N6") {
        keyAction(c, 230);
      }
      else if (v == "N7") {
        keyAction(c, 231);
      }
      else if (v == "N8") {
        keyAction(c, 232);
      }
      else if (v == "N9") {
        keyAction(c, 234);
      }
      else if (v == "N10") {
        keyAction(c, 221);
      }
      else if (v == "N11") {
        keyAction(c, 224);
      }
      else if (v == "N12") {
        keyAction(c, 222);
      }
      else if (v == "N13") {
        keyAction(c, 235);
      }
      else if (v == "N14") {
        keyAction(c, 223);
      }
      else if (v == "N15") {
        keyAction(c, 220);
      }
      else {
        if (c == "KD") {
          Keyboard.press(v[0]);
        }
        else if (c == "KU") {
          Keyboard.release(v[0]);
        }
      }
    }
    else {
      int c = cmd.toInt();
      switch (c) {
        case -1:
        Mouse.release();
        Keyboard.releaseAll();
        break;
        case 0:
          Mouse.click(MOUSE_LEFT);
          break;
        case 1:
          Mouse.press(MOUSE_LEFT);
          break;
        case 2:
          Mouse.release(MOUSE_LEFT);
          break;
        case 3:
          Mouse.click(MOUSE_LEFT);
          Mouse.click(MOUSE_LEFT);
          break;
        case 4:
          Mouse.click(MOUSE_RIGHT);
          break;
        case 5:
          Mouse.press(MOUSE_RIGHT);
          break;
        case 6:
          Mouse.release(MOUSE_RIGHT);
          break;
        case 7:
          Mouse.click(MOUSE_RIGHT);
          Mouse.click(MOUSE_RIGHT);
          break;
        case 8:
          Mouse.click(MOUSE_MIDDLE);
          break;
        case 9:
          Mouse.press(MOUSE_MIDDLE);
          break;
        case 10:
          Mouse.release(MOUSE_MIDDLE);
          break;
      }
    }
  }
}
 
void keyAction(String c, uint8_t k) {
  if (c == "KD") {
    Keyboard.press(k);
  }
  else if (c == "KU") {
    Keyboard.release(k);
  }
}
