"""
Генерирует временные картинки-заглушки для папки cats/.
Запусти один раз, чтобы проверить, что программа работает,
а потом замени файлы в cats/ на свои настоящие картинки котиков
(имена файлов должны остаться теми же).
"""
from PIL import Image, ImageDraw, ImageFont

EMOTIONS = {
    "sad": ((80, 120, 200), "Грустный"),
    "happy": ((80, 200, 120), "Весёлый"),
    "angry": ((200, 80, 80), "Злой"),
    "surprise": ((220, 200, 80), "Удивлённый"),
    "neutral": ((150, 150, 150), "Нейтральный"),
}

SIZE = (400, 400)


def main():
    for name, (color, label) in EMOTIONS.items():
        img = Image.new("RGB", SIZE, color)
        draw = ImageDraw.Draw(img)

        # Простая "мордочка" кота, чтобы было видно разницу между заглушками
        draw.ellipse((100, 120, 300, 320), fill=(255, 255, 255))
        draw.polygon([(100, 160), (60, 60), (150, 130)], fill=(255, 255, 255))
        draw.polygon([(300, 160), (340, 60), (250, 130)], fill=(255, 255, 255))
        draw.ellipse((150, 190, 175, 215), fill=(0, 0, 0))
        draw.ellipse((225, 190, 250, 215), fill=(0, 0, 0))

        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((SIZE[0] - text_w) / 2, 340), label, fill=(0, 0, 0), font=font)

        path = f"cats/{name}.png"
        img.save(path)
        print(f"Сохранено: {path}")


if __name__ == "__main__":
    main()
