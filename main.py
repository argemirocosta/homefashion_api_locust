from locust import HttpUser, task, between


class HelloWorldUser(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        #self.client.get('/cliente/servidor')
        self.client.request(method="GET", url="/cliente/servidor", auth=('usuario1', 'senha1'))
