from locust import HttpUser, task, between

class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_tf_predict(self):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        res = self.client.get("/", headers=headers)