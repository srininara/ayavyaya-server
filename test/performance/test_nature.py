# Run this under the perf virtualenv
from locust import HttpLocust, TaskSet, task

class NatureGetTest(TaskSet):

    @task
    def get_natures(self):
        self.client.get("/ayavyaya/api/v1.0/natures")

class NaturePerfTests(HttpLocust):
    # host = "http://example.org"
    max_wait = 1000
    min_wait = 1000
    task_set = NatureGetTest
