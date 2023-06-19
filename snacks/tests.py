from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack
# Create your tests here.

class SnacksTest(TestCase):

    def setUp(self):
        self.purchaser = get_user_model().objects.create(username="tester",password="tester")
        self.Snack = Snack.objects.create(title="tester", description="blah blah blah", purchaser=self.purchaser)

    def test_home_page_status(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_page_response(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_home_page_context(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        snack_list = response.context['Snacks']
        self.assertEqual(len(snack_list), 1)
        self.assertEqual(snack_list[0].title, "tester")
        self.assertEqual(snack_list[0].description,'blah blah blah')
        self.assertEqual(snack_list[0].purchaser.username, "tester")

    def test_detail_page_status_code(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        snack_detail = response.context['snack']
        self.assertEqual(snack_detail.title, "tester")
        self.assertEqual(snack_detail.description, 'blah blah blah')
        self.assertEqual(snack_detail.purchaser.username, "tester")

    
    def test_create_view(self):
        obj={
            'title':"test2",
            'purchaser':self.purchaser.id,
            'description': "info..."
            
        }

        url = reverse('snack_create')
        response = self.client.post(path=url,data=obj,follow=True)
        self.assertEqual(len(Snack.objects.all()),2)
        # self.assertRedirects(response, reverse('snack_list'))

    def test_update_view(self):
        obj={
            'title':"test2",
            'purchaser':self.purchaser.id,
            'description': "info..."
            
        }

        url = reverse('snack_update', args=(1,))
        response = self.client.post(path=url,data=obj,follow=True)
        # self.assertEqual(len(Snack.objects.all()),2)
        self.assertRedirects(response, reverse('snack_list'))

    
    def test_delete_view(self):
       

        url = reverse('snack_delete', args=(1,))
        response = self.client.post(path=url,follow=True)
        # self.assertEqual(len(Snack.objects.all()),2)
        self.assertRedirects(response, reverse('snack_list'))


    def test_str_method(self):
        self.assertEqual(str(self.Snack),"tester")


    def test_create_response(self):
        url = reverse('snack_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_create.html')
        self.assertTemplateUsed(response, 'base.html')


    def test_update_response(self):
        url = reverse('snack_update', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_update.html')
        self.assertTemplateUsed(response, 'base.html')


    def test_delete_response(self):
        url = reverse('snack_delete', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_delete.html')
        self.assertTemplateUsed(response, 'base.html')