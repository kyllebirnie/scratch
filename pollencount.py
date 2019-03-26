import requests
import datetime

today = datetime.datetime.now().strftime('%Y-%m-%d')
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')


class pollen(object):

    def __init__(self, postcode):

        request = requests.get('http://api.postcodes.io/postcodes/' + postcode)
        if request.status_code == 200:
            response = request.json()['result']
            self.latitude = response['latitude']
            self.longitude = response['longitude']

    @property
    def pollencount(self):

        request = requests.get('https://socialpollencount.co.uk/api/forecast?location=[%s,%s]' % (self.latitude, self.longitude))
        if request.status_code == 200:
            forecast = request.json()['forecast']
            try:
                for counter, element in enumerate(forecast):
                    if today in element['date']:
                        todays_pollen_level = element.get('pollen_count')
                    if tomorrow in element['date']:
                        tomorrows_pollen_level = element.get('pollen_count')
                        return todays_pollen_level, tomorrows_pollen_level, forecast
            except ValueError:
                raise RuntimeError("Unexpected response")
            else:
                raise IOError("Failure downloading from API")


status = pollen('EH129EP').pollencount

print(today, status[0])
print(tomorrow, status[1])