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
            (100.052, "cent euro et cinq centimes"),  # Mantisse arrondie
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

    def test_traitement_segment(self):
        liste_nombre = ["456", "009", "123", "098"]
        mantisse = "12"
        result = self.svl._traitement_segment(mantisse, liste_nombre)
        self.assertEqual(
            result,
            [
                "douze",
                "quatre-cent-cinquante-six",
                "neuf",
                "cent-vingt-trois",
                "quatre-vingt-dix-huit",
            ],
        )

    def test_preparation(self):
        nombre = 123.87
        mantisse, liste_nombres = self.svl._preparation(nombre)
        self.assertEqual(mantisse, "87")
        self.assertEqual(liste_nombres, ["123"])

    def test_recadrage_mantisse_base(self):
        result = self.svl._recadrage("82", is_mantisse=True)
        self.assertEqual(result, "82")

    def test_recadrage_mantisse_court(self):
        result = self.svl._recadrage("2", is_mantisse=True)
        self.assertEqual(result, "20")

    def test_recadrage_mantisse_long(self):
        result = self.svl._recadrage("675", is_mantisse=True)
        self.assertEqual(result, "67")

    def test_recadrage_dizaine_base(self):
        result = self.svl._recadrage("17")
        self.assertEqual(result, "17")

    def test_recadrage_dizaine_court(self):
        result = self.svl._recadrage("7")
        self.assertEqual(result, "07")

    def test_recadrage_dizaine_long(self):
        result = self.svl._recadrage("167")
        self.assertEqual(result, "67")

    def test_recadrage_centaine_base(self):
        result = self.svl._recadrage("453", is_centaine=True)
        self.assertEqual(result, "4")

    def test_recadrage_centaine_court(self):
        result = self.svl._recadrage("7", is_centaine=True)
        self.assertEqual(result, "0")

    def test_recadrage_centaine_long(self):
        result = self.svl._recadrage("20", is_centaine=True)
        self.assertEqual(result, "0")

    def test_nom_dizaine_dans_dico(self):
        result = self.svl._nom_dizaine("16")
        self.assertEqual(result, "seize")

    def test_nom_dizaine_sup_80(self):
        result = self.svl._nom_dizaine("89")
        self.assertEqual(result, "quatre-vingt-neuf")

    def test_nom_dizaine_sup_60(self):
        result = self.svl._nom_dizaine("64")
        self.assertEqual(result, "soixante-quatre")

    def test_nom_dizaine_sup_60_et_1(self):
        result = self.svl._nom_dizaine("61")
        self.assertEqual(result, "soixante-et-un")

    def test_nom_dizaine_sup_60_et_11(self):
        result = self.svl._nom_dizaine("71")
        self.assertEqual(result, "soixante-et-onze")

    def test_nom_dizaine_sup_20(self):
        result = self.svl._nom_dizaine("25")
        self.assertEqual(result, "vingt-cinq")

    def test_nom_dizaine_sup_20_et_1(self):
        result = self.svl._nom_dizaine("41")
        self.assertEqual(result, "quarante-et-un")

    def test_nom_centaine(self):
        result = self.svl._nom_centaine("410")
        self.assertEqual(result, "quatre-cent")

    def test_nom_centaine_special(self):
        result = self.svl._nom_centaine("124")
        self.assertEqual(result, "cent")

    def test_nom_centaine_absente(self):
        result = self.svl._nom_centaine("069")
        self.assertEqual(result, "")
