Jasper-Module-Speedtest
======================

Jasper Speedtest Module which allows you to run speedtest.net tests and sends you the report to your email.

##Steps to install Speedtest Module

* Install the `speedtest-cli` package via pip:
```
sudo pip install speedtest-cli
```
* run the following commands in order:
```
git clone https://github.com/ArtBIT/jasper-module-speedtest.git
cp jasper-module-speedtest/Speedtest.py <path to jasper/client/modules>
#i.e. cp jasper-module-speedtest/Speedtest.py /usr/local/lib/jasper/client/modules/
```
* Edit `~/.jasper/profile.yml` and add the following at the bottom:
```
speedtest:
  email: 'email.to.send.reports.to@whatever.com'
```
* Make sure you have [mailgun](http://jasperproject.github.io/documentation/configuration/#mailgun) or gmail account set-up for Jasper.
* Restart the Pi:
```
sudo reboot
```
##Congrats, JASPER Speedtest Module is now installed and ready for use.
Here are some examples:
```
YOU: Speedtest
JASPER: Okay, this will only take a minute. *runs the test and reports the upload/download speeds back to you*
```

