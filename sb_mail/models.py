# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
import importlib
from django.template import Template, Context
from django.core.mail import send_mass_mail, send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import operator
from django.contrib.auth.models import Group
import smtplib
from django.shortcuts import render

# Create your models here.

type_choices = (
    ('In', 'In'),
    ('Out', 'Out'),
)
choices = (
    ('plain', 'plain'),
    ('Html', 'HTML'),
)


class sb_mail_server(models.Model):
    auth_choices = (
        ('SSL', 'SSL'),
        ('TLS', 'TLS    '),
        ('TTL', 'TTL'),
    )
    state_choices = (
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
    )
    server_type_choices = (
        ('POP', 'POP'),
        ('IMAP', 'IMAP'),
        ('SMTP', 'SMTP'),
    )

    name = models.CharField(max_length=20)
    server = models.CharField(max_length=30)
    port = models.IntegerField(null=True)
    auth_type = models.CharField(max_length=10, choices=auth_choices)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=10, choices=type_choices, default='In', editable=False)
    state = models.CharField(max_length=10, choices=state_choices)
    server_type = models.CharField(max_length=10, choices=server_type_choices)
    priority = models.IntegerField(null=True)
    keep_attachment = models.BooleanField(default=True)

    def send(self):
        return 1

    def receive(self):
        return 1

    def test_connection(self):
        print ("connection testing code.")
        return 1

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'In Server'
        verbose_name_plural = 'In Servers'


class mail_server(sb_mail_server):

    def save(self, *args, **kwargs):
        self.type = 'Out'
        super(sb_mail_server, self).save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Out Server'


