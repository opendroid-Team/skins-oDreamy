# -*- coding: UTF-8 -*-
# Weather by m43c0 
# Last modified 28-10-2013
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Label import Label
from Components.Pixmap import Pixmap
from Tools.Directories import fileExists
from urllib import quote
from urllib2 import Request, urlopen, URLError, HTTPError
from xml.dom import minidom, Node
from enigma import loadPic, eTimer, gFont, addFont

try:
    from Search_Id import *	
except:
    pass
	
def FontWeather(file, name, scale, replacement):
	try:
		addFont(file, name, scale, replacement)
	except Exception, ex:
		addFont(file, name, scale, replacement, 0)				
FontWeather("/usr/lib/enigma2/python/Plugins/Extensions/Weather/Font/weather.ttf", "weather", 100, False)
	
import gettext
def _(txt):
	t = gettext.dgettext("Weather", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
	
class MeteoMain(Screen):
 
    def __init__(self, session):
        path = "/usr/lib/enigma2/python/Plugins/Extensions/Weather/Skin/Weather.xml" 
        with open(path, "r") as f:
		self.skin = f.read()
		f.close() 	         	
        Screen.__init__(self, session)		
        self['lab1'] = Label(_('Retrieving data ...'))
        self['lab1b'] = Label('')
        self['lab2'] = Label('')
        self['lab3'] = Label('')
        self['lab4'] = Label('')
        self['lab4b'] = Label('')
        self['lab5'] = Pixmap()
        self['lab6'] = Label('')
        self['lab7'] = Label('')
        self['lab7b'] = Label('')
        self['lab8'] = Label('')
        self['lab8b'] = Label('')
        self['lab9'] = Label('')
        self['lab9b'] = Label('')
        self['lab10'] = Label('')
        self['lab10b'] = Label('')
        self['lab11'] = Label('')
        self['lab11b'] = Label('')
        self['lab12'] = Label('')
        self['lab12b'] = Label('')
        self['lab13'] = Label('')
        self['lab14'] = Label('')
        self['lab14b'] = Label('')
        self['lab15'] = Label('')
        self['lab15b'] = Label('')
        self['lab16'] = Label('')
        self['lab17'] = Pixmap()
        self['lab18'] = Label('')
        self['lab19'] = Label('')
        self['lab19b'] = Label('')
        self['lab20'] = Label('')
        self['lab20b'] = Label('')
        self['lab21'] = Label('')
        self['lab22'] = Pixmap()
        self['lab23'] = Label('')
        self['lab24'] = Label('')
        self['lab24b'] = Label('')
        self['lab25'] = Label('')
        self['lab25b'] = Label('')
        self['lab26'] = Label('')
        self['lab26b'] = Label('')
        self['lab27'] = Label('')
        self['lab27b'] = Label('')
        self['lab28'] = Pixmap()
        self['lab28a'] = Label('')
        self['lab28b'] = Label('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {
         'red': self.key_red,
         'back': self.close,
         'ok': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.startConnection)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)
        self.bhv = 2

    def startShow(self):
        self.activityTimer.start(10)

    def startConnection(self):
        self.activityTimer.stop()
        self.updateInfo()

    def updateInfo(self):
        myurl = self.get_Url()
        req = Request(myurl)
        try:
            handler = urlopen(req)
        except HTTPError as e:
            maintext = 'Error: connection failed !'
        except URLError as e:
            maintext = 'Error: Page not available !'
        else:
            dom = minidom.parse(handler)
            handler.close()
            maintext = ''
            tmptext = ''	
            if dom:
                weather_data = {}
                weather_data['title'] = dom.getElementsByTagName('title')[0].firstChild.data
                txt = str(weather_data['title'])
                if txt.find('Error') != -1 or self.bhv < 2:
                    self['lab1'].setText(_('Sorry, wrong WOEID'))
                    return
                ns_data_structure = {'location': ('city', 'region', 'country'),
                 'units': ('temperature', 'distance', 'pressure', 'speed'),
                 'wind': ('chill', 'direction', 'speed'),
                 'atmosphere': ('humidity', 'visibility', 'pressure', 'rising'),
                 'astronomy': ('sunrise', 'sunset'),
                 'condition': ('text', 'code', 'temp', 'date')}
                for tag, attrs in ns_data_structure.items():
                    weather_data[tag] = self.xml_get_ns_yahoo_tag(dom, 'http://xml.weather.yahoo.com/ns/rss/1.0', tag, attrs)

                weather_data['geo'] = {}
                weather_data['geo']['lat'] = dom.getElementsByTagName('geo:lat')[0].firstChild.data
                weather_data['geo']['long'] = dom.getElementsByTagName('geo:long')[0].firstChild.data
                weather_data['condition']['title'] = dom.getElementsByTagName('item')[0].getElementsByTagName('title')[0].firstChild.data
                weather_data['html_description'] = dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].firstChild.data
                forecasts = []
                for forecast in dom.getElementsByTagNameNS('http://xml.weather.yahoo.com/ns/rss/1.0', 'forecast'):
                    forecasts.append(self.xml_get_attrs(forecast, ('day', 'date', 'low', 'high', 'text', 'code')))

                weather_data['forecasts'] = forecasts
                dom.unlink()
                maintext = 'Data provider: '
                self['lab1b'].setText(_('Yahoo Weather'))
                city = '%s' % str(weather_data['location']['city'])
                self['lab2'].setText(city)
                txt = str(weather_data['condition']['date'])
                parts = txt.strip().split(' ')
                txt = _('Last Updated:')+' %s %s %s %s %s' % (parts[1],
                 parts[2],
                 parts[3],
                 parts[4],
                 parts[5])
                self['lab3'].setText(txt)
                txt = str(weather_data['condition']['temp'])
                self['lab4'].setText(txt)
                self['lab4b'].setText('\xc2\xb0C')
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/Icon/%s.png' % str(weather_data['condition']['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 220, 195, 0, 0, 0, 0)
                self['lab5'].instance.setPixmap(png)
                txt = str(weather_data['condition']['text'])
                self['lab6'].setText(txt)
                self['lab7'].setText(_('Humidity   :'))
                txt = str(weather_data['atmosphere']['humidity']) + ' %'
                self['lab7b'].setText(txt)
                self['lab8'].setText(_('Pressure   :'))
                txt = str(weather_data['atmosphere']['pressure']) + ' mb'
                self['lab8b'].setText(txt)
                self['lab9'].setText(_('Visibility :'))
                txt = str(weather_data['atmosphere']['visibility']) + ' km'
                self['lab9b'].setText(txt)
                self['lab10'].setText(_('Sunrise    :'))
                txt = str(weather_data['astronomy']['sunrise'])
                self['lab10b'].setText(txt)
                self['lab11'].setText(_('Sunset     :'))
                txt = str(weather_data['astronomy']['sunset'])
                self['lab11b'].setText(txt)
                self['lab12'].setText(_('Wind       :'))
                direction = self.wind_direction(str(weather_data['wind']['direction']))
                txt = _('From')+' %s at %s kmh' % (direction, str(weather_data['wind']['speed']))
                self['lab12b'].setText(txt)
                txt = self.extend_day(str(weather_data['forecasts'][0]['day']))
                self['lab13'].setText(txt)
                self['lab14'].setText(_('High :'))
                txt = str(weather_data['forecasts'][0]['high']) + '\xc2\xb0C'
                self['lab14b'].setText(txt)
                self['lab15'].setText(_('Low :'))
                txt = str(weather_data['forecasts'][0]['low']) + '\xc2\xb0C'
                self['lab15b'].setText(txt)
                txt = str(weather_data['forecasts'][0]['text'])
                self['lab16'].setText(txt)
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/Icon/%s.png' % str(weather_data['forecasts'][0]['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 150, 133, 0, 0, 0, 0)
                self['lab17'].instance.setPixmap(png)
                txt = self.extend_day(str(weather_data['forecasts'][1]['day']))
                self['lab18'].setText(txt)
                self['lab19'].setText(_('High :'))
                txt = str(weather_data['forecasts'][1]['high']) + '\xc2\xb0C'
                self['lab19b'].setText(txt)
                self['lab20'].setText(_('Low :'))
                txt = str(weather_data['forecasts'][1]['low']) + '\xc2\xb0C'
                self['lab20b'].setText(txt)
                txt = str(weather_data['forecasts'][1]['text'])
                self['lab21'].setText(txt)
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/Icon/%s.png' % str(weather_data['forecasts'][1]['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 150, 133, 0, 0, 0, 0)
                self['lab22'].instance.setPixmap(png)
                self['lab23'].setText(city)
                self['lab24'].setText(_('Latitude :'))
                txt = str(weather_data['geo']['lat']) + '\xc2\xb0'
                self['lab24b'].setText(txt)
                self['lab25'].setText(_('Longitude :'))
                txt = str(weather_data['geo']['long']) + '\xc2\xb0'
                self['lab25b'].setText(txt)
                self['lab26'].setText(_('Region    :'))
                txt = str(weather_data['location']['region'])
                self['lab26b'].setText(txt)
                self['lab27'].setText(_('Country   :'))
                txt = str(weather_data['location']['country'])
                self['lab27b'].setText(txt)
                myicon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/Skin/1color.png'
                png = loadPic(myicon, 250, 30, 0, 0, 0, 0)
                self['lab28'].instance.setPixmap(png)
                self['lab28a'].setText(':')
                self['lab28b'].setText(_('Change city'))
            else:
                maintext = 'Error getting XML document!'

        self['lab1'].setText(maintext)

    def xml_get_ns_yahoo_tag(self, dom, ns, tag, attrs):
        element = dom.getElementsByTagNameNS(ns, tag)[0]
        return self.xml_get_attrs(element, attrs)

    def xml_get_attrs(self, xml_element, attrs):
        result = {}
        for attr in attrs:
            result[attr] = xml_element.getAttribute(attr)

        return result

    def wind_direction(self, degrees):
        try:
            degrees = int(degrees)
        except ValueError:
            return ''

        if degrees < 23 or degrees >= 338:
            return 'North'
        if degrees < 68:
            return 'NEast'
        if degrees < 113:
            return 'East'
        if degrees < 158:
            return 'SEast'
        if degrees < 203:
            return 'South'
        if degrees < 248:
            return 'SWest'
        if degrees < 293:
            return 'West'
        if degrees < 338:
            return 'NWest'

    def extend_day(self, day):
        if day == 'Mon':
            return _('Monday')
        elif day == 'Tue':
            return _('Tuesday')
        elif day == 'Wed':
            return _('Wednesday')
        elif day == 'Thu':
            return _('Thursday')
        elif day == 'Fri':
            return _('Friday')
        elif day == 'Sat':
            return _('Saturday')
        elif day == 'Sun':
            return _('Sunday')
        else:
            return day

    def checkIcon(self, localfile):
        if fileExists(localfile):
            pass
        else:
            url = localfile.replace('/usr/lib/enigma2/python/Plugins/Extensions/Weather/Icon/weather', 'http://www.mysite.net/weapic/weabig')
            handler = urlopen(url)	
            if handler:
                content = handler.read()
                fileout = open(localfile, 'wb')
                fileout.write(content)
                handler.close()
                fileout.close()
        return localfile

    def get_Url(self):
        url = 'http://weather.yahooapis.com/forecastrss?w='
        url2 = '721943'
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Weather/Config/Location_id"):	
             url2=open("/usr/lib/enigma2/python/Plugins/Extensions/Weather/Config/Location_id").read()				
        url = url+url2+'&u=c'
        return url

    def delTimer(self):
        del self.activityTimer

    def key_red(self):
        self.session.open(WeatherSearch)
		
def Main(session, **kwargs):
            session.open(MeteoMain)

def Plugins(**kwargs):
        return PluginDescriptor(name = 'Weather', description = 'Weather Yahoo', icon = 'plugin.png', where = [PluginDescriptor.WHERE_EXTENSIONSMENU,PluginDescriptor.WHERE_PLUGINMENU], fnc = Main)


          