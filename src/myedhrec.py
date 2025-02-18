from pyedhrec import EDHRec
from unidecode import unidecode
class MyEDHREc(EDHRec):
	def __init__(self):
		super().__init__()
		self._json_page_cards_url = 'https://json.edhrec.com/pages/cards/'

	def get_similar_cards(self, cards_name: str):
		data = self.get_json(cards_name)
		return data['similar']
	def get_json(self, cards_name: str):
		formatted_card_name = format_card_name(cards_name)
		url = f'{self._json_page_cards_url}{formatted_card_name}.json'
		data = self._get(url)
		return data


def format_card_name(card_name: str) -> str:
	card_name =  card_name.lower()
	card_name = card_name.replace(' // ', '-')
	card_name = card_name.replace(" ", "-")
	# remove apostrophes
	card_name = card_name.replace("'", "")
	# remove commas
	card_name = card_name.replace(",", "")

	# encode removing accent, ae, oe, ue, ':' ect for url compatibility
	card_name = card_name.replace(":", "")
	card_name = card_name.replace("!", "")
	card_name = card_name.replace("?", "")
	card_name = unidecode(card_name)


	return card_name


