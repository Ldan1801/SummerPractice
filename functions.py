import cv2 as cv
import numpy as np


def load_image(file_path: str) -> np.ndarray:
    """
    Загрузка изображения с указанного пути.
    :param file_path: путь к файлу изображения
    :return: изображение в формате numpy array
    """
    img = cv.imread(file_path)
    if img is None:
        raise ValueError("Не удалось загрузить изображение")
    return img


def make_photo_from_video_capture() -> None:
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', frame)
        k = cv.waitKey(1)
        if k == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break
        if k == ord('s'):
            print('saving image')
            cv.imwrite("saving image.png", frame)
            cap.release()
            cv.destroyAllWindows()
            break


def show_image(image: np.ndarray) -> None:
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def show_images_сhannel(image: np.ndarray, chanell: str) -> None:
    blue_channel, green_channel, red_channel = cv.split(image)
    if chanell == 'blue':
        cv.imshow('blue', blue_channel)
    if chanell == 'green':
        cv.imshow('green', green_channel)
    if chanell == 'red':
        cv.imshow('red', red_channel)
    cv.waitKey(0)
    cv.destroyAllWindows()


def show_negative_image(image: np.ndarray) -> None:
    negative_image = 255 - image

    cv.imshow('Negative Image', negative_image)

    cv.waitKey(0)
    cv.destroyAllWindows()


def draw_circle(image: np.ndarray, center: tuple, radius: int) -> None:
    cv.circle(image, center, radius, (0, 0, 255), -1)


def rotate_image(image: np.ndarray, angle) -> None:
    # Получение размеров изображения
    (h, w) = image.shape[:2]

    # Определение центра изображения
    center = (w // 2, h // 2)

    # Вычисление синуса и косинуса угла
    cos = np.abs(np.cos(np.radians(angle)))
    sin = np.abs(np.sin(np.radians(angle)))

    # Вычисление новых размеров холста
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Создание матрицы поворота с учетом нового размера
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Выполнение поворота с новыми размерами
    rotated = cv.warpAffine(image, M, (new_w, new_h))

    return rotated


