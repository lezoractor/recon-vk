# recon-vk

Программа для сбора и анализа публичной информации социальной сети Вконтакте.
[Work in progress]

## Алгоритмы

### Поиск скрытых друзей
- Получаем все публично доступные данные нужной страницы
- Вытягиваем из них связи с любыми другими страницами или группами
- Проверяем каждую полученную страницу, нет ли у нее в друзьях нужной страницы
- ???
- PROFIT!

### Реальное местоположение человека
Наибольшая точность, если друзей от 80 до 400
- Находим все геометки с данной страницы и страниц друзей
- Группируем метки по времени и месту (т.е. две фотографии в одном месте и в один день станут одной записью)
- Находим скопление меток и показываем на карте

### Определение групп людей и их смысла
- Строим граф одной страницы
- Догружаем тех, на кого ссылается больше N страниц
- Определяем группы лиц
- Находим общие черты (общая группа, географическое положение, музыка, информация о странице)
- Выводим список групп, называем их наболее выделяющейся общей чертой
- В качестве подробной информации - список общих черт

### Вторая страница человека
- Запрашиваем доп. инфу (предполагаемое имя или фамилия, предполагаемый год рождения)
- Составляем полный социальный граф страницы (т.е. в том числе и группы, аудио и т.п.)
- Добавляем тех, на кого ссылается больше N страниц или групп
- Находим того (тех), у кого социальный граф больше похож на данный
- Если найдено много, то используем доп. инфу. для фильтрации
- ????
- PROFIT!

## Всякие идеи 
- Сделать выделение (лассо) на графе, выбирающее группу людей, и открывающее соответствующую информацию на панели информации. (Допустим, выделили группу людей, и можно посмотреть их общие характеристики)
- По-умолчанию на графе показываются только дружеские связи и страницы людей в качестве вершин, но можно расширить этот список.
