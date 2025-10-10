from develop_fun.log_fun import get_logger
from src.file_to_py_format import file_to_py_format
from src.find import process_search_bank, process_bank_operations
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date


def main():
    logger = get_logger()
    # пустое значение заготовка
    format_file = None
    status_filter = None

    # приветствие
    print('Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n'
            'Выберите необходимый пункт меню:\n')
    # цикл для получения формата файла(бесконечный пока не получит правильный ответ)
    while True:
        try:
            file_formats ={
                1:'json',
                2:'csv',
                3:'xlsx'
            }
            format_file = int(input(
            '1. Получить информацию о транзакциях из JSON-файла\n'
            '2. Получить информацию о транзакциях из CSV-файла\n'
            '3. Получить информацию о транзакциях из XLSX-файла\n'
            'Ввод: ').replace(" ",""))
            if not isinstance(format_file,int) or format_file not in [1,2,3]:
                print('\n\n\nВведите вариант ответа в формате:\nЧисло 1 , 2 или 3\nБез лишних символов\n\n')
            elif format_file in [1,2,3]:
                format_file = file_formats[format_file]
                print(f"\n\n\nФормат файла {format_file}\n\n\n")
                file_in_py_format = file_to_py_format(file_format=format_file)

                # print(f"Прочитано транзакций: {len(file_in_py_format)}")
                logger.info(f"Прочитано транзакций: {len(file_in_py_format)}")

                # # отладка
                # if file_in_py_format:
                #     print("Первая транзакция:", file_in_py_format[0])
                #     print("Статусы в файле:", set(t.get('state') for t in file_in_py_format))


                break
        except Exception as e:
            print('\n\n\nВведите вариант ответа в формате:\nЧисло 1 , 2 , 3 \nБез лишних символов и  букв\n\n')
            logger.error(f'Ошибка при вводе формата :\n{e}')
        # Выбор статуса фильтрации
    while True:
        print('Введите статус, по которому необходимо выполнить фильтрацию.\n'
              'Доступные для фильтровки статусы:\n'
              'EXECUTED, CANCELED, PENDING.')
        if format_file == 'xlsx':
            status_filter = 'executed'
            print('Для xlsx формата только статус:executed')
        else:
            status_filter = (input("Поле ввода статуса:   ").lower())
        if status_filter in ['executed', 'canceled', 'pending']:
            print(f'Операции отфильтрованы по статусу | {status_filter} |')
            filter_file = filter_by_state(transactions=file_in_py_format,state= status_filter)
            logger.info(f'Операции отфильтрованы по статусу | {status_filter} |')
            break
        else:
            print(f'\n\n\nСтатус операции |{status_filter}| недоступен.')

    # фильтровать по дате?
    while True:
        ans_sort_by_date = (input('Отсортировать операции по дате? Да/Нет\nВвод: ').lower())
        ans_to_sort_min_max = input('Фильтровать по возрастанию?\n(по умолчанию:сортировка по убыванию)\nВвод:')
        if ans_sort_by_date in ['да', 'нет'] and ans_to_sort_min_max in ['да', 'нет'] :
            if ans_sort_by_date == 'да':
                if ans_to_sort_min_max == 'нет':
                    filter_file = sort_by_date(transactions=filter_file, reverse=False)
                else:
                    # по умолчанию по убыванию
                    filter_file = sort_by_date(transactions=filter_file)
                print("Файл отфильтрован по дате")
                logger.info("Файл отфильтрован по дате")
                if ans_to_sort_min_max == 'да':
                    print('Отсортировано по убыванию')
                    logger.info('Отсортировано по убыванию')
                elif ans_to_sort_min_max == 'нет':
                    print('Отсортировано по возрастанию')
                    logger.info('Отсортировано по возрастанию')
                break
            else:
                break
        else:
            print('Ответ некоректный\n ')


    # Выводить только рублевые транзакции?
    while True:
        ans_sort_only_RUB = (input('Выводить только рублевые транзакции?\n(ответ да\нет)\nВвод: ').lower())
        if ans_sort_only_RUB in ['да','нет']:
            if ans_sort_only_RUB == 'да':
                filter_file = list(filter_by_currency(filter_file,currency_name='RUB'))
                print('Выведены только рублёвые транзакции')
                logger.info('Выведены только рублёвые транзакции')
                break
            elif ans_sort_only_RUB == 'нет':
                print('Выведены транзакции для всех валют')
                logger.info('Выведены транзакции для всех валют')
                break
            else:
                print('Ответ некоректный\n ')

    # Отфильтровать список транзакций по определенному слову в описании? Да/Нет
    while True:
        filt_to_word = (input('Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nВвод:').lower())
        if filt_to_word in ['да','нет']:
            if filt_to_word == 'да':
                input_word = input('Введите слово для фильтрации:').lower()
                filter_file = process_search_bank(filter_file,search=input_word)
                print(f'Список отсортирован по {input_word}')
                logger.info(f'Список отсортирован по {input_word}')
                break
            else:
                break
        else:
            print("Некоректный ввод")
    # нужно ли отфильтровать по категориям?
    while True:
        category_list = ['Супермаркеты', 'Фастфуд', 'Дом и ремонт', 'Каршеринг', 'Переводы',
                         'Аптеки', 'Связь', 'Такси', 'Транспорт',
                         'Местный транспорт', 'Различные товары',
                         'Одежда и обувь', 'Электроника и техника',
                         'Канцтовары', 'Ж/д билеты', 'Топливо',
                         'Развлечения', 'Рестораны', 'Цветы', 'Косметика',
                         'Детские товары', 'Сервис', 'Медицина',
                         'Госуслуги', 'Фото и видео', 'Сувениры',
                         'Онлайн-кинотеатры', 'НКО', 'Образование',
                         'Пополнения', 'Бонусы', 'Другое', 'Услуги банка',
                         'ЖКХ', 'Наличные', 'Мобильная связь',
                         'Частные услуги', 'Авиабилеты']
        category_filters = (input('Фильровать по категориям?\nда/нет\nВвод:').lower())
        if category_filters in ['да',"нет"]:
            if category_filters == 'да':
                while True:
                    print_all_category = input('Вывести список всех категорий?(да/нет)\nВвод: ').lower()
                    if print_all_category in ['да', 'нет']:
                        if print_all_category == 'да':
                            print(category_list)
                            break
                        elif print_all_category == 'нет':
                            break
                    else:
                        print('Некоректный ввод')
                cat_words_to_filt = input('Введите слова для фильтрации через пробел\nВвод').lower().split()


                count_filt_cat = (process_bank_operations(filter_file,cat_words_to_filt))
                logger.info(f'Фильтрация по категориям: {cat_words_to_filt}')
                break
            elif category_filters == 'нет':
                count_filt_cat = len(filter_file)
                logger.info('Фильтрация по категориям отключена')
                break
        else:
            print('Некорректный ввод\n')


    #Распечатываю итоговый список транзакций
    print('Распечатываю итоговый список транзакций...')
    logger.info('Распечатываю итоговый список транзакций...')
    if isinstance(count_filt_cat,dict):
        for operation,count in count_filt_cat.items():
            print(f'Всего банковских операций в подборке {operation} - {count}')
            logger.info(f'Всего банковских операций в подборке {operation} - {count}')
    # значит просто число (пользователь нажал 'нет')
    else:
        print(f'Всего банковских операций в подборке {count_filt_cat}')
        logger.info(f'Всего банковских операций в подборке {count_filt_cat}')
    if not filter_file:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')
        logger.info('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')
    elif filter_file:
        for transaction in filter_file:
            print(f'{transaction}\n')
        logger.info(f'Выведено транзакций: {len(filter_file)}')



if __name__ == '__main__':
    main()