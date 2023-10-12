# BEGIN: 3f4d5e6r7t8y
from src.modules.utils import getCountryCode

def test_getCountryCode():
    assert getCountryCode("13.7563,100.5018") == "th"
    assert getCountryCode("51.5074,0.1278") == "gb"
    assert getCountryCode("35.6895,139.6917") == "jp"
    assert getCountryCode("40.7128,-74.0060") == "us"
    assert getCountryCode("48.8566,2.3522") == "fr"
    assert getCountryCode("55.7558,37.6173") == "ru"
    assert getCountryCode("37.5665,126.9780") == "kr"
    assert getCountryCode("31.2304,121.4737") == "cn"
    assert getCountryCode("19.4326,-99.1332") == "mx"
    assert getCountryCode("52.5200,13.4050") == "de"

# END: 3f4d5e6r7t8y