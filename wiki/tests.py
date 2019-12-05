import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page
from wiki.views import PageForm
from django.urls import reverse_lazy, reverse

# Create your tests here.

class WikiTestCase(TestCase):
    def test_true_is_true(self):
        """ Tests if True is equal to True. Should always pass. """
        self.assertEqual(True, True)

    # Testing a Model
    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        # Author is a required field in our model.
        # Create a user for this test and save it to the test database.
        user = User()
        user.save()

        # Create and save a new page to the test database.
        page = Page(title="My Test Page", content="test", author=user)
        page.save()

        # Make sure the slug that was generated in Page.save()
        # matches what we think it should be.
        self.assertEqual(page.slug, "my-test-page")

class PageListViewTests(TestCase):
    """ Tests that the homepage works"""

    def test_multiple_pages(self):    
        # Make some test data to be displayed on the page
        # Same as user = User(); user.save()
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test", author=user)

        # Issue a GET response to the MakeWiki homepage.
        # When we make a request, we get a response back.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the number of pages passed to the template
        # matches the number of pages we have in the database
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )

class PageDetailViewTests(TestCase):
    """ Tests the wiki details page loads for a specific page """

    def test_detail_page(self):
        user = User.objects.create()

        page = Page.objects.create(title="My Detail Page", content="details details schmeetales", author=user)

        slug = page.slug
        response = self.client.get(f'/{slug}/')

        self.assertEqual(response.status_code, 200)

class CreatePageFormTests(TestCase):
    """ Tests if wiki page creation form loads when visiting /new"""

    def test_view_form_page(self):
        # Figure out how to fix this with the new login required stuff
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse('login'))

    def test_form_entry(self):
        user = User.objects.create()

        form_data = {
            "title": "This Is My Hair",
            "author": user.id,
            "content": "I dont wear wigs."
        }

        response = self.client.post('/new', data = form_data)
        self.assertEqual(response.status_code, 302)

        page = Page.objects.get(title='This Is My Hair')
        self.assertEqual(page.content, 'I dont wear wigs.')