# -*- coding: UTF-8 -*-
## Copyright 2008-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module requires a model `courses.CourseProvider` 
to be defined by the application.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
#~ from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
#~ from lino.modlib.uploads import models as uploads
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
#~ from north import babel 
from lino.dd import dtos
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
#~ from lino.core.dbutils import obj2str

pcsw = dd.resolve_app('pcsw')

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.pcsw.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

#~ if settings.SITE.user_model:
    #~ User = dd.resolve_model(settings.SITE.user_model,strict=True)

#~ Company = resolve_model('contacts.Company')
class CourseProvider(pcsw.Company):
    """
    A CourseProvider is a Company that offers Courses. 
    """
    class Meta:
        #~ app_label = 'courses'
        verbose_name = _("Course provider")
        verbose_name_plural = _("Course providers")
    #~ name = models.CharField(max_length=200,
          #~ verbose_name=_("Name"))
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))
    
    def disable_delete(self,ar):
        # skip the is_imported_partner test
        return super(pcsw.Partner,self).disable_delete(ar)
        
    
    
dd.inject_field(pcsw.Company,
    'is_courseprovider',
    mti.EnableChild(CourseProvider,verbose_name=_("is Course Provider")),
    """Whether this Company is also a Course Provider."""
    )

    
    
class CourseProviderDetail(pcsw.CompanyDetail):
    """
    This is the same as CompanyDetail, except that we remove MTI fields
    and add a tab :guilabel:`Courses`.
    """
    box5 = "remarks" 
    main = "general notes CourseOffersByProvider"

  

#~ class CourseProviders(pcsw.Companies):
class CourseProviders(contacts.Companies):
    """
    List of Companies that have `Company.is_courseprovider` activated.
    """
    required_user_groups = ['integ']
    #~ required_user_level = UserLevel.manager
    #~ hide_details = [Contact]
    #~ use_as_default_table = False
    #~ app_label = 'courses'
    #~ label = _("Course providers")
    model = CourseProvider
    detail_layout = CourseProviderDetail()
    #~ known_values = dict(is_courseprovider=True)
    #~ filter = dict(is_courseprovider__exact=True)
    
    #~ def create_instance(self,req,**kw):
        #~ instance = super(CourseProviders,self).create_instance(req,**kw)
        #~ instance.is_courseprovider = True
        #~ return instance
            





#
# COURSE ENDINGS
#
#~ class CourseEnding(dd.Model):
    #~ u"""
    #~ Eine Kursbeendigung ist eine *Art und Weise, wie eine Kursanfrage beendet wurde*.
    #~ Später können wir dann Statistiken machen, wieviele Anfragen auf welche Art und 
    #~ Weise beendet wurden.
    #~ """
    #~ class Meta:
        #~ verbose_name = _("Course Ending")
        #~ verbose_name_plural = _('Course Endings')
        
    #~ name = models.CharField(_("designation"),max_length=200)
    
    #~ def __unicode__(self):
        #~ return unicode(self.name)
        
#~ class CourseEndings(dd.Table):
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    #~ model = CourseEnding
    #~ column_names = 'name *'
    #~ order_by = ['name']

  
class CourseContent(dd.Model):
    u"""
    Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)
    """
    
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
        
    name = models.CharField(max_length=200,
          blank=True,# null=True,
          verbose_name=_("Name"))
    u"""
    Bezeichnung des Kursinhalts (nach Konvention des DSBE).
    """
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class CourseContents(dd.Table):
    model = CourseContent
    order_by = ['name']
    detail_layout = """
    id name
    courses.CourseOffersByContent
    courses.CourseRequestsByContent
    """
    

