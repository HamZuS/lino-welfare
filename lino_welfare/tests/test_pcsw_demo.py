# -*- coding: utf-8 -*-
# Copyright 2011-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module contains tests that are run on a demo database.
  
To run only this test suite::

  $ cd ~/hgwork/welfare
  $ python manage.py test lino_welfare.DemoTest
  
Methods named `test0*` do not modify any data.

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils import translation
from django.core.exceptions import ValidationError

from lino import dd
from djangosite.utils.djangotest import RemoteAuthTestCase

cbss = dd.resolve_app('cbss')
Event = dd.resolve_model('cal.Event')


class PseudoRequest:

    def __init__(self, name):
        self.user = settings.SITE.user_model.objects.get(username=name)
        self.subst_user = None


class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    #~ fixtures = [ 'std','demo' ]
    fixtures = settings.SITE.demo_fixtures
    #~ fixtures = 'std few_countries few_cities few_languages props cbss democfg demo demo2'.split()
    #~ fixtures = 'std all_countries few_cities all_languages props demo'.split()
    #~ never_build_site_cache = True

    #~ avoid do_print failure due to build_absolute_uri() when use_davlink is True
    # override_djangosite_settings = dict(use_davlink=False)

    def test001(self):
        #~ run_db_overview_test(self)
        """
        Test the number of rows returned for certain queries
        """

        #~ def test002(self):
        """
        Printing a Budget
        The same as in tests/debts.rst, but a different implementation
        """

        """
        All demo requests should have at least one row of result.
        """
        ses = settings.SITE.login('rolf')
        for obj in cbss.RetrieveTIGroupsRequest.objects.all():
            msg = "%s has no result" % obj
            self.assertNotEqual(obj.Result(ses).get_total_count(), 0, msg)

    def unused_test001(self):
        """
        Some simple tests:
        - total number of Person records
        - name of some person
        """
        Person = dd.resolve_model('contacts.Person')
        #~ from lino.projects.pcsw.models import Person
        self.assertEquals(Person.objects.count(), 78)

        p = Person.objects.get(pk=118)
        #~ self.assertEquals(unicode(p), "ARENS Annette (118)")
        #~ self.assertEquals(unicode(p), "AUSDEMWALD Alfons (118)")
        #~ self.assertEquals(unicode(p), "COLLARD Charlotte (118)")
        self.assertEquals(unicode(p), "Herrn Laurent BASTIAENSEN")
        #~ self.assertEquals(unicode(p), "BASTIAENSEN Laurent (118)")

    def unused_test002(self):
        """
        Tests whether SoftSkillsByPerson works and whether it returns language-specific labels.
        Bug discovered :blogref:`20110228`.
        See also :blogref:`20110531`.

        """
        #~ from lino.modlib.users.models import User
        #~ u = User.objects.get(username='rolf')
        #~ lang = u.language
        # ~ u.language = '' # HTTP_ACCEPT_LANGUAGE works only when User.language empty
        #~ u.save()

        settings.SITE.ui  # trigger ui instance

        obj = pcsw.Client.objects.get(pk=128)
        ar = cv.SoftSkillsByPerson.request(master_instance=obj)

        pk = 128
        mt = 44
        url = '/api/cv/SoftSkillsByPerson?mt=%d&mk=%d&fmt=json' % (mt, pk)

        #~ if 'en' in babel.AVAILABLE_LANGUAGES:
        if settings.SITE.get_language_info('en'):
            response = self.client.get(
                url, REMOTE_USER='robin', HTTP_ACCEPT_LANGUAGE='en')
            #~ result = self.check_json_result(response,'count rows gc_choices disabled_actions title')
            result = self.check_json_result(
                response, 'count rows title success no_data_text')
            self.assertEqual(result['title'],
                             "Soft skills of EVERS Eberhart (%d)" % pk)
            self.assertEqual(len(result['rows']), 2)
            row = result['rows'][0]
            self.assertEqual(row[0], "Obedient")
            #~ self.assertEqual(row[1],7)
            self.assertEqual(row[2], "moderate")
            self.assertEqual(row[3], "2")

        #~ if 'de' in babel.AVAILABLE_LANGUAGES:
        if settings.SITE.get_language_info('de'):
            response = self.client.get(
                url, REMOTE_USER='rolf', HTTP_ACCEPT_LANGUAGE='de')
            result = self.check_json_result(
                response, 'count rows title success no_data_text')
            self.assertEqual(result['title'],
                             "Eigenschaften von EVERS Eberhart (%d)" % pk)
            self.assertEqual(len(result['rows']), 2)
            row = result['rows'][0]
            self.assertEqual(row[0], "Gehorsam")
            #~ self.assertEqual(row[1],7)
            self.assertEqual(row[2], "mittelmäßig")
            self.assertEqual(row[3], "2")

        # ~ 20111111 babel.set_language(None) # switch back to default language for subsequent tests

        u.language = lang
        u.save()

        #~ tf('http://127.0.0.1:8000/api/properties/SoftSkillsByPerson?_dc=1298881440121&fmt=json&mt=22&mk=15',
            #~ """
            #~ {
            #~ count: 3,
            #~ rows: [
              #~ [ "Gehorsam", 7, "mittelm\u00e4\u00dfig", "2", null, 53, "Sozialkompetenzen", 2 ],
              #~ [ "F\u00fchrungsf\u00e4higkeit", 8, "mittelm\u00e4\u00dfig", "2", null, 54, "Sozialkompetenzen", 2 ],
              #~ [ null, null, null, null, null, null, "Sozialkompetenzen", 2 ]
            #~ ],
            #~ gc_choices: [  ],
            #~ title: "~Eigenschaften pro Person Arens Annette (15)"
            #~ }
            #~ """)
    def unused_test003(self):
        """
        Test whether the AJAX call issued for Detail of Annette Arens is correct.
        """
        cases = [
            #  [ id,         name, recno, first, prev, next, last ]
            [119, "Charlier",     8,   199,  201,  118, 166],
            [167, "Ärgerlich",   56,   199,  164,  166, 166],
            [166, "Östges",      57,   199,  167, None, 166],
        ]
        #
        for case in cases:
            url = '/api/contacts/Persons/%s?fmt=json' % case[0]
            response = self.client.get(url, REMOTE_USER='root')
            result = self.check_json_result(
                response, 'navinfo disable_delete data id title')
            # disabled because they depend on local database sorting configuration
            # re-enabled because demo fixtures no longer contain cyrillic chars
            self.assertEqual(result['data']['last_name'], case[1])
            self.assertEqual(result['navinfo']['recno'], case[2])
            self.assertEqual(result['navinfo']['first'], case[3])
            self.assertEqual(result['navinfo']['prev'], case[4])
            self.assertEqual(result['navinfo']['next'], case[5])
            self.assertEqual(result['navinfo']['last'], case[6])

    def unused_test004(self):
        """
        Test whether date fields are correctly parsed.
        """
        for value in ('01.03.2011', '15.03.2011'):
            url = '/api/jobs/Contracts/1'
            #~ data =  'applies_from='+value+'&applies_until=17.05.2009&company=R-Cycle%20'
            #~ 'Sperrgutsortierzentrum&companyHidden=83&contact=Arens%20Andreas%20(1'
            #~ '4)%20(Gesch%C3%A4ftsf%C3%BChrer)&contactHidden=2&date_decided=&date_e'
            #~ 'nded=&date_issued=&delay_type=Tage&delay_typeHidden=D&delay_value=0&du'
            #~ 'ration=&ending=Vertragsbeendigung%20ausw%C3%A4hlen...&endingHidden=&lan'
            #~ 'guage=Deutsch&languageHidden=de&person=Altenberg%20Hans%20(16)&personHi'
            #~ 'dden=16&reminder_date=11.11.2010&reminder_text=demo%20reminder&type=Kon'
            #~ 'vention%20Art.60%C2%A77%20Sozial%C3%B6konomie&typeHidden=1&user=root&us'
            #~ 'erHidden=4&user_asd=Benutzer%20ausw%C3%A4hlen...&user_asdHidden='
            data = 'applies_from=' + value

            response = self.request_PUT(url, data, REMOTE_USER='root')
            result = self.check_json_result(
                response, 'message success data_record')
            self.assertEqual(result['success'], True)
            self.assertEqual(result['data_record']
                             ['data']['applies_from'], value)

            url = "/api/jobs/Contracts/1?fmt=json"
            response = self.client.get(url, REMOTE_USER='root')
            #~ print 20110723, response
            result = self.check_json_result(
                response, 'navinfo disable_delete data id title')
            self.assertEqual(result['data']['applies_from'], value)

    def unused_test005(self):
        """
        Simplification of test04, used to write Lino ticket #27.
        """
        url = '/api/countries/Countries/BE'
        value = 'Belgienx'
        data = 'name=%s&nameHidden=Belgienx&fmt=json' % value
        response = self.request_PUT(url, data, REMOTE_USER='root')
        #~ response = self.client.put(url,data,content_type='application/x-www-form-urlencoded')
        result = self.check_json_result(
            response, 'message success data_record')
        self.assertEqual(result['success'], True)
        self.assertEqual(result['data_record']['data']['name'], value)

        url = '/api/countries/Countries/BE?fmt=json'
        response = self.client.get(url, REMOTE_USER='root')
        result = self.check_json_result(
            response, 'navinfo disable_delete data id title')
        self.assertEqual(result['data']['name'], value)

    def unused_test006(self):
        """
        Testing BabelValues.
        """
        from lino.utils import babel
        from lino_welfare.modlib.pcsw.models import Person
        #~ from lino.apps.pcsw.models import Property, PersonProperty
        Property = settings.SITE.modules.properties.Property
        PersonProperty = settings.SITE.modules.properties.PersonProperty
        annette = Person.objects.get(pk=118)
        self.assertEquals(unicode(annette), "ARENS Annette (118)")

        p = Property.objects.get(id=2)  # "Obedient"
        pp = PersonProperty.objects.filter(property=p)[0]

        #~ if 'en' in babel.AVAILABLE_LANGUAGES:
        with translation.override('en'):
        #~ if settings.SITE.get_language_info('en'):
            #~ dd.set_language('en')
            self.assertEquals(unicode(p), u"Obedient")
            self.assertEquals(unicode(pp), u"not at all")

        #~ if 'de' in babel.AVAILABLE_LANGUAGES:
        with translation.override('de'):
        #~ if settings.SITE.get_language_info('de'):
            #~ dd.set_language('de')
            self.assertEquals(unicode(p), u"Gehorsam")
            self.assertEquals(unicode(pp), u"gar nicht")

        #~ if 'fr' in babel.AVAILABLE_LANGUAGES:
        with translation.override('fr'):
        #~ if settings.SITE.get_language_info('fr'):
            #~ dd.set_language('fr')
            self.assertEquals(unicode(p), u"Obéissant")
            self.assertEquals(unicode(pp), u"pas du tout")

        # ~ dd.set_language(None) # switch back to default language for subsequent tests

    def unused_test009(self):
        """
        This tests for the bug discovered :blogref:`20110610`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_demo_tests.py`.
        """
        #~ dd.set_language('en')
        url = '/choices/jobs/StudiesByPerson/city?start=0&limit=30&country=&query='
        response = self.client.get(url, REMOTE_USER='root')
        result = self.check_json_result(response, 'count rows')
        #~ self.assertEqual(result['title'],u"Choices for city")
        self.assertEqual(len(result['rows']), 30)
        # ~ dd.set_language(None) # switch back to default language for subsequent tests

    def unused_test010(self):
        """
        Test the unique_together validation of Place
        See :blogref:`20110610` and :blogref:`20110611`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_demo_tests.py`.
        """
        from lino.modlib.countries.models import Place, Country
        from django.db.utils import IntegrityError
        be = Country.objects.get(pk='BE')
        try:
            Place(name="Eupen", country=be, zip_code='4700').save()
        except IntegrityError:
            if settings.SITE.allow_duplicate_cities:
                self.fail(
                    "Got IntegrityError though allow_duplicate_cities should be allowed.")
        else:
            if not settings.SITE.allow_duplicate_cities:
                self.fail("Expected IntegrityError")

        try:
            be.place_set.create(name="Eupen", zip_code='4700')
        except IntegrityError:
            if settings.SITE.allow_duplicate_cities:
                self.fail(
                    "Got IntegrityError though allow_duplicate_cities should be allowed.")
        else:
            if not settings.SITE.allow_duplicate_cities:
                self.fail("Expected IntegrityError")

    def unused_test011(self):
        """
        Tests whether the user problem
        described in :blogref:`20111206`
        is solved.
        """
        from lino_welfare.modlib.jobs.models import Contract
        obj = Contract.objects.get(pk=5)
        with translation.override('de'):
            self.assertEqual(obj.contact.person.get_full_name(),
                             "Herrn Hans ALTENBERG")
        #~ dd.set_language(None)
        #~ translation.deactivate()

    def unused_test012(self):
        """
        Test whether the contact person of a jobs contract is correctly filled in
        when the provider has exactly one contact person.
        """
        from lino_welfare.modlib.jobs.models import Contract, JobProvider, Job
        from lino_welfare.modlib.pcsw.models import Person
        from lino.modlib.users.models import User
        u = User.objects.get(username='root')
        #~ qs = Person.objects.order_by('last_name','first_name')
        p = Person.objects.get(pk=177)  # Emil Eierschal
        #~ e = Employer.objects.get(pk=185)
        j = Job.objects.get(pk=1)  # bisa
        c = Contract(person=p, user=u, job=j,
                     applies_from=p.coached_from, duration=312)
        c.full_clean()
        c.save()
        self.assertEqual(c.contact.person.pk, 118)
        #~ self.assertEqual(c.applies_until,p.coached_from+datetime.timedelta(days=))

    def unused_test014(self):
        """
        Tests for the bug discovered :blogref:`20111222`.
        """
        for url in """\
        /choices/isip/Contract/person?start=0&limit=10&query=
        /choices/contacts/Person/city?start=0&limit=10&country=BE&query=
        /choices/jobs/Contract/duration
        """.splitlines():
            url = url.strip()
            if url and not url.startswith("#"):
                response = self.client.get(url, REMOTE_USER='root')
                result = self.check_json_result(response, 'count rows')
                #~ self.assertEqual(result['title'],u"Choices for city")
                self.assertEqual(len(result['rows']), min(result['count'], 10))

    def unused_test015(self):
        """
        Temporary bug on :blogref:`20111223`.
        """
        url = '/api/contacts/Persons/-99999?fmt=json&an=insert'
        response = self.client.get(url, REMOTE_USER='root')
        result = self.check_json_result(response, 'data phantom title')
        self.assertEqual(result['phantom'], True)

    def unused_test015b(self):
        """
        Test whether PropsByGroup has a detail.
        20120218 : "properties.PropsByGroup has no action u'detail'"
        """
        cases = [
            ('/api/properties/PropsByGroup/%s?mt=11&mk=1&an=detail&fmt=json', 8),
            ('/api/contacts/AllPartners/%s?an=detail&fmt=json', 117),
        ]
        for case in cases:
            url = case[0] % case[1]
            response = self.client.get(url, REMOTE_USER='root')
            result = self.check_json_result(response,
                                            'navinfo disable_delete data title disabled_actions id')
            self.assertEqual(result['id'], case[1])

    def unused_test016(self):
        """
        All rows of persons_by_user now clickable.
        See :blogref:`20111223`.
        """
        cases = [
            ['root', 19],
            ['alicia', 17],
        ]
        for case in cases:
            url = '/api/pcsw/MyPersons?fmt=json&limit=30&start=0&su=%s' % case[0]
            response = self.client.get(url, REMOTE_USER='root')
            result = self.check_json_result(
                response, 'count rows gc_choices disabled_actions title')
            self.assertEqual(result['count'], case[1])

    def unused_test017(self):
        # moved to docs/tested
        Budget = resolve_model('debts.Budget')
        bud = Budget.objects.get(pk=3)
        s = bud.BudgetSummary().to_rst()
        #~ print s
        self.assertEquivalent(s, """
        ========================================================= ==============
         Beschreibung                                              Betrag
        --------------------------------------------------------- --------------
         Monatliche Einkünfte                                      5 000,00
         Jährliche Einkünfte (2 400,00 / 12)                       200,00
         Monatliche Ausgaben                                       -550,00
         Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
         Raten der laufenden Kredite                               -45,00
         **Finanzielle Situation**                                 **4 585,33**
        ========================================================= ==============
        """)

    def unused_test101(self):
        """
        First we try to uncheck the is_jobprovider checkbox on
        the Company view of a JobProvider.
        This should fail since the JP has Jobs and Contracts.
        """
        Company = resolve_model('contacts.Company')
        JobProvider = resolve_model('jobs.JobProvider')
        Job = resolve_model('jobs.Job')
        Contract = resolve_model('jobs.Contract')
        bisaProvider = JobProvider.objects.get(name='BISA')
        bisaCompany = Company.objects.get(name='BISA')

        # it should work even on an imported partner
        save_iip = settings.SITE.is_imported_partner

        def f(obj):
            return True
        settings.SITE.is_imported_partner = f

        JOBS = Job.objects.filter(provider=bisaProvider)
        self.assertEqual(JOBS.count(), 3)
        rr = PseudoRequest('rolf')
        try:
            Company.is_jobprovider.set_value_in_object(rr, bisaCompany, False)
            self.fail("Expected ValidationError")
        except ValidationError, e:
            # cannot delete because there are 3 Jobs referring to BISA
            pass
        for job in JOBS:
            for cont in Contract.objects.filter(job=job):
                cont.delete()
            job.delete()
        Company.is_jobprovider.set_value_in_object(rr, bisaCompany, False)

        bisaCompany = Company.objects.get(name='BISA')  # still exists

        try:
            bisaProvider = JobProvider.objects.get(name='BISA')
            self.fail("Expected JobProvider.DoesNotExist")
        except JobProvider.DoesNotExist, e:
            pass

        # restore is_imported_partner method
        settings.SITE.is_imported_partner = save_iip
