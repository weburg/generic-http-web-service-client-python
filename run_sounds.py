from time import sleep

from weburg.ghowst.generic_http_web_service_client import *


http_web_service = GenericHTTPWebServiceClient("http://localhost:8081/generichttpws")

http_web_service.play_sounds(name="arrow_x.wav")
sleep(0.75)
http_web_service.play_sounds(name="arrow2.wav")