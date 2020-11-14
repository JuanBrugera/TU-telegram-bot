import re

TU_PRODUCT_REGEX = re.compile(r'https://www\.tu\.com/products/(\w|-)*')
TU_PRODUCT_JSON_REGEX = re.compile(r'productJson:({.*}),};')
SI_NO_REGEX = re.compile(r'^(SI|NO)$')
