import requests


class CurrencyConverter:
    def __init__(self):
        self.usd_rate = self._fetch_usd_rate()

    def _fetch_usd_rate(self):
        """Отримує актуальний курс USD з офіційного API НБУ"""
        url = "https://bank.gov.ua"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list):
                # API повертає список, беремо перший елемент та дістаємо поле 'rate'
                return float(data[0]['rate'])
            else:
                raise ValueError("Неправильна структура даних від API")

        except Exception as e:
            print(f"Помилка отримання курсу з сайту НБУ: {e}")
            print("Використовується резервний курс (45.00 грн/USD)")
            return 45.00  # Резервний курс на випадок збою мережі

    def convert_uah_to_usd(self, amount_uah):
        """Конвертує гривні (UAH) в долари США (USD)"""
        if amount_uah < 0:
            raise ValueError("Сума не може бути від'ємною")
        return amount_uah / self.usd_rate


def main():
    print("Отримання актуального курсу валют з сайту НБУ...")
    converter = CurrencyConverter()
    print(f"Поточний офіційний курс: 1 USD = {converter.usd_rate:.4f} UAH\n")

    try:
        user_input = input("Введіть суму в гривнях (UAH) для конвертації: ")
        # Замінюємо кому на крапку, якщо користувач ввів дробове число через кому
        amount_uah = float(user_input.replace(',', '.'))

        amount_usd = converter.convert_uah_to_usd(amount_uah)
        print(f"Результат конвертації: {amount_uah:.2f} UAH = {amount_usd:.2f} USD")

    except ValueError as e:
        if "Сума не може бути від'ємною" in str(e):
            print("Помилка: введено від'ємне число.")
        else:
            print("Помилка: будь ласка, введіть коректне числове значення.")


if __name__ == "__main__":
    main()


