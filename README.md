# Main Element

Main Element - это онлайн/оффлайн стратегия в 2D, написанная на Pygame.

### В новой версии (checkpoint 3):
1. Улучшенное поведение ботов.
2. Многочисленные исправления онлайна привели к его стабильности.
3. Появились условия выигрыша и проигрыша.
4. Добавлены новые структуры.
5. Добавлена фоновая музыка.
6. Баланс начисления ресурсов и войск.
7. Добавлена возможность обратной связи через гугл формы.

### Запуск
Запустите `main_element.exe` в папке c исходным кодом.\
Внимание: нельзя изменять/перемещать файлы игры в папке `data`.\
Для загрузки сохранения нажмите `Загрузить` и выберите сейв.

### Настройка онлайн-режима (для хоста)
1. Нажмите `Новая игра` и выберите режим онлайн.
2. В поле `кол-во игроков` введите кол-во игроков (от 2 до 4).
3. В поле `порт` введите желаемый порт.
4. Нажмите enter и ожидайте подключения других игроков.
Если кол-во игроков будет меньше 4, оставшиеся места будут заполнены нашими замечательными ботами.
P.S. из сохранения ботов нельзя будет убрать

### Настройка онлайн-режима (для клиента)
1. Нажмите `Онлайн`.
2. Введите ipv4-адрес хоста и порт.
3. Нажмите enter. (если выкинуло в главное меню, значит Вы ввели неправильный адрес/порт).

### Запуск оффлайн-режима
1. Нажмите `Новая игра`/`Загрузить`. В случае, если нажали `Загрузить`, выберите файл с сохранением.
2. Назовите сохранение.
3. Нажмите `Локально`.

## Интерфейс игрового окна
Нижняя строка - для отображения сообщений (о постройке структуры/атаке и т.д.)
Верхняя панель - кол-во ресурсов, кнопка перемещения к своей центральной структуре.

### Постройка структур
Постройки можно ставить только на своих клетках и только в определенных биомах (окрашены в цвет вашей фракции).
1. Нажмите ПКМ.
2. В открывшемся окне выберите структуру для постройки и нажмите `проектировать`.

### Перемещение войск
Изначально все войска находятся в центральной клетке.\
Для перемещения войск нажмите на клетку старта и протяните курсор до другой клетки. С помощью появившегося ползунка выберите кол-во войск. Если в целевой клетке будут находиться войска противника, то она будет захвачена, при условии, что кол-во атакующих войск будет превышать кол-во обороняющихся. Учтите, что любая структура дает прибавку к обороне, т.е. разница между атакой и обороной будет увеличена.

### Геймплей
Вам предложено управлять небольшим поселением людей одной из фракций, участвующих в борьбе за господство своего природного элемента на одной старинной карте какого-то участка земли где-то в средневековой Европе.

Цель - уничтожить центральные структуры противников, символизирующие одну из четырех природных стихий.

Для захвата территории необходимо переместить свое войско в чужую или нейтральную клетку (зажать ЛКМ на клетке с войском и переместить курсор в соседнюю клетку, затем выставить кол-во людей для операции). Чтобы посмотреть, кому принадлежат клетки, нажмите на переключатель в верхнем правом углу.

На своих территориях можно строить структуры. Каждая из них дает определенное кол-во ресурсов (отображается в правом верхнем углу), войск и имеет уровень защиты (минимальное кол-во людей, которое нужно противнику для захвата клетки с данной структурой, в добавок к численности ваших войск, расположенных здесь).

Игра продолжается до тех пор, пока существует ваша центральная структура и пока вы не захватили всех противников.