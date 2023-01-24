import unittest

from somme_lettres import SommeVersLettres


class TestSommeVersLettres(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.svl = SommeVersLettres()

    def test_convertions_sommes_lettres(self):

        valeurs = [
            (0.01, "un centime"),
            (5.0, "cinq euros"),
            (8.0, "huit euros"),
            (12.59, "douze euros et cinquante-neuf centimes"),
            (100.052, "cent euros et cinq centimes"),  # Mantisse arrondie
            (192.75, "cent-quatre-vingt-douze euros et soixante-quinze centimes"),
            (1000.00, "mille euros"),
            (10_000.00, "dix-mille euros"),
            (100_005.00, "cent-mille-cinq euros"),
            (1_000_000.00, "un-million euros"),
            (1_000_000_100.10, "un-milliard-cent euros et dix centimes"),
            (
                9_999_000_000_100.00,
                "neuf-billions-neuf-cent-quatre-vingt-dix-neuf-milliards-cent euros",
            ),
            (
                8_753.9,
                "huit-mille-sept-cent-cinquante-trois euros et quatre-vingt-dix centimes",
            ),
            (
                72_654.02,
                "soixante-douze-mille-six-cent-cinquante-quatre euros et deux centimes",
            ),
            (
                147_258_369.0,
                "cent-quarante-sept-millions-deux-cent-cinquante-huit-mille-trois-cent-soixante-neuf euros",
            ),
            (
                465_789_147_258_369.0,
                "quatre-cent-soixante-cinq-billions-sept-cent-quatre-vingt-neuf-milliards-cent-quarante-sept-millions-deux-cent-cinquante-huit-mille-trois-cent-soixante-neuf euros",
            ),
        ]

        for somme, lettres in valeurs:
            with self.subTest(somme):
                self.assertEqual(self.svl.conversion(somme), lettres)

    def test_type_error_conversion(self):
        with self.assertRaises(TypeError) as e:
            self.svl.conversion(456)
            self.assertEqual(
                e.exception, "Le nombre à convertir doit être de type float"
            )

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

    def test_value_error_preparation(self):
        nombre = 12345678901234567890123456789012345678901234567890123456789012345678901234567890.0
        with self.assertRaises(ValueError) as e:
            self.svl._preparation(nombre)
            self.assertEqual(
                e.exception,
                "Le nombre a convertir dépasse les capacité de traitement actuelle: 10^78 maximum",
            )

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

    def test_nom_puissance_centimes_uniquement(self):
        result = self.svl._nom_puissances(["douze", ""])
        self.assertEqual(result.strip(), "douze centimes")

    def test_singulier(self):
        result = self.svl._pluriel("un")
        self.assertEqual(result, "")

    def test_pluriel(self):
        result = self.svl._pluriel("autre")
        self.assertEqual(result, "s")

    def test_gen_centimes_singulier(self):
        centimes = "un"
        result = self.svl._gen_centimes(centimes)
        self.assertEqual(result, "un centime")

    def test_gen_centimes_uniquement(self):
        centimes = "vingt-quatre"
        result = self.svl._gen_centimes(centimes)
        self.assertEqual(result, "vingt-quatre centimes")

    def test_gen_centimes_et_unites_seulement(self):
        centimes = "vingt-quatre"
        unites = "un"
        result = self.svl._gen_centimes(centimes, unites)
        self.assertEqual(result, "et vingt-quatre centimes")

    def test_gen_centimes_puissances_seulement(self):
        centimes = "vingt-quatre"
        puissances = ["mille"]
        result = self.svl._gen_centimes(centimes, puissances=puissances)
        self.assertEqual(result, "et vingt-quatre centimes")

    def test_gen_centimes_complet(self):
        centimes = "vingt-quatre"
        unites = "un"
        puissances = ["mille"]
        result = self.svl._gen_centimes(centimes, unites, puissances)
        self.assertEqual(result, "et vingt-quatre centimes")

    def test_gen_unites_singulier(self):
        monnaie = "euro"
        unites = "un"
        result = self.svl._gen_unites(monnaie, unites)
        self.assertEqual(result, "un euro")

    def test_gen_unites(self):
        monnaie = "euro"
        unites = "dix"
        result = self.svl._gen_unites(monnaie, unites)
        self.assertEqual(result, "dix euros")

    def test_gen_unites_autre_monnaie(self):
        monnaie = "franc"
        unites = "dix"
        result = self.svl._gen_unites(monnaie, unites)
        self.assertEqual(result, "dix francs")

    def test_gen_unites_avec_puissance(self):
        monnaie = "franc"
        puissances = ["mille"]
        result = self.svl._gen_unites(monnaie, puissances=puissances)
        self.assertEqual(result, "francs")

    def test_gen_unites_complet(self):
        monnaie = "franc"
        unites = "dix"
        puissances = ["mille"]
        result = self.svl._gen_unites(monnaie, unites, puissances)
        self.assertEqual(result, "dix francs")

    def test_gen_puissances_vide(self):
        result = self.svl._gen_puissances()
        self.assertEqual(result, [])

    def test_gen_puissances_3_un(self):
        puissances = ["un"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["mille"])

    def test_gen_puissances_3(self):
        puissances = ["onze"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["onze-mille"])

    def test_gen_puissances_6_un(self):
        puissances = ["", "un"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["un-million"])

    def test_gen_puissances_6(self):
        puissances = ["", "onze"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["onze-millions"])

    def test_gen_puissances_9_un(self):
        puissances = ["", "", "un"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["un-milliard"])

    def test_gen_puissances_9(self):
        puissances = ["", "", "onze"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["onze-milliards"])

    def test_gen_puissances_12_un(self):
        puissances = ["", "", "", "un"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["un-billion"])

    def test_gen_puissances_12(self):
        puissances = ["", "", "", "onze"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["onze-billions"])

    def test_gen_puissances_15_un(self):
        puissances = ["", "", "", "", "un"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["un-billiard"])

    def test_gen_puissances_15(self):
        puissances = ["", "", "", "", "onze"]
        result = self.svl._gen_puissances(puissances)
        self.assertEqual(result, ["onze-billiards"])
