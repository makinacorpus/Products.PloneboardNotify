import smtplib

from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate

#from Products.Archetypes import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

def _getAllValidEmailsFromGroup(putils, acl_users, group):
    """Look at every user in the group, return all valid emails"""
    return [m.getProperty('email') for m in group.getGroupMembers() if putils.validateSingleEmailAddress(m.getProperty('email'))]

def _getSendToValues(object):
    """Load the portal configuration for the notify system and obtain a list of emails.
    If the sendto_all is True, the mail will be sent to all members of the Plone site.
    The sendto_values value is used to look for name of groups, then name on users in the portal and finally for normal emails.
    @return a list of emails
    """
    ploneboard_notify_properties = getToolByName(object,'portal_properties')['ploneboard_notify_properties']
    sendto_all = ploneboard_notify_properties.sendto_all
    sendto_values = ploneboard_notify_properties.sendto_values
    acl_users = getToolByName(object, 'acl_users')
    putils = getToolByName(object, 'plone_utils')

    emails = []
    if sendto_all:
        users = acl_users.getUsers()
        emails.extend([m.getProperty('email') for m in users if putils.validateSingleEmailAddress(m.getProperty('email'))])
    for entry in sendto_values:
        group = acl_users.getGroupById(entry)
        # 1 - is a group?
        if group:
            emails.extend(_getAllValidEmailsFromGroup(putils, acl_users, group))
            continue
        # 2 - is a member?
        user = acl_users.getUserById(entry)
        if user:
            email = user.getProperty('email')
            if putils.validateSingleEmailAddress(email):
                emails.append(email)
            continue
        # 3 - is a valid email address?
        if putils.validateSingleEmailAddress(entry):
            emails.append(entry)

    return emails

def SendMail(object, event):
    """A Zope3 event for sending emails"""
    portal = getToolByName(object,"portal_url").getPortalObject()

    send_from = portal.getProperty('email_from_address')
    if type(send_from)==tuple and send_from:
        send_from = send_from[0]
       
    send_to = _getSendToValues(object)
    
    translation_service = getToolByName(object,'translation_service')
    
    #subject = _(u'A new message has been added on the forum ') + ('"%s"' % object.aq_parent.Title())
    #text = _("The new message is:<br />") + object.REQUEST.form['text']
    
    msg_sbj = u"New message added on the forum "
    subject = translation_service.utranslate(domain='plone',
                                             msgid=msg_sbj,
                                             default=msg_sbj,
                                             context=object)
    subject+= object.aq_parent.Title().decode('utf-8')

    msg_txt = u"The new message is:"
    text = translation_service.utranslate(domain='plone',
                                          msgid=msg_txt,
                                          default=msg_txt,
                                          context=object)
    text += "<br/>" + object.REQUEST.form['text'].decode('utf-8')
    text += "<hr/>" + object.absolute_url()

    server = portal.MailHost.smtp_host
    header_charset = 'ISO-8859-1'
    body_charset = 'utf-8'
    #msg = MIMEText(text, 'html')
    msg = MIMEText(text.encode(body_charset), 'html', body_charset)
    msg.set_charset(body_charset)
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(unicode(subject), header_charset)

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, set(send_to), msg.as_string())
        smtp.close()
    except Exception, inst:
        putils = getToolByName(object,'plone_utils')
        putils.addPortalMessage('Not able to send notifications', type='warning')
        object.plone_log(str(inst))