class CourseOffer(dd.Model):
    """
    """
    class Meta:
        verbose_name = _("Course Offer")
        verbose_name_plural = _('Course Offers')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Name"))
    u"""
    Der Titel des Kurses. Maximal 200 Zeichen.
    """
    
    content = models.ForeignKey("courses.CourseContent")
    """
    Der Inhalt des Kurses (ein :class:`CourseContent`)
    """
    
    provider = models.ForeignKey('courses.CourseProvider')
    #~ provider = models.ForeignKey(CourseProvider,
        #~ verbose_name=_("Course provider"))
    #~ """
    #~ Der Kursanbieter (eine :class:`Company`)
    #~ """
    
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title,self.provider)
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().data_iterator
        
    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'candidates'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return settings.SITE.DEFAULT_LANGUAGE.django_code
        
        
    
class Course(dd.Model,mixins.Printable):
    u"""
    Ein konkreter Kurs, der an einem bestimmten Datum beginnt.
    Für jeden Kurs muss ein entsprechendes Angebot existieren, 
    das u.A. den :class:`Kursinhalt <CourseContent>` 
    und :class:`Kursanbieter <CourseProvider>` 
    detailliert. Also selbst für einen einmalig stattfindenden 
    Kurs muss ein Angebot erstellt werden.
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
        
    offer = models.ForeignKey("courses.CourseOffer")
    
    title = models.CharField(max_length=200,
        blank=True,
        verbose_name=_("Name"))
        
    start_date = models.DateField(_("start date"))
    
    #~ content = models.ForeignKey("courses.CourseContent",verbose_name=_("Course content"))
  
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung über diesen konkreten Kurs. Maximal 200 Zeichen.
    """
        
    def __unicode__(self):
        #~ s = u"%s %s (%s)" % (self._meta.verbose_name,self.pk,babel.dtos(self.start_date))
        s = dtos(self.start_date)
        if self.title:
            s += " " + self.title
        if self.offer:
            s += " " + unicode(self.offer)
        return s
  
    print_candidates = DirectPrintAction(
      label=_("List of candidates"),
      tplname='candidates')
    print_participants = DirectPrintAction(
      label=_("List of participants"),
      tplname='participants')
    
    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'candidates'))
        #~ rpt.add_action(DirectPrintAction('participants',_("List of participants"),'participants'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return settings.SITE.DEFAULT_LANGUAGE.django_code
        
    def participants(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die in diesem Kurs eingetragen sind. 
        """
        return ParticipantsByCourse.request(self).data_iterator
        
    def candidates(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage 
        kommen. 
        """
        return CandidatesByCourse.request(self).data_iterator
        

        
class Courses(dd.Table):
    required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = Course
    order_by = ['start_date']
    detail_layout = """
    id:8 start_date offer title 
    remark
    courses.ParticipantsByCourse
    courses.CandidatesByCourse
    """
    
class CoursesByOffer(Courses):
    master_key = 'offer'
    column_names = 'start_date * id'

class CourseOffers(dd.Table):
    required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = CourseOffer
    detail_layout = """
    id:8 title content provider
    description
    CoursesByOffer
    """
    
class CourseOffersByProvider(CourseOffers):
    master_key = 'provider'

class CourseOffersByContent(CourseOffers):
    master_key = 'content'



class CourseRequestStates(dd.Workflow):
    help_text = _("List of possible states of a Course Request")
    
    #~ @classmethod
    #~ def migrate(cls,old):
        #~ """
        #~ Used by :meth:`lino_welfare.modlib.pcsw.migrate.migrate_from_1_4_4`.
        #~ """
        #~ cv = {
          #~ None: 'candidate',
          #~ 1:'award',
          #~ 2:'passed',
          #~ 3:'failed',
          #~ 4:'aborted'
          #~ }
        #~ return getattr(cls,cv[old])
        #~ 
        
    #~ @classmethod
    #~ def allow_state_candidate(cls,self,user):
        #~ if self.course:
            #~ return True
        #~ return False
    
add = CourseRequestStates.add_item
add('10', _("Candidate"),"candidate") 
#~ add('10', _("Active"),"candidate") 
add('20', _("Registered"),"registered") 
add('30', _("Passed"),"passed")   # bestanden
add('40', _("Award"),"award")   # gut bestanden
add('50', pgettext_lazy(u"courses",u"Failed"),"failed")   # nicht bestanden
add('60', _("Aborted"),"aborted")   # abgebrochen
add('70', _("Inactive"),"inactive")


class RegisterCandidate(dd.ChangeStateAction):
    label = _("Register")
    required = dict(states=['candidate'])
    help_text = _("Register this candidate for this course.")

    def run_from_ui(self,obj,ar,**kw):
        assert isinstance(obj,CourseRequest)
        if ar.actor.master is Course and ar.master_instance is not None:
            obj.course = ar.master_instance
        if not obj.course:
            return ar.error(_("Cannot register to unknown course."),alert=True)
        kw = super(RegisterCandidate,self).run_from_ui(obj,ar,**kw)
        kw.update(refresh_all=True)
        kw.update(message=_("%(person)s has been registered to %(course)s") % dict(
                person=obj.person,course=obj.course))
        return kw
    
class UnRegisterCandidate(dd.ChangeStateAction):
    label = _("Unregister")
    required = dict(states=['registered'])
    help_text = _("Unregister this candidate from this course.")

    def run_from_ui(self,obj,ar,**kw):
        assert isinstance(obj,CourseRequest)
        course = obj.course
        obj.course = None
        kw = super(UnRegisterCandidate,self).run_from_ui(obj,ar,**kw)
        kw.update(refresh_all=True)
        kw.update(message=_("%(person)s has been unregistered from %(course)s") 
            % dict(person=obj.person,course=course))
        return kw
        
        
    
class CourseRequest(dd.Model):
    """
    A Course Request is created when a certain Person expresses her 
    wish to participate in a Course with a certain CourseContent.
    """
    workflow_state_field = 'state'
    
    class Meta:
        verbose_name = _("Course Requests")
        verbose_name_plural = _('Course Requests')
        
    person = models.ForeignKey("pcsw.Client",
        help_text="Le client qui désire suivre un cours.")
    
    offer = models.ForeignKey("courses.CourseOffer",blank=True,null=True)
    
    content = models.ForeignKey("courses.CourseContent",
        verbose_name=_("Course content"),
        help_text=u"Der gewünschte Kursinhalt.)")
    
    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"),
        help_text=_("When this request has been submitted."))
        #~ help_text=u"Das Datum, an dem die Anfrage erstellt wurde.")
    
    urgent = models.BooleanField(_("Needed for job search"),
        default=False,
        help_text=_("Check this if the request is needed for job search."))
        #~ help_text=u"Ankreuzen, wenn der Kurs für die Arbeitssuche benötigt wird.")
    
    #~ """Empty means 'any provider'
    #~ """
    #~ provider = models.ForeignKey(CourseProvider,blank=True,null=True,
        #~ verbose_name=_("Course provider"))
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset
        
    state = CourseRequestStates.field(default=CourseRequestStates.candidate)
        
    course = models.ForeignKey("courses.Course",blank=True,null=True,
        verbose_name=_("Course found"))
    u"""
    Der Kurs, durch den diese Anfrage befriedigt wurde.
    So lange dieses Feld leer ist, gilt die Anfrage als offen.
    """
        
    #~ """
    #~ The person's feedback about how satisfied she was.
    #~ """
    #~ satisfied = StrengthField(verbose_name=_("Satisfied"),blank=True,null=True)
    
    #~ remark = models.CharField(max_length=200,
    remark = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung zu dieser konkreten Kursanfrage oder -teilnahme.
    """
        
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    u"""
    Datum der effektives Beendigung dieser Kursteilname.
    """
    
    #~ ending = models.ForeignKey("courses.CourseEnding",blank=True,null=True,
        #~ verbose_name=_("Ending"))
    #~ u"""
    #~ Die Art der Beendigung 
    #~ (ein Objekt vom Typ :class:`CourseEnding`.)
    #~ Das wird benutzt für spätere Statistiken.
    #~ """
    
    def on_create(self,ar):
        self.date_submitted = datetime.date.today()
        super(CourseRequest,self).on_create(ar)

    def save(self,*args,**kw):
        if self.offer and self.offer.content:
            self.content = self.offer.content
        super(CourseRequest,self).save(*args,**kw)
        
    @chooser()
    def offer_choices(cls,content):
        if content:
            return CourseOffer.objects.filter(content=content)
        return CourseOffer.objects.all()
    
    def before_state_change(self,ar,kw,old,new):
        if new.name in ('passed','award','failed','aborted'):
            if not self.date_ended:
                self.date_ended = datetime.date.today()
      
    def get_row_permission(self,ar,state,ba):
        if not super(CourseRequest,self).get_row_permission(ar,state,ba):
            #~ if ba.action.action_name == 'wf7':
                #~ logger.info('20130424 courses.CourseRequest.get_row_permission() %r super said no',ba)
            return False
        if isinstance(ba.action,RegisterCandidate):
            if ar.actor.master is not Course or ar.master_instance is None:
                return False
        return True
        
        
