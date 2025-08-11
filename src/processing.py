def filter_by_state(transcription: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
       Фильтрует список словарей, оставляя только те, где значение ключа 'state' совпадает с заданным.

    :param transactions: Список словарей для фильтрации.
    :param state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').
    :return: Отфильтрованный список словарей.
    """
    return [
        transcription
        for transcription in transcription
        if transcription.get("state") == state
    ]


def sort_by_date(transcription_no_sort: list[dict], reverse: bool = True) -> list[dict]:
    """в словаре ищет ключ 'date' и по нему сортирует в соответствии со значением 'reverse', давая на выход отсортированный по дате словарь"""
    return sorted(transcription_no_sort, key=lambda x: x["date"], reverse=reverse)
