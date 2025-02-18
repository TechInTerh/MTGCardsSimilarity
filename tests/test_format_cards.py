from unittest import TestCase
from src.myedhrec import format_card_name

class TestFormatCardsName(TestCase):
	def test_double_dot(self):
		name = "Rune of Protection: Artifacts"
		expected = "rune-of-protection-artifacts"
		got = format_card_name(name)
		self.assertEqual(expected, got)
	def test_double_slash(self):
		name = "Dusk // Dawn"
		expected = "dusk-dawn"
		got = format_card_name(name)
		self.assertEqual(expected, got)
	def test_exclamation(self):
		name = "Kaboom!"
		expected = "kaboom"
		got = format_card_name(name)
		self.assertEqual(expected, got)
	def test_encoding_unicde_u_accent(self):
		name = "Lim-Dûl's Hex"
		expected = "lim-duls-hex"
		got = format_card_name(name)
		self.assertEqual(expected, got)
	def test_encoding_unicode_ae(self):
		name = "Æther Vial"
		expected = "aether-vial"
		got = format_card_name(name)
		self.assertEqual(expected, got)
	def test_encoding_accent(self):
		name = "El-Hajjâj"
		expected = "el-hajjaj"
		got = format_card_name(name)
		self.assertEqual(expected, got)