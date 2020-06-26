import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Menu

def create_menu(restaurant_name, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Menu.objects.create(restaurant_name=restaurant_name, pub_date=time)

class MenuIndexViewTests(TestCase):
    def test_no_menus(self):
        """
        Test if proper error message displays when there are no menus
        """
        response = self.client.get(reverse('menus:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Menus Today")
        self.assertQuerysetEqual(response.context['menu_list'], [])

    def test_past_menu(self):
        """
        Menu with pub_date older than one week
        """
        create_menu(restaurant_name='Old Menu', days=-8)
        response = self.client.get(reverse('menus:index'))
        self.assertContains(response, "No Menus Today")
        self.assertQuerysetEqual(response.context['menu_list'], [])

    def test_recent_menu(self):
        """
        Menu with valid pub_date
        """
        create_menu(restaurant_name="Recent Menu", days=-6)
        response = self.client.get(reverse('menus:index'))
        self.assertQuerysetEqual(
            response.context['menu_list'], 
            ['<Menu: Recent Menu Menu>'])

    def test_future_menu(self):
        """
        Menu with pub_date in the future should not be displayed
        """
        create_menu(restaurant_name="Future Menu", days = 30)
        response = self.client.get(reverse('menus:index'))
        self.assertContains(response, "No Menus Today")
        self.assertQuerysetEqual(response.context['menu_list'], [])

    def test_past_recent_and_future_menu(self):
        """
        Menu with pub_date within the past week are displayed
        but beyond a week are not
        """
        create_menu(restaurant_name='Old Menu', days=-8)
        create_menu(restaurant_name='Recent Menu', days=-6)
        create_menu(restaurant_name='Future Menu', days = 1)
        response = self.client.get(reverse('menus:index'))
        self.assertQuerysetEqual(
            response.context['menu_list'],
            ['<Menu: Recent Menu Menu>']
        )

    def test_more_than_10_menus(self):
        """
        Create 11 menus and check that only 10 are displayed
        """
        for i in range(0,10):
            create_menu(restaurant_name='Menu {}'.format(i), days=-1)
        response = self.client.get(reverse('menus:index'))
        self.assertEqual(len(response.context['menu_list']), 10)

class MenuRetrieveViewTests(TestCase):
    def test_future_menu(self):
        """
        Retrieve view of a menu with future pub_date should return 404
        """
        future_menu = create_menu(restaurant_name='Future menu', days=5)
        url = reverse('menus:retrieve', args=(future_menu.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recent_menu(self):
        """
        Retrieve view of menu with pub_date within one week should display
        """
        recent_menu = create_menu(restaurant_name='Recent menu', days=-5)
        url = reverse('menus:retrieve', args=(recent_menu.id,))
        response = self.client.get(url)
        self.assertContains(response, recent_menu.restaurant_name)

class MenuModelTests(TestCase):

    def test_published_within_one_week_with_future_menu(self):
        """
        published_within_one_week() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_menu = Menu(pub_date=time)
        self.assertIs(future_menu.published_within_one_week(), False)

    def test_published_within_one_week_with_old_menu(self):
        """
        published_within_one_week() returns False for questions whose pub_date is beyon one week ago
        """
        time = timezone.now() - datetime.timedelta(days=7, seconds=1)
        past_menu = Menu(pub_date=time)
        self.assertIs(past_menu.published_within_one_week(), False)

    def test_published_within_one_week_with_valid_pub_date(self):
        """
        """
        time = timezone.now() - datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
        recent_menu = Menu(pub_date=time)
        self.assertIs(recent_menu.published_within_one_week(), True)

    def test_published_within_one_week_with_default_pub_date(self):
        new_menu = Menu(restaurant_name='claro')
        self.assertIs(new_menu.published_within_one_week(), True)

    def test_menu_item_relationship(self):
        """
        When creating a menu and subsequent items, does it actually store the data in the database
        """
        claro: Menu = Menu(restaurant_name='claro')