class CourseRequests(dd.Table):
    #~ debug_permissions = 20130424
    model = CourseRequest
    required=dict(user_groups=['integ'],user_level='manager')
    detail_layout = """
    date_submitted person content offer urgent 
    course state date_ended id:8 
    remark  uploads.UploadsByController 
    """
    order_by = ['date_submitted']
    active_fields = ['offer']

class CourseRequestsByPerson(CourseRequests):
    """
    Table of :class:`CourseRequest` instances of a 
    :class:`lino.modlib.pcsw.models.Client`.
    """
    required=dict(user_groups=['integ'])
    master_key = 'person'
    column_names = 'date_submitted:10 content:15 offer:15 course:20 urgent state date_ended remark:15 id'
    hidden_columns = 'id'
    auto_fit_column_widths = True
    

class CourseRequestsByContent(CourseRequests):
    required=dict(user_groups=['integ'])
    master_key = 'content'
        
class RequestsByCourse(CourseRequests):
    """
    Table of :class:`CourseRequest` instances of a :class:`Course`.
    """
    required=dict(user_groups=['integ'])
    master_key = 'course'
  
    @classmethod
    def create_instance(self,req,**kw):
        obj = super(RequestsByCourse,self).create_instance(req,**kw)
        if obj.course is not None:
            obj.content = obj.course.offer.content
        return obj
        

