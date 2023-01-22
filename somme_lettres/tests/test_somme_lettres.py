import unittest

from somme_lettres import SommeVersLettres


class TestSommeVersLettres(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.svl = SommeVersLettres()

    def test_convertions_sommes_lettres(self):
        
        valeurs = [
            # (0.01, "un centime"),
            (8.0, "huit euro"),
            (12.59, "douze euro et cinquante-neuf centimes"),
            (100.05, "cent euro et cinq centimes"),
            (192.75, "cent-quatre-vingt-douze euro et soixante-quinze centimes"),
            (1000.00, "mille  euro"),  # FIXME: double espace non désiré
            (
                8_753.9,
                "huit-mille sept-cent-cinquante-trois euro et quatre-vingt-dix centimes",
            ),  # FIXME: tiret après les milliers attendu
            (
                72_654.02,
                "soixante-douze-mille six-cent-cinquante-quatre euro et deux centimes",
            ),  # FIXME: tiret après les milliers attendu
        ]

        for somme, lettres in valeurs:
            with self.subTest(somme):
                self.assertEqual(self.svl.conversion(somme), lettres)

    def test_segmentation_petit_nombre(self):
        result: list = self.svl._segmentation("1")
        self.assertEqual(result, ["001"])

    def test_segmentation_en_deux(self):
        result: list = self.svl._segmentation("123456")
        self.assertEqual(result, ["456", "123"])

    def test_segmentation_en_trois_avec_partie_reduite(self):
        result: list = self.svl._segmentation("98123456")
        self.assertEqual(result, ["456", "123", "098"])
