from locust import HttpUser, task, between, events
from influxdb import InfluxDBClient
import json
import socket
import datetime
import pytz

host=socket.gethostname()
client=InfluxDBClient(host="localhost",port="8086")
client.switch_database("locust_data")

def individual_success_handle(request_type,name,response_time,response_length,**kwargs):
    print(request_type+ name+str(response_time)+str(response_length))
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                       '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                       '}]'
    json_string=SUCCESS_TEMPLATE%("ResponseTable",host,name,request_type,"OK",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    client.write_points(json.loads(json_string))

def individual_fail_handle(request_type,name,response_time,response_length,exception,**kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string=FAIL_TEMPLATE%("ResponseTable",host,name,request_type,exception,"FAIL",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    client.write_points(json.loads(json_string))

events.request_success+=individual_success_handle
events.request_failure+=individual_fail_handle

class Cliente(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    def on_start(self):
        print('ok')

    @task
    def cliente_no_ar(self):
        request = self.client.request(method="GET", url="/cliente/servidor", auth=('usuario1', 'senha1'))
        print(request.content)
        print(request.status_code)

    @task
    def cadastrar_cliente(self):
        payload = {"nome": "TESTE 109","cpf": "07725791485","usuario": {"id": 180}}
        request = self.client.request(method="POST", url="/cliente", auth=('usuario1', 'senha1'), json=payload)
        print(request.status_code)