class mail_message(models.Model):
    status_choices = (
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Queue', 'Queue'),
    )
    priority_choices = (
        ('Urgent', 'Urgent'),
        ('Normal', 'Normal'),
        ('Low', 'Low'),
    )
    to_email = models.CharField("To Email", max_length=100, null=True)
    from_email = models.CharField("From Email", max_length=100, null=True)
    cc_email = models.CharField("CC Email", max_length=100, null=True)
    bbc_email = models.CharField("BBC Email", max_length=100, null=True)
    subject = models.CharField("Subject", max_length=100, null=True)
    body_text = models.TextField("Body Text", max_length=2000, null=True)
    body_html = models.TextField("Body Html", max_length=2000, null=True)
    type = models.CharField("Type", max_length=10, choices=type_choices, null=True)
    object_package = models.CharField("Object Package", max_length=90, null=True)
    object = models.CharField("Object", max_length=90, null=True)
    object_id = models.CharField("Object ID", max_length=90, null=True)
    mailserver_id = models.ForeignKey(sb_mail_server, verbose_name="Mail Server ID", blank=True, null=True)
    status = models.CharField("Status", max_length=10, choices=status_choices, null=True)
    priority = models.CharField("Priority", max_length=10, choices=priority_choices, null=True)
    text_type = models.CharField("Choices", max_length=10, choices=choices, null=True)

    def _send(self, context={}):

        mail_id = self.mailserver_id.login
        mail_password = self.mailserver_id.password

        server = smtplib.SMTP(self.mailserver_id.server, self.mailserver_id.port)

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = mail_id
        msg['To'] = self.to_email
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(self.body_html.encode('utf-8') if self.text_type == 'Html' else self.body_text.encode('utf-8'),
                         self.text_type, 'utf-8')

        msg.attach(part1)
        server.starttls()
        server.login(mail_id, mail_password)
        try:
            server.sendmail(mail_id, self.to_email, msg.as_string())
        except:
            mail_message.objects.filter(object=self.object).update(status="Sent", type="Out")
            return 1
        server.quit()
        if context['priority']:
            mail_message.objects.filter(object=self.object).update(status="Sent", priority=context['priority'],
                                                                   type="Out")
        else:
            mail_message.objects.filter(object=self.object).update(status="Sent", type="Out")
        return 1

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class sbmail_template(models.Model):
    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    name = models.CharField("Name", max_length=30)
    to_email = models.CharField("To Email", max_length=100)
    from_email = models.CharField("From Email", max_length=100)
    cc_email = models.CharField("CC Email", max_length=100)
    bbc_email = models.CharField("BBC Email", max_length=100)
    subject = models.CharField("Subject", max_length=100)
    body_text = models.TextField("Body Text", max_length=2000)
    body_html = models.TextField("Body Html", max_length=2000)
    type = models.CharField("Type", max_length=10, choices=choices)
    object_package = models.CharField("Object Package", max_length=90)
    object = models.CharField("Object", max_length=90)
    mailserver_id = models.ForeignKey(sb_mail_server, verbose_name="Mail Server ID", blank=True, null=True)

    def __unicode__(self):
        return self.name

    def send(self, object_id, context={}, quick=False):
        # FIRST TAKE TEMPLATE AND PARSE AND GET MAIL BODY
        # mail_body = self.parse_template()
        # __model =  globals()[self.object]             #CREATE CLASS
        # __model = getattr(importlib.import_module(self.object_package), self.object)
        pkg = importlib.import_module(self.object_package)
        __model = getattr(pkg, self.object)
        obj = __model.objects.get(id=object_id)  # CREATE OBJECT / INSTANCE

        if obj:
            html_code = self._parse(self.body_html if self.type == 'Html' else self.body_text, obj, context=context)
            to_email = self._parse(self.to_email, obj, context=context)
            from_email = self._parse(self.from_email, obj, context=context)
            cc_email = self._parse(self.cc_email, obj, context=context)
            bbc_email = self._parse(self.bbc_email, obj, context=context)
            subject = self._parse(self.subject, obj, context=context)
            name = self._parse(self.name, obj, context=context)
            body_text = self._parse(self.body_text, obj, context=context)
            body_html = self._parse(self.body_html, obj, context=context)
            # type = self._parse(self.type, obj, context=context)

            object_package = self._parse(self.object_package, obj, context=context)
            object = self._parse(self.object, obj, context=context)

            obj_data = {'html_code': html_code, 'to_email': to_email, 'from_email': from_email, 'subject': subject,
                        'object': object, 'type': self.type}
            mail_message.objects.create(to_email=to_email, from_email=from_email, cc_email=cc_email,
                                        bbc_email=bbc_email, subject=subject, body_text=body_text, body_html=body_html,
                                        text_type=self.type, object_package=object_package, object=object,
                                        object_id=object_id, status="Queue", mailserver_id=self.mailserver_id,
                                        priority=context['priority'])
            # data = self._send(context,obj_data)

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            # filename = "NAME OF THE FILE WITH ITS EXTENSION"
            # attachment = open("PATH OF THE FILE", "rb")
            # print msg.as_string()
            # part2 = MIMEBase('application', 'octet-stream')
            # part2.set_payload((attachment).read())
            # encoders.encode_base64(part2)
            # part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # msg.attach(part2)

            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.

            # message1 = (subject, html_code,from_email,to_email)
            # message2 = (subject, html_code,from_email,to_email)
            # mail = send_mass_mail((message1, message2), fail_silently=False)
            # send_mail(subject,html_code,[from_email],[to_email],fail_silently=False)

            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server.login(self.mailserver_id.login, self.mailserver_id.password)
            # msg = "YOUR MESSAGE!"
            # server.sendmail(self.mailserver_id.login, to_email, msg)
            # server.quit()

        # NOW PARSE EMAIL OTHER FIELDS LIKE TO-MAIL, FROM-MAIL, SUBJECT AND OTHER.

        # THAN LAST WRITE CODE TO SEND AN EMAIL AS FINAl AND RETURN IT SUCCES OR FAIL AS RETURN VALUE.

        return 1

    def _send(self, context, data):

        mail_id = self.mailserver_id.login
        mail_password = self.mailserver_id.password

        server = smtplib.SMTP(self.mailserver_id.server, self.mailserver_id.port)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = data['subject']
        msg['From'] = mail_id
        msg['To'] = data['to_email']

        part1 = MIMEText(data['html_code'].encode('utf-8'), data['type'], 'utf-8')
        msg.attach(part1)

        server.starttls()
        server.login(mail_id, mail_password)
        try:
            server.sendmail(mail_id, data['to_email'], msg.as_string())
        except:
            message = 'Mail Delivery Failed.Please Try After Some time.'
            return message
        server.quit()
        if context['priority']:
            mail_message.objects.filter(object=data['object']).update(status="Sent", priority=context['priority'],
                                                                      type="Out")
        else:
            mail_message.objects.filter(object=data['object']).update(status="Sent", type="Out")

        return 1

    def _parse(self, raw_template, obj, context):
        t = Template(raw_template)
        c = Context({"object": obj, "context": context})
        return t.render(c)

    def quick_send(self):
        return 1

    def parse_template(self):
        # NO USE RIGHT NOW, WILL REFINE LATER ONCE SEND FUNCTION DONE.
        return 1

    def add_attachment(self):
        return 1


class Email_Subscription(models.Model):
    name = models.CharField("Name", max_length=40, blank=True, null=True)
    email = models.EmailField("Email", max_length=50)
    active = models.BooleanField("Active", default=True)
    subcription_datetime = models.DateTimeField("Subscription Time", default=timezone.now, blank=True)
    unsubcription_datetime = models.DateTimeField("Unsubscription Time", null=True, blank=True)
    unsubcription_reason = models.CharField("Unsubscription Reason", max_length=100, blank=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class mail_message_attachment(models.Model):
    mail_message_id = models.ForeignKey(mail_message, verbose_name="Mail Message ID", null=True)
    title = models.CharField("Title", max_length=90, null=True)
    file = models.FileField("File", upload_to='files', null=True)
    time = models.DateTimeField("Attachment Time", null=True)

    class Meta:
        verbose_name = 'Message Attachment'
        verbose_name_plural = 'Message Attachments'


class sb_settings(models.Model):
    signup_group = models.ManyToManyField(Group, verbose_name="Groups")
    support_email = models.EmailField('Email', max_length=50)
    rank = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Group Settings"
        ordering = ('id',)
