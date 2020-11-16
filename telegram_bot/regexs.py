import re

TU_PRODUCT_REGEX = re.compile(r'(https://www\.tu\.com/products/[0-9a-z-]+)(\?variant=\d+)?')
TU_PRODUCT_JSON_REGEX = re.compile(r'productJson:({.*}),};')
TU_PRODUCT_INFO_REGEX = re.compile(r'.*(bloque_info_producto grid).*')
TU_PRODUCT_DESCRIPTION_UPPERS = re.compile(r'\.[A-Z|ÁÉÍÓÚ]')
