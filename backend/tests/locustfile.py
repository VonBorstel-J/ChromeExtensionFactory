# /backend/tests/locustfile.py
from locust import HttpUser, TaskSet, task, between
import random
import string

class UserBehavior(TaskSet):
    def on_start(self):
        self.email = f"user_{self.random_string(5)}@test.com"
        self.password = "password123"
        self.signup()
        self.login()

    def random_string(self, length=5):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def signup(self):
        self.client.post("/auth/signup", json={"email": self.email, "password": self.password})

    def login(self):
        response = self.client.post("/auth/login", json={"email": self.email, "password": self.password})
        self.token = response.json().get("token")

    @task(1)
    def create_project(self):
        project_data = {
            "name": f"Project_{self.random_string(3)}",
            "data": {"templates": ["web_scraper", "tab_manager"]}
        }
        self.client.post("/projects/", json=project_data, headers={"Authorization": self.token})

    @task(2)
    def publish_extension(self):
        project_id = random.randint(1, 50)  # Assuming project IDs range from 1 to 50
        self.client.post(f"/publish/publish/{project_id}", headers={"Authorization": self.token})

    @task(3)
    def download_extension(self):
        project_id = random.randint(1, 50)
        self.client.get(f"/publish/download/{project_id}", headers={"Authorization": self.token})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
