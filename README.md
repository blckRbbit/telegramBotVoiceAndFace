1. Откройте терминал в директории, где расположена папка с проектом. Введите команду: *python3 -m venv <имя виртуального окружения>*;

2. Активируйте виртуальное окружение: *source <имя окружения>/bin/activate*;

3. Установите пакеты зависимостей командой: *pip install -r requirements.txt* (если у вас не установлен менеджер пакетов pip, введите команду *sudo apt install python3-pip*);

4. 
	- В телеграме напишите боту по имени **BotFather** команду */newbot*; 
	- Введите **ИМЯ** бота (*именно имя, не никнейм*);
	- Введите **НИКНЕЙМ** бота, который обязательно должен заканчиваться на bot;
	- BotFather пришлет Вам токен и ссылку на Вашего бота;

5. Откройте файл **config.py** и в строке TOKEN, в кавычки вставьте Ваш токен, в строке NAME - имя бота, в строке USERNAME - никнейм бота;

6. Перейдите в директорию **bot** и в терминале пропишите *python3 bot.py*;

Бот сохраняет голосовые сообщения, конвертируя их в формат wav и фотографии, на которых присутствует лицо, ход выполнения документируется в логах, в терминале.