class ParticipantsByCourse(RequestsByCourse):
    """
    List of participating candidates for the given :class:`Course`.
    """
    label = _("Participants")
    column_names = 'person remark:20 date_ended state workflow_buttons:60'
    #~ do_unregister = UnregisterCandidate()
    
    #~ @dd.action(_("Passed"),required=dict(states=['registered']))
    #~ def passed(self,ar):
        #~ self.state = CourseRequestStates.passed
        #~ if not self.date_ended:
            #~ self.date_ended = datetime.date.today()
        #~ self.save()
        #~ return ar.success_response(refresh=True,
          #~ message=_("%(person)s passed %(course)s") 
            #~ % dict(person=self.person,course=self.course))
            
    #~ @dd.action(pgettext_lazy(u"courses",u"Failed"),required=dict(states=['registered']))
    #~ def failed(self,ar):
        #~ self.state = CourseRequestStates.failed
        #~ if not self.date_ended:
            #~ self.date_ended = datetime.date.today()
        #~ self.save()
        #~ return ar.success_response(refresh=True,
          #~ message=_("%(person)s failed in %(course)s") 
            #~ % dict(person=self.person,course=self.course))
            
    #~ @dd.action(_("Aborted"),required=dict(states=['registered']))
    #~ def aborted(self,ar):
        #~ self.state = CourseRequestStates.aborted
        #~ self.save()
        #~ return ar.success_response(refresh=True,
          #~ message=_("%(person)s aborted from %(course)s") 
            #~ % dict(person=self.person,course=self.course))
            
    #~ @dd.action(_("Unregister"),required=dict(states=['registered']))
    #~ def unregister(self,ar):
        #~ """
        #~ Unregister the given :class:`Candidate` for the given :class:`Course`.
        #~ This action is available on a row of :class:`ParticipantsByCourse`.
        #~ """
        #~ course = self.course
        #~ self.state = CourseRequestStates.candidate
        #~ self.course = None
        #~ self.save()
        #~ return ar.success_response(refresh_all=True,
          #~ message=_("%(person)s has been unregistered from %(course)s") 
            #~ % dict(person=self.person,course=course))
    
    

