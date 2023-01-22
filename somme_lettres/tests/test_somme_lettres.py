import unittest

from somme_lettres import SommeVersLettres


class TestSommeVersLettres(unittest.TestCase):
    def test_convertions_sommes_lettres(self):
        svl = SommeVersLettres()
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
                self.assertEqual(svl.conversion(somme), lettres)
