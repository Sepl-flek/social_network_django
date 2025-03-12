import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from post.models import Post, UserPostRelation
from post.serializers import PostSerializer


class PostApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user1')
        self.post1 = Post.objects.create(header='dog' ,description='Post about dog', owner=self.user)
        self.post2 = Post.objects.create(header='cat' ,description='Post about cat', owner=self.user)

    def test_get(self):
        url = reverse('post-list')

        request = self.client.get(url)
        serializer_data = PostSerializer([self.post1, self.post2], many=True).data
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(serializer_data, request.data)

    def test_get_one(self):
        url = reverse('post-detail', args=(self.post1.id,))

        response = self.client.get(url)
        serializer_data = PostSerializer(self.post1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('post-list')

        data = {'header': 'Naruto',
                'description': 'Post about Naruto'}

        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Post.objects.all().count())
        self.assertEqual(self.user, Post.objects.last().owner)


class TestPostRelation(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user2 = User.objects.create(username='test_user2')
        self.post1 = Post.objects.create(header='dog', description='Post about dog', owner=self.user)
        self.post2 = Post.objects.create(header='cat', description='Post about cat', owner=self.user)

    def test_like(self):
        url = reverse('userpostrelation-detail', args=(self.post1.id,))

        self.client.force_login(self.user)
        '''Check on like'''
        data = {
            'is_like': True
        }
        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.post1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user, post=self.post1)
        self.assertTrue(relation.is_like)
        self.assertEqual(1, self.post1.likes)

        '''chek remove like'''
        data = {
            'is_like': False
        }
        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.post1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.is_like)
        self.assertEqual(0, self.post1.likes)

        data = {
            'is_bookmark': True
        }
        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user, post=self.post1)

        self.assertTrue(relation.is_bookmark)