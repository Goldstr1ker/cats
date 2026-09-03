"""
Программа: смотрит на лицо через веб-камеру, определяет эмоцию
и показывает рядом картинку котика с такой же эмоцией.

Управление: клавиша 'q' в окне с видео — выход.
"""
import time

import cv2
import numpy as np
from fer import FER

IMAGE_PATHS = {
    "angry": "cats/angry.jfif",
    "happy": "cats/happy.jfif",
    "sad": "cats/sad.jfif",
    "surprise": "cats/surprise.jfif",
    "neutral": "cats/neutral.jfif",
}

# Раз в столько секунд пересчитываем эмоцию (не каждый кадр, чтобы не грузить CPU)
CHECK_INTERVAL = 0.5


def load_cat_images(size):
    images = {}
    for emotion, path in IMAGE_PATHS.items():
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(
                f"Не найдена картинка для эмоции '{emotion}': {path}\n"
                f"Запусти make_placeholders.py, чтобы создать заглушки, "
                f"или положи свою картинку по этому пути."
            )
        images[emotion] = cv2.resize(img, size)
    return images


def main():
    detector = FER(mtcnn=False)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть камеру")

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Не удалось получить кадр с камеры")

    h, w = frame.shape[:2]
    cat_images = load_cat_images((w, h))

    current_emotion = "neutral"
    last_check = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        if now - last_check > CHECK_INTERVAL:
            last_check = now
            result = detector.detect_emotions(frame)
            if result:
                emotions = result[0]["emotions"]
                current_emotion = max(emotions, key=emotions.get)

        cat_img = cat_images.get(current_emotion, cat_images["neutral"])
        combined = np.hstack((frame, cat_img))

        cv2.putText(
            combined, current_emotion, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
        )

        cv2.imshow("Твоё лицо и котик", combined)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
