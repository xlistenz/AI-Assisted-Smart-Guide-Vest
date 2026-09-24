import time
import cv2
import numpy as np
import datetime
import os
from pathlib import Path
from picamera2 import Picamera2
from ultralytics import YOLO
import RPi.GPIO as GPIO

# ================= 設定區 =================
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    str(Path(__file__).resolve().parents[1] / "models" / "my_model.pt"),
)

# --- 系統按鈕腳位 ---
BTN_MASTER_PIN = 4      # G4: 系統開關
BTN_ACTION_PIN = 25     # G25: 導航開關

# --- 馬達與 LED ---
MOTOR_LEFT = 17
MOTOR_CENTER = 27
MOTOR_RIGHT = 22
PIN_RED_LIGHT = 23
PIN_GREEN_LIGHT = 24

# --- 語音模組 ---
PIN_VOICE_B3  = 12
PIN_VOICE_A27 = 26
PIN_VOICE_A26 = 19
PIN_VOICE_A25 = 13

# --- 參數設定 ---
# 使用 640x480 確保視野最廣 (Original Logic)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
INFERENCE_SIZE = 640 

# 導航中心區
ZONE_LEFT_LIMIT = 280   
ZONE_RIGHT_LIMIT = 360

# --- 信心度設定 ---
CONF_THRESHOLD = 0.25       
GREEN_LIGHT_CONF = 0.15     
CROSSWALK_CONF = 0.25       

IOU_THRESHOLD = 0.4     
MAX_DETECTIONS = 20     

VOICE_COOLDOWN = 2.5    
SMOOTH_ALPHA = 0.5      

# ==========================================

def turn_off_all_outputs():
    """ 關閉所有輸出 """
    pins = [MOTOR_LEFT, MOTOR_CENTER, MOTOR_RIGHT, 
            PIN_RED_LIGHT, PIN_GREEN_LIGHT, 
            PIN_VOICE_B3, PIN_VOICE_A27, PIN_VOICE_A26, PIN_VOICE_A25]
    GPIO.output(pins, GPIO.LOW)

def set_voice_pins(b3, a27, a26, a25):
    GPIO.output(PIN_VOICE_B3,  GPIO.HIGH if b3 else GPIO.LOW)
    GPIO.output(PIN_VOICE_A27, GPIO.HIGH if a27 else GPIO.LOW)
    GPIO.output(PIN_VOICE_A26, GPIO.HIGH if a26 else GPIO.LOW)
    GPIO.output(PIN_VOICE_A25, GPIO.HIGH if a25 else GPIO.LOW)

def play_voice_section(section):
    """ 觸發語音段落 """
    if section == 1: set_voice_pins(1, 0, 0, 1)   # 紅燈
    elif section == 2: set_voice_pins(1, 0, 1, 0) # 綠燈
    elif section == 3: set_voice_pins(1, 0, 1, 1) # 斑馬線
    elif section == 4: set_voice_pins(1, 1, 0, 0) # 偏右
    elif section == 5: set_voice_pins(1, 1, 0, 1) # 偏左
    elif section == 6: set_voice_pins(1, 1, 1, 0) # 等待
    
    # [新增] 按鈕語音功能
    elif section == 7: set_voice_pins(1, 1, 1, 1) # G4: 啟動程序
    elif section == 8: set_voice_pins(1, 0, 0, 0) # G25: 開始辨識

    time.sleep(0.15)
    set_voice_pins(0, 0, 0, 0)

