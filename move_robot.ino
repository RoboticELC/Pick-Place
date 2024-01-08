// SERVO SETTING
#include <Servo.h>
Servo kanan; Servo base; Servo gripper;
// 6 angles
int pos_base = 0, pos_kanan = 90, pos_grip = 120;
int open_grip = 120, close_grip = 70, drag_down = 170, drag_up = 90, home = 0;

void setup() {
  base.attach(3); kanan.attach(6); gripper.attach(9);
  calibrate();
}

void loop() {
  move(45);
  move(90);
  move(135);
}

void calibrate() {
  base.write(pos_base); kanan.write(pos_kanan); gripper.write(pos_grip);
}

void Servo_Move(int a, int b, char c, char d){
  if (d == 'i'){//increase
    for (int pos = a; pos <= b; pos += 1) {
      if (c == 'B'){
        base.write(pos);
      }else if (c == 'K'){
        kanan.write(pos);
      }else if (c == 'G'){
        gripper.write(pos);
      }
      delay(15);
    }
  }
  else if (d == 'd'){//decrease
    for (int pos = a; pos >= b; pos -= 1) {
      if (c =='B'){
        base.write(pos);
      }else if (c == 'K'){
        kanan.write(pos);
      }else if (c == 'G'){
        gripper.write(pos);
      }
      delay(15);
    }
  }
}

// decrease --> getobject (120 to 70), drag (170 to 90), back home (x to 0)
// increase --> release object (70 to 120), reach (90 to 170), place (0 to x)

/* PSEUDOCODE Servo Movement
1. Reach object 
2. Pinch object 
3. Delay(3000)
4. Drag object 
5. Place to X 
6. Reach object 
7. Release object 
8. Drag Link 
9. Place to Home 
*/

//int open_grip = 120, close_grip = 70, drag_down = 170, drag_up = 90, home = 0;
void move(int x){
  Servo_Move(drag_up, drag_down, 'K', 'i'); //reach
  Servo_Move(open_grip, close_grip, 'G', 'd');
  Servo_Move(drag_down, drag_up, 'K', 'd'); //drag
  Servo_Move(home, x, 'B', 'i');
  Servo_Move(drag_up, drag_down, 'K', 'i'); //reach
  Servo_Move(close_grip, open_grip, 'G', 'i');
  Servo_Move(drag_down, drag_up, 'K', 'd'); //drag
  Servo_Move(x, home, 'B', 'd');
}