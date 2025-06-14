import cv2
import time
from morse import morse_to_text  # your existing decoder

def detect_flash_morse(threshold=180):
    cap = cv2.VideoCapture(0)
    morse_sequence = ''
    is_flashing = False
    flash_start = 0

    print("Watching for Morse flashes (Press 'q' to stop)...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = gray.mean()
            current_time = time.time()

            if brightness > threshold:
                if not is_flashing:
                    flash_start = current_time
                    is_flashing = True
            else:
                if is_flashing:
                    flash_duration = current_time - flash_start
                    if flash_duration < 0.3:
                        morse_sequence += '.'
                        print('.', end='', flush=True)
                    else:
                        morse_sequence += '-'
                        print('-', end='', flush=True)
                    is_flashing = False

            cv2.imshow("Flash Decoder", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    print("\nMorse Code:", morse_sequence)
    print("Decoded Message:", morse_to_text(morse_sequence))


if __name__ == "__main__":
    detect_flash_morse()
