# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


def trim_value(value):
    if isinstance(value, list):
        # Nếu giá trị là một mảng, trim từng phần tử trong mảng
        output_array = []
        for item in value:
            splitted_items = item.split('.')
            output_array.extend(splitted_items)
        output_array = [trim_value(item) for item in output_array]
        while '' in output_array:
            output_array.remove('')
        return output_array
    elif isinstance(value, str):
        # Nếu giá trị là một chuỗi, trim chuỗi
        return value.strip()
    else:
        # Trường hợp còn lại (bao gồm giá trị là None), không làm gì
        return value


def trim_object(obj):
    trimmed_obj = {}
    for key, value in obj.items():
        trimmed_value = trim_value(value)
        trimmed_obj[key] = trimmed_value
    return trimmed_obj


class TimViec365Pipeline:
    def process_item(self, item, spider):
        return trim_object(item)
