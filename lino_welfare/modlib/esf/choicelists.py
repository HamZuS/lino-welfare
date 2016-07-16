# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

"""Choicelists for `lino_welfare.modlib.esf`.

"""
from __future__ import unicode_literals

from django.db import models

from lino.api import dd, _


class ParticipationCertificates(dd.ChoiceList):
    verbose_name = _("Participation Certificate")
    verbose_name_plural = _("Participation Certificates")
add = ParticipationCertificates.add_item
add('10', _("Epreuve d’évaluation réussie sans titre spécifique"))


class StatisticalField(dd.Choice):

    field_name = None
    field = None

    def __init__(self, value, text, name=None, **kwargs):
        super(StatisticalField, self).__init__(value, text, name, **kwargs)
        self.field = models.IntegerField(value, default=0, help_text=text)
        self.field_name = "esf" + value

    def collect_value_from_guest(self, obj):
        if obj.event.event_type is None:
            return 0
        sf = obj.event.event_type.esf_field
        if sf is not None and sf.value == self.value:
            return 1
        return 0


class StatisticalFields(dd.ChoiceList):
    verbose_name = _("ESF field")
    verbose_name_plural = _("ESF fields")
    item_class = StatisticalField

add = StatisticalFields.add_item
add('10', _("Informative sessions"))     # Séance d'info
add('20', _("Individual consultation"))  # Entretien individuel
add('21', _("Evaluation of external training"))  # Evaluation formation externe et art.61
add('30', _("Certified integration service"))  # S.I.S. agréé
add('40', _("Level tests"))  # Tests de niveau
add('41', _("IT basics"))  # Initiation informatique
add('42', _("Mobility"))  # Mobilité
add('43', _("Remedial teaching"))  # Remédiation mathématique et français
add('44', _("Wake up!"))  # Activons-nous
add('50', _("Getting a professional situation")) # Mise en situation professionnelle
add('60', _("Cyber Job"))  # Cyber-employ
add('70', _("Art 60§7 job supplyment"))  # Mise à l’emploi sous contrat art.60§7


@dd.receiver(dd.pre_analyze)
def inject_statistical_fields(sender, **kw):
    for sf in StatisticalFields.items():
        if sf.field_name is not None:
            dd.inject_field('esf.ClientSummary', sf.field_name, sf.field)

dd.inject_field(
    'cal.EventType', 'esf_field', StatisticalFields.field(blank=True))
