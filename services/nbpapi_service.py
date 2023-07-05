import requests


class CurrencyExchange:
    def __init__(self, currency):
        self.currency = currency
        self.url = f"https://api.nbp.pl/api/exchangerates/rates/a/{self.currency}/?format=json"
        self.output = None

    def get_currency(self):
        if self.currency == "PLN":
            self.output = 1.0
            return self.output

        res = requests.get(self.url)
        if res.status_code == 200:
            data = res.json()
            rates = data.get('rates', [])
            if rates:
                self.output = rates[0].get('mid')
                return self.output

        return None
