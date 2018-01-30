from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse

User = get_user_model()
class BlogPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User.objects.create(username='testusertoufiq', email='test@test.com')
		user_obj.set_password('test1234')
		user_obj.save()
		blog_post = BlogPost.objects.create(user=user_obj, title='New Post 11', content='wow haha')
		blog_post.save()

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_post(self):
		post_count = BlogPost.objects.count()
		self.assertEqual(post_count, 1)

	def test_get_list(self):
		data = {}
		url=api_reverse("api-postings:post-listcreate")
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_post_item(self):
		data={'title': "Something", 'content':'something called content'}
		url = api_reverse('api-postings:post-listcreate')
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_get_item(self):
		blog_post = BlogPost.objects.first()
		data = {}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_item(self):
		blog_post = BlogPost.objects.first()
		data={'title': "Something", 'content':'something called content'}
		url = blog_post.get_api_url()
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



