import config
import dlib
import logger
import os
import pydub
import requests
import telebot

from skimage import io

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['voice'])
def save_audio_messages(message):
    """Сохраняет голосовое сообщение на диск, конвертируя его в wav"""
    try:
        file_info = bot.get_file(message.voice.file_id)
        logger.log.info(f"Передан голосовой файл: {file_info}")
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path))
        logger.log.info(f"Ответ сервера: {file}")
        folder_name = f"{message.from_user.id}_{message.from_user.username}"
        if folder_name not in os.listdir(config.upload_folder):
            logger.log.info(f"Создаю папку для нового пользователя: {folder_name}")
            os.mkdir(os.path.join(config.upload_folder, folder_name))
        logger.log.info(f"Пользователь {folder_name} уже использовал бота")
        file_name = str(message.message_id)
        path = f"{folder_name}/{file_name}.ogg"
        path_to_message = os.path.join(config.upload_folder, path)
        logger.log.info(f"в обработку принят файл в формате '.ogg', путь: {path_to_message}")
        with open(path_to_message, 'wb') as sent_message:
            logger.log.info(f"файл {path_to_message} успешно записан на диск")
            sent_message.write(file.content)
        sound = pydub.AudioSegment.from_ogg(f"{path_to_message}")
        wav_pass = path_to_message.rsplit('.', 1)[0] + ".wav"
        sound.export(f"{wav_pass}", format="wav")
        os.remove(path_to_message)
        logger.log.info(f"Конвертация {wav_pass} прошла успешно")
        bot.reply_to(message, f"Пожалуй, я сохраню это.")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['photo'])
def save_photo_with_face(message):
    """Сохраняет фото, где есть лицо, на диск"""

    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        logger.log.info(f"Передано изображение: {file_info}")
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path))
        logger.log.info(f"Ответ сервера: {file}")
        folder_name = f"{message.from_user.id}_{message.from_user.username}"
        if folder_name not in os.listdir(config.upload_folder):
            os.mkdir(os.path.join(config.upload_folder, folder_name))
            logger.log.info(f"Создаю папку для нового пользователя: {folder_name}")
        logger.log.info(f"Пользователь {folder_name} уже использовал бота")
        file_name = file_info.file_path.rsplit('/', 1)[1]
        path = f"{folder_name}/{file_name}"
        path_to_image = os.path.join(config.upload_folder, path)
        logger.log.info(f"{path_to_image} обрабатывается")
        with open(path_to_image, 'wb') as sent_image:
            sent_image.write(file.content)
            logger.log.info(f"файл {path_to_image} успешно записан на диск")
        detector_1 = dlib.get_frontal_face_detector()
        detector_2 = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
        image = io.imread(path_to_image)
        dets_1 = detector_1(image, 1)
        dets_2 = detector_2(image, 1)
        if str(dets_2) == 'mmod_rectangles[]' and str(dets_1) == 'rectangles[]':
            os.remove(path_to_image)
            bot.reply_to(message, f"На этом снимке не видно лиц, не буду сохранять!")
            logger.log.info('Лицо на снимке не было определено')
        else:
            bot.reply_to(message, f"Пожалуй, я сохраню это. На этом снимке есть лицо!")
            logger.log.info('Лицо на снимке было успешно определено')
    except Exception as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