class CandidatesByCourse(RequestsByCourse):
    """
    List of :class:`Candidates <Candidate>` for the given :class:`Course`
    which are not registiered.
    """
    label = _("Candidates")
    column_names = 'person remark:20 date_submitted state workflow_buttons:60 content'
    
    
    #~ @dd.action(_("Register"),required=dict(states=['candidate']))
    #~ def register(self,ar):
        #~ """
        #~ Register the given :class:`Candidate` for the given :class:`Course`.
        #~ This action is available on a row of :class:`CandidatesByCourse`.
        #~ """
        #~ if ar.master_instance is not None:
            #~ self.course = ar.master_instance
        #~ if not self.course:
            #~ return ar.error.response(_("Cannot register to unknown course."))
        #~ self.state = CourseRequestStates.registered
        #~ self.save()
        #~ return ar.success_response(refresh_all=True,
            #~ message=_("%(person)s has been registered to %(course)s") % dict(
                #~ person=self.person,course=self.course))
        
    
    @classmethod
    def get_request_queryset(self,rr):
        if rr.master_instance is None:
            return []
        return self.model.objects.filter(course__isnull=True,
            state=CourseRequestStates.candidate,
            content=rr.master_instance.offer.content)
    
    @classmethod
    def create_instance(self,req,**kw):
        """Manually clear the `course` field.
        """
        obj = super(CandidatesByCourse,self).create_instance(req,**kw)
        obj.course = None
        return obj

CLIENTS_TABLE = pcsw.Clients

