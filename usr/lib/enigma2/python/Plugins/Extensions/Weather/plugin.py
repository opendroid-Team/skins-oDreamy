# -*- coding: UTF-8 -*-
# Weather by m43c0 
# Last modified 28-10-2013
# Last modified by opendroid team 29-1-2016
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
from Components.config import config, ConfigSubsection, ConfigYesNo
from time import strftime
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
        self['3lab22'] = Pixmap()
        self['3lab19'] = Label('')
        self['3lab19b'] = Label('')
        self['3lab20'] = Label('')
        self['3lab20b'] = Label('')
        self['3lab18'] = Label('')
        self['3lab21'] = Label('')
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
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/weather_icons_special/%s.png' % str(weather_data['condition']['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 220, 195, 0, 0, 0, 0)
                self['lab5'].instance.setPixmap(png)
                txt = self.extend_name(str(weather_data['condition']['text']))
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
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/weather_icons_special/%s.png' % str(weather_data['forecasts'][0]['code'])
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
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/weather_icons_special/%s.png' % str(weather_data['forecasts'][1]['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 150, 133, 0, 0, 0, 0)
                self['lab22'].instance.setPixmap(png)
                txt = self.extend_day(str(weather_data['forecasts'][2]['day']))
                self['3lab18'].setText(txt)
                self['3lab19'].setText(_('High :'))
                txt = str(weather_data['forecasts'][2]['high']) + '\xc2\xb0C'
                self['3lab19b'].setText(txt)
                self['3lab20'].setText(_('Low :'))
                txt = str(weather_data['forecasts'][2]['low']) + '\xc2\xb0C'
                self['3lab20b'].setText(txt)
                txt = str(weather_data['forecasts'][2]['text'])
                self['3lab21'].setText(txt)
                icon = '/usr/lib/enigma2/python/Plugins/Extensions/Weather/weather_icons_special/%s.png' % str(weather_data['forecasts'][2]['code'])
                myicon = self.checkIcon(icon)
                png = loadPic(myicon, 150, 133, 0, 0, 0, 0)
                self['3lab22'].instance.setPixmap(png)
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

    def extend_name(self, name):
        if name == 'AM Clouds/PM Sun':
            return _('AM Clouds/PM Sun')
        elif name == 'AM Drizzle':
            return _('AM Drizzle')
        elif name == 'AM Drizzle/Wind':
            return _('AM Drizzle/Wind')
        elif name == 'AM Fog/PM Clouds':
            return _('AM Fog/PM Clouds')
        elif name == 'AM Fog/PM Sun':
            return _('AM Fog/PM Sun')
        elif name == 'AM Ice':
            return _('AM Ice')
        elif name == 'AM Light Rain':
            return _('AM Light Rain')
        elif name == 'AM Light Rain/Wind':
            return _('AM Light Rain/Wind')
        elif name == 'AM Light Snow':
            return _('AM Light Snow')
        elif name == 'AM Rain':
            return _('AM Rain')
        elif name == 'AM Rain/Snow Showers':
            return _('AM Rain/Snow Showers')
        elif name == 'AM Rain/Snow':
            return _('AM Rain/Snow')
        elif name == 'AM Rain/Snow/Wind':
            return _('AM Rain/Snow/Wind')
        elif name == 'AM Rain/Wind':
            return _('AM Rain/Wind')
        elif name == 'AM Showers':
            return _('AM Showers')
        elif name == 'AM Showers/Wind':
            return _('AM Showers/Wind')
        elif name == 'AM Snow Showers':
            return _('AM Snow Showers')
        elif name == 'AM Snow':
            return _('AM Snow')
        elif name == 'AM Thundershowers':
            return _('AM Thundershowers')
        elif name == 'Blowing Snow':
            return _('Blowing Snow')
        elif name == 'Clear':
            return _('Clear')
        elif name == 'Clear/Windy':
            return _('Clear/Windy')
        elif name == 'Clouds Early/Clearing Late':
            return _('Clouds Early/Clearing Late')
        elif name == 'Cloudy':
            return _('Cloudy')
        elif name == 'Cloudy/Wind':
            return _('Cloudy/Wind')
        elif name == 'Cloudy/Windy':
            return _('Cloudy/Windy')
        elif name == 'Drifting Snow':
            return _('Drifting Snow')
        elif name == 'Drifting Snow/Windy':
            return _('Drifting Snow/Windy')
        elif name == 'Drizzle Early':
            return _('Drizzle Early')
        elif name == 'Drizzle Late':
            return _('Drizzle Late')
        elif name == 'Drizzle':
            return _('Drizzle')
        elif name == 'Drizzle/Fog':
            return _('Drizzle/Fog')
        elif name == 'Drizzle/Wind':
            return _('Drizzle/Wind')
        elif name == 'Drizzle/Windy':
            return _('Drizzle/Windy')
        elif name == 'Fair':
            return _('Fair')
        elif name == 'Fair/Windy':
            return _('Fair/Windy')
        elif name == 'Few Showers':
            return _('Few Showers')
        elif name == 'Few Showers/Wind':
            return _('Few Showers/Wind')
        elif name == 'Few Snow Showers':
            return _('Few Snow Showers')
        elif name == 'Fog Early/Clouds Late':
            return _('Fog Early/Clouds Late')
        elif name == 'Fog Late':
            return _('Fog Late')
        elif name == 'Fog':
            return _('Fog')
        elif name == 'Fog/Windy':
            return _('Fog/Windy')
        elif name == 'Foggy':
            return _('Foggy')
        elif name == 'Freezing Drizzle':
            return _('Freezing Drizzle')
        elif name == 'Freezing Drizzle/Windy':
            return _('Freezing Drizzle/Windy')
        elif name == 'Freezing Rain':
            return _('Freezing Rain')
        elif name == 'Haze':
            return _('Haze')
        elif name == 'Heavy Drizzle':
            return _('Heavy Drizzle')
        elif name == 'Heavy Rain Shower':
            return _('Heavy Rain Shower')
        elif name == 'Heavy Rain':
            return _('Heavy Rain')
        elif name == 'Heavy Rain/Wind':
            return _('Heavy Rain/Wind')
        elif name == 'Heavy Rain/Windy':
            return _('Heavy Rain/Windy')
        elif name == 'Heavy Snow Shower':
            return _('Heavy Snow Shower')
        elif name == 'Heavy Snow':
            return _('Heavy Snow')
        elif name == 'Heavy Snow/Wind':
            return _('Heavy Snow/Wind')
        elif name == 'Heavy Thunderstorm':
            return _('Heavy Thunderstorm')
        elif name == 'Heavy Thunderstorm/Windy':
            return _('Heavy Thunderstorm/Windy')
        elif name == 'Ice Crystals':
            return _('Ice Crystals')
        elif name == 'Ice Late':
            return _('Ice Late')
        elif name == 'Isolated T-storms':
            return _('Isolated T-storms')
        elif name == 'Isolated Thunderstorms':
            return _('Isolated Thunderstorms')
        elif name == 'Light Drizzle':
            return _('Light Drizzle')
        elif name == 'Light Freezing Drizzle':
            return _('Light Freezing Drizzle')
        elif name == 'Light Freezing Rain':
            return _('Light Freezing Rain')
        elif name == 'Light Freezing Rain/Fog':
            return _('Light Freezing Rain/Fog')
        elif name == 'Light Rain Early':
            return _('Light Rain Early')
        elif name == 'Light Rain':
            return _('Light Rain')
        elif name == 'Light Rain Late':
            return _('Light Rain Late')
        elif name == 'Light Rain Shower':
            return _('Light Rain Shower')
        elif name == 'Light Rain Shower/Fog':
            return _('Light Rain Shower/Fog')
        elif name == 'Light Rain Shower/Windy':
            return _('Light Rain Shower/Windy')
        elif name == 'Light Rain with Thunder':
            return _('Light Rain with Thunder')
        elif name == 'Light Rain/Fog':
            return _('Light Rain/Fog')
        elif name == 'Light Rain/Freezing Rain':
            return _('Light Rain/Freezing Rain')
        elif name == 'Light Rain/Wind Early':
            return _('Light Rain/Wind Early')
        elif name == 'Light Rain/Wind Late':
            return _('Light Rain/Wind Late')
        elif name == 'Light Rain/Wind':
            return _('Light Rain/Wind')
        elif name == 'Light Rain/Windy':
            return _('Light Rain/Windy')
        elif name == 'Light Sleet':
            return _('Light Sleet')
        elif name == 'Light Snow Early':
            return _('Light Snow Early')
        elif name == 'Light Snow Grains':
            return _('Light Snow Grains')
        elif name == 'Light Snow Late':
            return _('Light Snow Late')
        elif name == 'Light Snow Shower':
            return _('Light Snow Shower')
        elif name == 'Light Snow Shower/Fog':
            return _('Light Snow Shower/Fog')
        elif name == 'Light Snow with Thunder':
            return _('Light Snow with Thunder')
        elif name == 'Light Snow':
            return _('Light Snow')
        elif name == 'Light Snow/Fog':
            return _('Light Snow/Fog')
        elif name == 'Light Snow/Freezing Rain':
            return _('Light Snow/Freezing Rain')
        elif name == 'Light Snow/Wind':
            return _('Light Snow/Wind')
        elif name == 'Light Snow/Windy':
            return _('Light Snow/Windy')
        elif name == 'Light Snow/Windy/Fog':
            return _('Light Snow/Windy/Fog')
        elif name == 'Mist':
            return _('Mist')
        elif name == 'Mostly Clear':
            return _('Mostly Clear')
        elif name == 'Mostly Cloudy':
            return _('Mostly Cloudy')
        elif name == 'Mostly Cloudy/Wind':
            return _('Mostly Cloudy/Wind')
        elif name == 'Mostly Sunny':
            return _('Mostly Sunny')
        elif name == 'Partial Fog':
            return _('Partial Fog')
        elif name == 'Partly Cloudy':
            return _('Partly Cloudy')
        elif name == 'Partly Cloudy/Wind':
            return _('Partly Cloudy/Wind')
        elif name == 'Patches of Fog':
            return _('Patches of Fog')
        elif name == 'Patches of Fog/Windy':
            return _('Patches of Fog/Windy')
        elif name == 'PM Drizzle':
            return _('PM Drizzle')
        elif name == 'PM Fog':
            return _('PM Fog')
        elif name == 'PM Light Snow':
            return _('PM Light Snow')
        elif name == 'PM Light Rain':
            return _('PM Light Rain')
        elif name == 'PM Light Rain/Wind':
            return _('PM Light Rain/Wind')
        elif name == 'PM Light Snow/Wind':
            return _('PM Light Snow/Wind')
        elif name == 'PM Rain':
            return _('PM Rain')
        elif name == 'PM Rain/Snow Showers':
            return _('PM Rain/Snow Showers')
        elif name == 'PM Rain/Snow':
            return _('PM Rain/Snow')
        elif name == 'PM Rain/Wind':
            return _('PM Rain/Wind')
        elif name == 'PM Showers':
            return _('PM Showers')
        elif name == 'PM Showers/Wind':
            return _('PM Showers/Wind')
        elif name == 'PM Snow Showers':
            return _('PM Snow Showers')
        elif name == 'PM Snow Showers/Wind':
            return _('PM Snow Showers/Wind')
        elif name == 'PM Snow':
            return _('PM Snow')
        elif name == 'PM T-storms':
            return _('PM T-storms')
        elif name == 'PM Thundershowers':
            return _('PM Thundershowers')
        elif name == 'PM Thunderstorms':
            return _('PM Thunderstorms')
        elif name == 'Rain and Snow':
            return _('Rain and Snow')
        elif name == 'Rain and Snow/Windy':
            return _('Rain and Snow/Windy')
        elif name == 'Rain/Snow Showers/Wind':
            return _('Rain/Snow Showers/Wind')
        elif name == 'Rain Early':
            return _('Rain Early')
        elif name == 'Rain Late':
            return _('Rain Late')
        elif name == 'Rain Shower':
            return _('Rain Shower')
        elif name == 'Rain Shower/Windy':
            return _('Rain Shower/Windy')
        elif name == 'Rain to Snow':
            return _('Rain to Snow')
        elif name == 'Rain':
            return _('Rain')
        elif name == 'Rain/Snow Early':
            return _('Rain/Snow Early')
        elif name == 'Rain/Snow Late':
            return _('Rain/Snow Late')
        elif name == 'Rain/Snow Showers Early':
            return _('Rain/Snow Showers Early')
        elif name == 'Rain/Snow Showers Late':
            return _('Rain/Snow Showers Late')
        elif name == 'Rain/Snow Showers':
            return _('Rain/Snow Showers')
        elif name == 'Rain/Snow':
            return _('Rain/Snow')
        elif name == 'Rain/Snow/Wind':
            return _('Rain/Snow/Wind')
        elif name == 'Rain/Thunder':
            return _('Rain/Thunder')
        elif name == 'Rain/Wind Early':
            return _('Rain/Wind Early')
        elif name == 'Rain/Wind Late':
            return _('Rain/Wind Late')
        elif name == 'Rain/Wind':
            return _('Rain/Wind')
        elif name == 'Rain/Windy':
            return _('Rain/Windy')
        elif name == 'Scattered Showers':
            return _('Scattered Showers')
        elif name == 'Scattered Showers/Wind':
            return _('Scattered Showers/Wind')
        elif name == 'Scattered Snow Showers':
            return _('Scattered Snow Showers')
        elif name == 'Scattered Snow Showers/Wind':
            return _('Scattered Snow Showers/Wind')
        elif name == 'Scattered T-storms':
            return _('Scattered T-storms')
        elif name == 'Scattered Thunderstorms':
            return _('Scattered Thunderstorms')
        elif name == 'Shallow Fog':
            return _('Shallow Fog')
        elif name == 'Showers':
            return _('Showers')
        elif name == 'Showers Early':
            return _('Showers Early')
        elif name == 'Showers Late':
            return _('Showers Late')
        elif name == 'Showers in the Vicinity':
            return _('Showers in the Vicinity')
        elif name == 'Showers/Wind':
            return _('Showers/Wind')
        elif name == 'Sleet and Freezing Rain':
            return _('Sleet and Freezing Rain')
        elif name == 'Sleet/Windy':
            return _('Sleet/Windy')
        elif name == 'Snow Grains':
            return _('Snow Grains')
        elif name == 'Snow Late':
            return _('Snow Late')
        elif name == 'Snow Shower':
            return _('Snow Shower')
        elif name == 'Snow Showers Early':
            return _('Snow Showers Early')
        elif name == 'Snow Showers Late':
            return _('Snow Showers Late')
        elif name == 'Snow Showers':
            return _('Snow Showers')
        elif name == 'Snow Showers/Wind':
            return _('Snow Showers/Wind')
        elif name == 'Snow to Rain':
            return _('Snow to Rain')
        elif name == 'Snow':
            return _('Snow')
        elif name == 'Snow/Wind':
            return _('Snow/Wind')
        elif name == 'Snow/Windy':
            return _('Snow/Windy')
        elif name == 'Squalls':
            return _('Squalls')
        elif name == 'Sunny':
            return _('Sunny')
        elif name == 'Sunny/Wind':
            return _('Sunny/Wind')
        elif name == 'Sunny/Windy':
            return _('Sunny/Windy')
        elif name == 'T-showers':
            return _('T-showers')
        elif name == 'Thunder in the Vicinity':
            return _('Thunder in the Vicinity')
        elif name == 'Thunder':
            return _('Thunder')
        elif name == 'Thundershowers Early':
            return _('Thundershowers Early')
        elif name == 'Thundershowers':
            return _('Thundershowers')
        elif name == 'Thunderstorm':
            return _('Thunderstorm')
        elif name == 'Thunderstorm/Windy':
            return _('Thunderstorm/Windy')
        elif name == 'Thunderstorms Early':
            return _('Thunderstorms Early')
        elif name == 'Thunderstorms Late':
            return _('Thunderstorms Late')
        elif name == 'Thunderstorms':
            return _('Thunderstorms')
        elif name == 'Unknown Precipitation':
            return _('Unknown Precipitation')
        elif name == 'Unknown':
            return _('Unknown')
        elif name == 'Wintry Mix':
            return _('Wintry Mix')
        else:
            return name

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


          
