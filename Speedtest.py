# -*- coding: utf-8-*-
# vim: set expandtab:ts=4:sw=4:ft=python
import re
import subprocess
import urllib
from datetime import datetime

WORDS = ["SPEEDTEST", "SPEED", "TEST"]
PRIORITY = 3


def send_mail(profile, subject, text, files=None):
    try:
        if 'mailgun' in profile:
            user = profile['mailgun']['username']
            password = profile['mailgun']['password']
            server = 'smtp.mailgun.org'
        else:
            user = profile['gmail_address']
            password = profile['gmail_password']
            server = 'smtp.gmail.com'
    except:
        pass

    send_to = profile['speedtest']['email']
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    session = smtplib.SMTP(server, 587)
    session.starttls()
    session.login(user, password)
    session.sendmail(user, send_to, msg.as_string())
    session.quit()


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by performing a
        speedtest.net analysis and sending the resulting image to users
        email.
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    mic.say("Okay, this will only take a minute.")

    ## call the speedtest-cli command
    p = subprocess.Popen(["speedtest", "--simple", "--share"],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()

    ## Wait for it to terminate. Get return returncode
    p_status = p.wait()

    upload = ''
    download = ''
    filename = ''
    speedtest_url = ''
    for line in output.splitlines():
        if line.startswith('Download: '):
            download = line
        elif line.startswith('Upload: '):
            upload = line
        elif line.startswith('Share results: '):
            filename = '/tmp/speedtest-%s.png' % datetime.now().strftime('%Y-%m-%d.%H:%M:%S.%f')
            speedtest_url = line.replace('Share results: ', '')
            urllib.urlretrieve(speedtest_url, filename)

    if upload == '' or download == '' or speedtest_url == '' or filename == '':
        return mic.say("There was an error executing speedtest")

    mic.say(upload.replace(': ', ' speed is ').replace('Mbit/s', 'megabits per second.'))
    mic.say(download.replace(': ', ' speed is ').replace('Mbit/s', 'megabits per second.'))
    message = "\n".join([upload, download, speedtest_url])
    send_mail(profile, 'SpeedTest.Net Results', message, [filename])


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.
        Arguments:
        text -- user-input, typically transcribed speech
    """

    regex = "(" + "|".join(WORDS) + ")"
    return bool(re.search(regex, text, re.IGNORECASE))