class PendingCourseRequests(CourseRequests):
    """
    List of pending course requests.
    """
    required = dict(user_groups=['integ'])
    label = _("Pending Course Requests")
    order_by = ['date_submitted']
    filter = models.Q(course__isnull=True)
    parameters = dict(
        request_state = CourseRequestStates.field(blank=True),
        course_content = models.ForeignKey("courses.CourseContent",blank=True),
        course_provider = models.ForeignKey('courses.CourseProvider',blank=True),
        **CLIENTS_TABLE.parameters)
    params_layout = CLIENTS_TABLE.params_layout + """\
    request_state course_content course_provider
    """
    
    
    @classmethod
    def setup_columns(self):
        """
        Builds columns dynamically for the different age slices.
        Called when kernel setup is done, 
        before the UI handle is being instantiated.
        """
        self.column_names = 'date_submitted workflow_buttons:30 person age '
        self.column_names += 'address person__gsm person__phone person__coaches '
        #~ self.column_names += 'address person__gsm person__phone person__coach1 person__coach2 '
        #~ self.column_names += 'person__address_column person__age ' 
        self.column_names += 'content urgent remark'
        age_slices = [(16,24), (25,30), (31,40), (41,50),(51,60),(61,None)]
        for sl in age_slices:
            if sl[1] is None:
                label = ">%d" % sl[0]
            else:
                label = "%d-%d" % sl

            def w(sl):
                def func(self,obj,ar):
                    if obj._age_in_years is None: return None
                    if obj._age_in_years < sl[0]: return None
                    if obj._age_in_years > sl[1]: return None
                    return 1
                return func
            vf = dd.VirtualField(models.IntegerField(label),w(sl))
            self.add_virtual_field('a'+str(sl[0]),vf)
            self.column_names += ' ' + vf.name+':5'
                
        self.column_names += ' ax'
    
        
    @classmethod
    def get_data_rows(self,ar):
        #~ qs = super(PendingCourseRequests,self).get_request_queryset(ar)
        qs = self.get_request_queryset(ar)
        for obj in qs:
            age = obj.person.get_age_years()
            if age is not None: age = age.days / 365
            obj._age_in_years = age
            yield obj
            
    editable = True
    

    @dd.virtualfield(models.IntegerField(_("Age")))
    def age(self,obj,request):
        return obj._age_in_years
    
    @dd.displayfield(_("Address"))
    def address(self,obj,ar):
        return obj.person.address_location(', ')
        
    #~ @dd.displayfield(_("Age"))
    #~ def age(self,obj,request):
        #~ if obj._age_in_years is None: return ''
        #~ return str(obj._age_in_years)
        
    #~ @dd.virtualfield(models.BooleanField(_("unknown age")))
    @dd.virtualfield(models.IntegerField(_("unknown age")))
    def ax(self,obj,request):
        if obj._age_in_years is None: return 1
        return 0
        #~ return obj._age_in_years is None
        
    @classmethod
    def get_request_queryset(self,ar):
        #~ raise Exception(20130424)
        qs = super(PendingCourseRequests,self).get_request_queryset(ar)
        clients_qs = CLIENTS_TABLE.get_request_queryset(ar)
        #~ print 20130424, clients_qs
        qs = qs.filter(person__in=clients_qs)
        if ar.param_values.request_state:
            qs = qs.filter(state=ar.param_values.request_state)
        if ar.param_values.course_content:
            qs = qs.filter(content=ar.param_values.course_content)
        if ar.param_values.course_provider:
            qs = qs.filter(provider=ar.param_values.course_provider)
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        if ar.param_values.request_state:
            yield unicode(ar.param_values.request_state)
        if ar.param_values.course_content:
            yield unicode(ar.param_values.course_content)
        if ar.param_values.course_provider:
            yield unicode(ar.param_values.course_provider)
        for t in super(PendingCourseRequests,self).get_title_tags(ar):
            yield t
        for t in CLIENTS_TABLE.get_title_tags(ar):
            yield t
            
        
MODULE_LABEL = _("Courses")
        
def site_setup(self): pass
    
def setup_main_menu(site,ui,profile,m):
    if profile.integ_level:
        m = m.add_menu("courses",MODULE_LABEL)
        m.add_action(CourseProviders)
        m.add_action(CourseOffers)
        m.add_action(PendingCourseRequests)
            
  
def setup_master_menu(site,ui,profile,m): pass
def setup_my_menu(site,ui,profile,m): pass
def setup_config_menu(site,ui,profile,m):
    m = m.add_menu("courses",MODULE_LABEL)
    m.add_action(CourseContents)
    #~ m.add_action(CourseEndings)
            
  
def setup_explorer_menu(site,ui,profile,m):
    m = m.add_menu("courses",MODULE_LABEL)
    m.add_action(Courses)
    m.add_action(CourseRequests)
            
            
def setup_workflows(site):

    CourseRequestStates.registered.add_transition(RegisterCandidate)
    CourseRequestStates.candidate.add_transition(UnRegisterCandidate)
    CourseRequestStates.passed.add_transition(states="registered")
    CourseRequestStates.failed.add_transition(states="registered")
    CourseRequestStates.aborted.add_transition(states="registered")
    
    CourseRequestStates.inactive.add_transition(states="candidate")
    CourseRequestStates.candidate.add_transition(states="inactive")
        #~ debug_permissions = 20130424)
    
