from django.test import TestCase
from core.businesslogic.matching import matching_logic
from core.models import Project, Investor
import datetime

class MatchmakingTestCase(TestCase):
    def setUp(self):
        self.project_one = Project.objects.create(name="Project One", description="Desc of project", amount=1000.00, delivery_date=datetime.date(2022, 12, 30))
        self.project_two = Project.objects.create(name="Project Two", description="Desc of project", amount=1000.00, delivery_date=datetime.date(2022, 10, 30))
        self.project_three = Project.objects.create(name="Project Three", description="Desc of project", amount=7000.00, delivery_date=datetime.date(2022, 3, 30))

        self.investor_one = Investor.objects.create(name="Investor One", remaining_amount=10000, total_amount=10000, individual_amount=7000, project_delivery_deadline=datetime.date(2023, 3, 20))
        self.investor_two = Investor.objects.create(name="Investor Two", remaining_amount=4000, total_amount=4000, individual_amount=4000, project_delivery_deadline=datetime.date(2022, 11, 20))
        self.investor_three = Investor.objects.create(name="Investor Three", remaining_amount=10000, total_amount=10000, individual_amount=8000, project_delivery_deadline=datetime.date(2022, 4, 20))

    def test_matchmaking_for_project(self):
        matching_list_for_project_one = matching_logic(self.project_one, Investor.objects.all())
        matching_list_for_project_two = matching_logic(self.project_two, Investor.objects.all())
        matching_list_for_project_three = matching_logic(self.project_three, Investor.objects.all())

        self.assertEqual(len(matching_list_for_project_one), 1)
        self.assertIn(self.investor_one.id, matching_list_for_project_one)

        self.assertEqual(len(matching_list_for_project_two), 2)
        self.assertIn(self.investor_one.id, matching_list_for_project_two)
        self.assertIn(self.investor_two.id, matching_list_for_project_two)

        self.assertEqual(len(matching_list_for_project_three), 2)
        self.assertIn(self.investor_one.id, matching_list_for_project_three)
        self.assertIn(self.investor_three.id, matching_list_for_project_three)

    def test_matchmaking_for_investor(self):
        matching_list_for_investor_one = matching_logic(self.investor_one, Project.objects.all())
        matching_list_for_investor_two = matching_logic(self.investor_two, Project.objects.all())
        matching_list_for_investor_three = matching_logic(self.investor_three, Project.objects.all())

        self.assertEqual(len(matching_list_for_investor_one), 3)
        self.assertIn(self.project_one.id, matching_list_for_investor_one)
        self.assertIn(self.project_two.id, matching_list_for_investor_one)
        self.assertIn(self.project_three.id, matching_list_for_investor_one)

        self.assertEqual(len(matching_list_for_investor_two), 1)
        self.assertIn(self.project_two.id, matching_list_for_investor_two)

        self.assertEqual(len(matching_list_for_investor_three), 1)
        self.assertIn(self.project_three.id, matching_list_for_investor_three)
