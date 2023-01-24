#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional

_DICO = {
    "00": "",
    "0": "zéro",
    "1": "un",
    "01": "un",
    "2": "deux",
    "02": "deux",
    "3": "trois",
    "03": "trois",
    "4": "quatre",
    "04": "quatre",
    "5": "cinq",
    "05": "cinq",
    "6": "six",
    "06": "six",
    "7": "sept",
    "07": "sept",
    "8": "huit",
    "08": "huit",
    "9": "neuf",
    "09": "neuf",
    "10": "dix",
    "11": "onze",
    "12": "douze",
    "13": "treize",
    "14": "quatorze",
    "15": "quinze",
    "16": "seize",
    "17": "dix-sept",
    "18": "dix-huit",
    "19": "dix-neuf",
    "20": "vingt",
    "30": "trente",
    "40": "quarante",
    "50": "cinquante",
    "60": "soixante",
    "80": "quatre-vingt",
}


class SommeVersLettres:
    """Converti une somme (float) en lettres (utilisé notamment pour les chèques et les bulletins de soutien)"""

    nombre = 0

    def conversion(self, nombre: float, monnaie: str = "euro"):
        assert isinstance(nombre, float)
        nombre = round(nombre, 2)
        self.nombre = nombre

        mantisse, liste_nombre = self._preparation(nombre)
        liste_mots = self._traitement_segment(mantisse, liste_nombre)
        return self._nom_puissances(liste_mots, monnaie)

    def _nettoyage_tirets(self, result: str) -> str:
        return result \
            .replace("-euros", " euros ") \
            .replace("euros-", " euros ") \
            .strip()

    def _segmentation(self, entiere: str) -> List[str]:
        """Découpe un nombre en sous-nombres de 3 chiffres"""
        liste_nombre = []
        seg_num = ""

        # Création des blocs de 3 chiffres
        for i in entiere[::-1]:
            seg_num += i
            if len(seg_num) == 3:
                liste_nombre.append("".join(seg_num[::-1]))
                seg_num = ""

        # Récupération du reste (inférieur à 3 chiffres)
        if len(seg_num):
            liste_nombre.append("{:0>3}".format("".join(seg_num[::-1])))

        return liste_nombre

    def _traitement_segment(self, mantisse: str, liste_nombre: List[str]):
        """Converti chaque sous-nombre individuellement en lettres"""
        liste_mots = [self._nom_dizaine(mantisse, is_mantisse=True)]
        for i in liste_nombre:
            centaine = self._nom_centaine(i)
            dizaine = self._nom_dizaine(i)
            if centaine and dizaine:
                liste_mots.append(centaine + "-" + dizaine)
            elif centaine:
                liste_mots.append(centaine)
            else:
                liste_mots.append(dizaine)
        return liste_mots

    def _preparation(self, nombre: float) -> Tuple[str, List[str]]:
        """Démembre la mantisse et le nombre en sous-nombres"""
        n_str = str(nombre)
        entiere, mantisse = n_str.split(".", 1)
        # Evite que : 0.1 ne devienne 1 centime au lieu de 10 centimes
        mantisse = f"{mantisse:0<2}"
        liste_nombre = self._segmentation(entiere)

        return mantisse, liste_nombre

    def _recadrage(
        self, nombre: str, is_centaine: bool = False, is_mantisse: bool = False
    ) -> str:
        """Ajuste le nombre sur la portion à nommer"""
        if is_centaine:
            return f"{nombre:0>3}"[:1]
        else:
            if is_mantisse:
                return f"{nombre:0<2}"[:2]
        return f"{nombre:0>3}"[-2:]

    def _nom_dizaine(self, nombre: str, is_mantisse: bool = False) -> str:
        """Génère la dizaine et l'unité d'un nombre à 3 chiffres"""
        nombre = self._recadrage(nombre, is_mantisse=is_mantisse)

        # Traitement des dizaines
        if nombre in _DICO:
            return _DICO[nombre]
        elif int(nombre) > 80:
            return _DICO["80"] + "-" + _DICO[str(int(nombre) - 80)]
        elif int(nombre) > 60:
            if nombre == "61" or nombre == "71":
                return _DICO["60"] + "-et-" + _DICO[str(int(nombre) - 60)]
            else:
                return _DICO["60"] + "-" + _DICO[str(int(nombre) - 60)]
        elif int(nombre) > 20:
            diz = str(nombre)[:1] + "0"
            if int(nombre) - int(diz) == 1:
                return _DICO[diz] + "-et-" + _DICO[str(int(nombre) - int(diz))]
            return _DICO[diz] + "-" + _DICO[str(int(nombre) - int(diz))]

        # Cas particulier (non géré)
        return ""

    def _nom_centaine(self, nombre: str) -> str:
        """Génère la centaine d'un nombre à 3 chiffres"""
        nombre = self._recadrage(nombre, is_centaine=True)

        if nombre == "0":
            return ""
        elif nombre == "1":
            return "cent"
        else:
            return _DICO[nombre] + "-cent"

    def _pluriel(self, nom: str) -> str:
        return "" if nom == "un" else "s"

    def _gen_centimes(self, centimes: str, unites: str = "", puissances: Optional[List[str]] = None) -> str:
        puissances = puissances or []

        if centimes and not unites and not puissances:
            return f"{centimes} centime{self._pluriel(centimes)}"
        elif centimes:
            return f"et {centimes} centime{self._pluriel(centimes)}"
        return ""

    def _gen_unites(self, monnaie: str, unites: str = "", puissances: Optional[List[str]] = None):
        puissances = puissances or []

        if unites:
            return f"{unites} {monnaie}{self._pluriel(unites)}"
        elif puissances:
            return f"{monnaie}s"
        return ""

    def _gen_puissances(self, puissances: Optional[List[str]] = None):
        puissances = puissances or []
        mots = []
        liste = ["mille", "million", "milliard"]

        for i, mot in enumerate(puissances):
            if i % 3 == 0 and mot:  # Milliers
                num = f"{mot}-" if mot != "un" else ""
                mots.append(f"{num}{liste[i % 3]}")

            elif i % 3 in [1, 2] and mot:  # Sauf milliers
                mots.append(f"{mot}-{liste[i % 3]}{self._pluriel(mot)}")
        return mots

    def _jonction(self, mots: List[str]) -> str:
        mots_ordre = mots[::-1]
        grands_nombres = '-'.join(mots_ordre[:-2])
        unites_et_centimes = ' '.join(mots_ordre[-2:])

        if grands_nombres:
            return f"{grands_nombres}-{unites_et_centimes}"
        else:
            return unites_et_centimes

    def _nom_puissances(self, liste_mots: list, monnaie: str = "euro") -> str:
        """Génère les noms des puissances de 3 (milliers, millions etc...)"""
        centimes, unites, *puissances = liste_mots

        mots = [
            self._gen_centimes(centimes, unites, puissances),
            self._gen_unites(monnaie, unites, puissances),
        ]
        mots.extend(self._gen_puissances(puissances))

        return self._nettoyage_tirets(
            self._jonction(mots)
        )
