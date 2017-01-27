import urllib2
import json
latitude = "43.665301"
longitude = "-79.395720"
f = urllib2.urlopen('http://api.wunderground.com/api/6a28c24f2553611a/geolookup/conditions/q/' +
latitude + ',' + longitude + '.json')
#f = urllib2.urlopen('http://api.wunderground.com/api/6a28c24f2553611a/\
#geolookup/conditions/q/CA/San_Francisco.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_c']
feels_like = parsed_json['current_observation']['feelslike_c']
humidity = parsed_json['current_observation']['relative_humidity']
precip = parsed_json['current_observation']['precip_today_metric']
weather = parsed_json['current_observation']['weather']
print "Current temperature in %s is: %s Degrees Celsius" % (location, temp_f)
print "Feels like: %s Degrees Celsius" % (feels_like)
print "Humidity: %s" % (humidity)
print "Precipitation: %s mm" % (precip)
print "Weather: %s" % (weather)
#for doc in parsed_json:
    #print parsed_json[doc]

f.close()
