from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Parameter:
    name: str
    part: str
    parameter: str
    value: int
    year: str
    category: str = ""


# class Aggregate:

# def group_by_year():


# class Part:
#     name: str
#     part: str


# @dataclass
# class Aggregation:
#     years: list
#     parts: list
#     parameters: list


# статья
# часть
# параметр
# значение
# год

# статья состоит из частей
# номера частей неуникальны
# параметры варьируются год от года
# части можно складывать (т.е. значения соответствующих параметров друг с другом, но некоторые параметры при сложении дают неопределенное значение)
