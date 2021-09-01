from django.test import TestCase 
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack

# Create your tests here.

class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'samer', email = 'samer@gmail.com', password = '12345'
        )
        self.snack = Snack.objects.create(
            title = 'Chips', description  = 'It tastes so delicious', purchaser = self.user
        )

    def test_StringRepresentation(self):
        self.assertEqual(str(self.snack), "Chips")

    def test_SnackContent(self):
        self.assertEqual(f"{self.snack.title}", 'Chips')
        self.assertEqual(f"{self.snack.description}", 'It tastes so delicious')
        self.assertEqual(self.snack.purchaser, self.user)

    def test_SnackListView(self):
        url = reverse('snack_list')
        actual = self.client.get(url).status_code
        self.assertEqual(actual, 200)

    def test_SnackDetailsView(self):
        response = self.client.get(reverse('snack_details', args='1'))
        self.assertEqual(response.status_code, 200)

    def test_SnackCreateView(self):
        response = self.client.post(reverse("snack_create"),{"title": "Laiz", "description": "Laiz is delicious", "purchaser": self.user})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laiz')
        self.assertContains(response, 'Laiz is delicious')
        self.assertContains(response, 'samer')

    def test_SnackUpdateView(self):
        response = self.client.post(reverse('snack_update', args='1'), {'title':'Chocolate'})
        self.assertContains(response, 'Chocolate')
        
    def test_SnackDeleteView(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)