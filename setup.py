import setuptools

mayor = 0
minor = 1
fix = 0

with open("README.md", 'r') as f:
    long_description = f.read()
    f.close()

with open('requirements.txt') as f:
    required = f.read().splitlines()
    f.close()

setuptools.setup(
    name="TU-telegram_bot",
    version=f"{mayor}.{minor}.{fix}",
    author="Juan Brugera Monedero",
    author_email="ed3n35@gmail.com",
    description="Telegram bot that automatically send messages to the group from a product link",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JuanBrugera/TU-telegram-bot",
    packages=setuptools.find_packages(),
    data_files=[
        ('.', ['requirements.txt', 'application-template.conf'])
    ],
    install_requires=required
)