def draw_motor_ui(frame, left_on, center_on, right_on):
    """ 繪製 UI """
    y_pos = 440 
    color_l = (0, 255, 255) if left_on else (50, 50, 50) 
    cv2.circle(frame, (60, y_pos), 25, color_l, -1)
    cv2.putText(frame, "L", (48, y_pos + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    color_c = (0, 255, 0) if center_on else (50, 50, 50)
    cv2.circle(frame, (320, y_pos), 25, color_c, -1)
    cv2.putText(frame, "C", (308, y_pos + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    color_r = (0, 255, 255) if right_on else (50, 50, 50)
    cv2.circle(frame, (580, y_pos), 25, color_r, -1)
    cv2.putText(frame, "R", (568, y_pos + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

def main():
    GPIO.setmode(GPIO.BCM)
    output_pins = [MOTOR_LEFT, MOTOR_CENTER, MOTOR_RIGHT, 
                   PIN_RED_LIGHT, PIN_GREEN_LIGHT, 
                   PIN_VOICE_B3, PIN_VOICE_A27, PIN_VOICE_A26, PIN_VOICE_A25]
    GPIO.setup(output_pins, GPIO.OUT)
    GPIO.output(output_pins, GPIO.LOW) 
    GPIO.setup(BTN_MASTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTN_ACTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print(f"載入模型 (Original Logic + Button Voice)...")
    try:
        model = YOLO(MODEL_PATH, task='detect')
    except Exception as e:
        print(f"錯誤：找不到模型 - {e}")
        return

    print("啟動相機 (640x480)...")
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"format": "XBGR8888", "size": (CAMERA_WIDTH, CAMERA_HEIGHT)})
        picam2.configure(config)
        picam2.start()
        try:
            picam2.set_controls({"AfMode": 2, "AfRange": 2})
        except:
            pass
    except Exception as e:
        print(f"相機失敗: {e}")
        GPIO.cleanup()
        return

    # 變數初始化
    system_ready = False
    nav_active = False
    last_btn_master = GPIO.HIGH
    last_btn_action = GPIO.HIGH
    smoothed_center_x = None     
    prev_time = 0
    last_nav_voice_time = 0
    
    traffic_state = "NONE" 
    last_voice_state = "NONE"
    red_light_start_time = 0
    has_played_red_voice = False
    has_played_red_wait = False
    has_played_no_light_voice = False

    print("系統就緒！")

    try:
        while True:
            # === G4 總開關 (不關機，只切換 Ready/Sleep) ===
            curr_btn_master = GPIO.input(BTN_MASTER_PIN)
            if last_btn_master == GPIO.HIGH and curr_btn_master == GPIO.LOW:
                system_ready = not system_ready
                if system_ready:
                    print("=== [G4] 系統啟動 ===")
                    # [新增] 播放語音：啟動程序
                    play_voice_section(7) 
                else:
                    print("=== [G4] 系統休眠 ===")
                    nav_active = False
                    turn_off_all_outputs()
                    smoothed_center_x = None
                    traffic_state = "NONE"
                time.sleep(0.3)
            last_btn_master = curr_btn_master

            if not system_ready:
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                continue

            # === G25 導航開關 ===
            curr_btn_action = GPIO.input(BTN_ACTION_PIN)
            if last_btn_action == GPIO.HIGH and curr_btn_action == GPIO.LOW:
                nav_active = not nav_active
                if nav_active:
                    print(">>> [G25] 導航開始 <<<")
                    # [新增] 播放語音：開始辨識
                    play_voice_section(8) 
                    
                    traffic_state = "NONE"
                    last_voice_state = "NONE"
                    red_light_start_time = 0
                    has_played_red_voice = False
                    has_played_red_wait = False
                    has_played_no_light_voice = False 
                    smoothed_center_x = None
                else:
                    print(">>> [G25] 導航暫停 <<<")
                    turn_off_all_outputs()
                    smoothed_center_x = None
                time.sleep(0.3)
            last_btn_action = curr_btn_action

            # === 影像處理 (維持原邏輯) ===
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time
            
            raw_frame = picam2.capture_array()
            frame = raw_frame[:, :, :3]
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            inference_frame = cv2.resize(frame, (INFERENCE_SIZE, INFERENCE_SIZE))

            results = model(inference_frame, 
                          imgsz=INFERENCE_SIZE, 
                          conf=GREEN_LIGHT_CONF, 
                          iou=IOU_THRESHOLD,
                          max_det=MAX_DETECTIONS,
                          verbose=False)

            instant_detect_green = False
            instant_detect_red = False
            
            nav_target_x = None 
            max_crosswalk_area = 0
            
            current_best_box_coords = None 
            current_best_box_conf = 0.0    
            light_center_coords = None
            light_color_code = (0, 0, 0)
            
            # --- 分析數據 ---
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    label_name = str(model.names[cls_id]).strip().casefold()
                    conf = box.conf[0]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    scale_y = CAMERA_HEIGHT / INFERENCE_SIZE
                    y1 = int(y1 * scale_y)
                    y2 = int(y2 * scale_y)
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    if label_name in {"cross road", "crosswalk", "zebra crossing", "斑馬線"}:
                        if conf > CROSSWALK_CONF:
                            area = (x2 - x1) * (y2 - y1)
                            if area > max_crosswalk_area:
                                max_crosswalk_area = area
                                nav_target_x = cx
                                current_best_box_coords = (x1, y1, x2, y2)
                                current_best_box_conf = conf

                    elif label_name in {"green light", "pedestrian green light", "行人綠燈"}:
                        if conf > GREEN_LIGHT_CONF:
                            instant_detect_green = True
                            light_center_coords = (cx, cy)
                            light_color_code = (0, 255, 0)

                    elif label_name in {"red light", "pedestrian red light", "行人紅燈"}:
                        if conf > CONF_THRESHOLD:
                            instant_detect_red = True
                            light_center_coords = (cx, cy)
                            light_color_code = (0, 0, 255)

            # --- 狀態鎖定 ---
            # Fail closed: do not keep showing an old signal after it disappears.
            if instant_detect_red:
                traffic_state = "RED"
            elif instant_detect_green:
                traffic_state = "GREEN"
            else:
                traffic_state = "NONE"

            # --- 全時計算並顯示中心點 (不論是否按下 G25) ---
            if nav_target_x is not None:
                if smoothed_center_x is None:
                    smoothed_center_x = nav_target_x
                else:
                    smoothed_center_x = smoothed_center_x * (1 - SMOOTH_ALPHA) + nav_target_x * SMOOTH_ALPHA
                
                cv2.circle(frame, (int(smoothed_center_x), CAMERA_HEIGHT//2), 10, (0, 255, 255), -1)
                cv2.putText(frame, "Target: Found", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                smoothed_center_x = None
                cv2.putText(frame, "Target: None", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
            
            # --- 繪圖 ---
            if current_best_box_coords:
                bx1, by1, bx2, by2 = current_best_box_coords
                cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 0, 255), 3)
                cv2.putText(frame, f"Cross {current_best_box_conf:.2f}", (bx1, by1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)

            if light_center_coords:
                cv2.circle(frame, light_center_coords, 10, light_color_code, 2)
                cv2.putText(frame, "LOCKED", (light_center_coords[0], light_center_coords[1]-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, light_color_code, 2)

            # ================= 導航邏輯 (僅在 nav_active 為 True 時觸發) =================
            status_light_text = f"State: {traffic_state}" 
            color_light_text = (100, 100, 100)
            
            is_motor_left_on = False
            is_motor_center_on = False
            is_motor_right_on = False

            if nav_active:
                # 語音
                if nav_target_x is not None:
                    if not has_played_no_light_voice:
                        play_voice_section(3) 
                        has_played_no_light_voice = True

                if last_voice_state == "RED" and traffic_state == "GREEN":
                    play_voice_section(2)
                
                if traffic_state == "RED":
                    if last_voice_state != "RED":
                        red_light_start_time = curr_time
                        has_played_red_voice = False
                        has_played_red_wait = False
                    
                    if not has_played_red_voice:
                        play_voice_section(1)
                        has_played_red_voice = True
                    
                    if has_played_red_voice and not has_played_red_wait:
                        if (curr_time - red_light_start_time) > 2.0:
                            play_voice_section(6)
                            has_played_red_wait = True
                
                last_voice_state = traffic_state

                # 輸出
                if traffic_state == "RED":
                    GPIO.output(PIN_RED_LIGHT, GPIO.HIGH)
                    GPIO.output(PIN_GREEN_LIGHT, GPIO.LOW)
                    status_light_text = "RED LIGHT"
                    color_light_text = (0, 0, 255)
                    is_motor_center_on = False 
                elif traffic_state == "GREEN":
                    GPIO.output(PIN_RED_LIGHT, GPIO.LOW)
                    GPIO.output(PIN_GREEN_LIGHT, GPIO.HIGH)
                    status_light_text = "GREEN LIGHT"
                    color_light_text = (0, 255, 0)
                    is_motor_center_on = True 
                else:
                    GPIO.output(PIN_RED_LIGHT, GPIO.LOW)
                    GPIO.output(PIN_GREEN_LIGHT, GPIO.LOW)
                    status_light_text = "Searching..."
                    color_light_text = (200, 200, 200)
                    is_motor_center_on = False

                # 導航馬達 (使用全時計算的 smoothed_center_x)
                if smoothed_center_x is not None:
                    can_speak_nav = (curr_time - last_nav_voice_time) > VOICE_COOLDOWN

                    if smoothed_center_x < ZONE_LEFT_LIMIT:
                        is_motor_left_on = True
                        is_motor_center_on = False 
                        if can_speak_nav:
                            play_voice_section(4) 
                            last_nav_voice_time = curr_time
                    elif smoothed_center_x > ZONE_RIGHT_LIMIT:
                        is_motor_right_on = True
                        is_motor_center_on = False
                        if can_speak_nav:
                            play_voice_section(5) 
                            last_nav_voice_time = curr_time
                    else:
                        if traffic_state != "RED":
                            is_motor_center_on = True
                else:
                    is_motor_left_on = False
                    is_motor_right_on = False
                    is_motor_center_on = False

                GPIO.output(MOTOR_CENTER, GPIO.HIGH if is_motor_center_on else GPIO.LOW)
                GPIO.output(MOTOR_LEFT, GPIO.HIGH if is_motor_left_on else GPIO.LOW)
                GPIO.output(MOTOR_RIGHT, GPIO.HIGH if is_motor_right_on else GPIO.LOW)
                
            # === UI ===
            cv2.line(frame, (ZONE_LEFT_LIMIT, 0), (ZONE_LEFT_LIMIT, CAMERA_HEIGHT), (255, 255, 0), 2)
            cv2.line(frame, (ZONE_RIGHT_LIMIT, 0), (ZONE_RIGHT_LIMIT, CAMERA_HEIGHT), (255, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, status_light_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_light_text, 2)
            
            if nav_active:
                draw_motor_ui(frame, is_motor_left_on, is_motor_center_on, is_motor_right_on)

            cv2.imshow("Smart Guide (Final + Voice)", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"執行錯誤: {e}")

    finally:
        turn_off_all_outputs()
        GPIO.cleanup()
        try:
            picam2.stop()
        except:
            pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
