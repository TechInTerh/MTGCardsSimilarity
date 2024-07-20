from pyedhrec import EDHRec


class MyEDHREc(EDHRec):
	def __init__(self):
		super().__init__()
		self._json_page_cards_url = 'https://json.edhrec.com/pages/cards/'

	def get_similar_cards(self, cards_name: str):
		formatted_card_name = format_card_name(cards_name)
		url = f'{self._json_page_cards_url}{formatted_card_name}.json'
		data = self._get(url)
		return data['similar']


def format_card_name(card_name: str) -> str:
	card_name = card_name.replace(' // ', '-')
	return EDHRec.format_card_name(card_name)
