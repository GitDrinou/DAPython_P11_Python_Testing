from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def show_summary(self):
        # Test de la page liste des compétitions
        self.client.post(
            "/showSummary",
            data={"email": "john@google.com"}
        )

    @task
    def purchase_places(self):
        # Test de l'achat de places
        self.client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1"
            }
        )
