from django.test import TestCase, Client
from .models import Reservation
from authentication.models import CustomUser
from cars.models import Car, CarType
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from django.urls import reverse

class ReservationModelTest(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create(email='test@test.com')
        self.car_type = CarType.objects.create(name='Test')

        self.car = Car.objects.create(
            brand='Test',
            model='Test',
            air_conditioning=Car.AirConditioning.NO,
            car_type=self.car_type,
            doors_quantity=Car.DoorsQuantity.TWO_DOOR,
            people_quantity=2,
            fuel_type=Car.FuelType.LPG,
            transmission_type=Car.TransmissionType.MANUAL,
            description='Test',
            price=1000.00
        )

    def test_reservation_str(self):
        reservation = Reservation.objects.create(
            user=self.user,
            car=self.car,
            start_date=timezone.now().date(),
            finish_date=timezone.now().date() + timezone.timedelta(days=3),
            reservation_status=Reservation.ReservationStatus.ACTIVE
        )
        expected_str = f'Rezerwacja - {self.car} {self.user}'
        self.assertEqual(str(reservation), expected_str)
        
    def test_reservation_status_choices(self):
        choices = dict(Reservation.ReservationStatus.choices)
        self.assertIn('active', choices)
        self.assertIn('canceled', choices)
        self.assertIn('completed', choices)

class ReservationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
        )
        self.car_type = CarType.objects.create(name='Test')
        self.car = Car.objects.create(
            brand='Test',
            model='Test',
            air_conditioning=Car.AirConditioning.NO,
            car_type=self.car_type,
            doors_quantity=Car.DoorsQuantity.TWO_DOOR,
            people_quantity=2,
            fuel_type=Car.FuelType.LPG,
            transmission_type=Car.TransmissionType.MANUAL,
            description='Test',
            price=1000.00
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            car=self.car,
            start_date=date.today(),
            finish_date=date.today(),
            reservation_status='active',
        )
    
    def test_reservation_view_get(self):
        response = self.client.get(reverse('reservation'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_reservation(self):
        response = self.client.post(reverse('create_reservation'), {'start': date.today(), 'end': date.today(), 'car': self.car.id})
        self.assertTrue(Reservation.objects.filter(user=self.user, car=self.car).exists())

class AddReservationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.car_type = CarType.objects.create(name='Test')
        self.car = Car.objects.create(
            brand='Test',
            model='Test',
            air_conditioning=Car.AirConditioning.NO,
            car_type=self.car_type,
            doors_quantity=Car.DoorsQuantity.TWO_DOOR,
            people_quantity=2,
            fuel_type=Car.FuelType.LPG,
            transmission_type=Car.TransmissionType.MANUAL,
            description='Test',
            price=1000.00
        )
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword',
            first_name='test',
        )
        self.user.groups.create(name='Employees')

    def test_add_reservation(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'user': self.user.id,
            'car': self.car.id,
            'start_date': '2024-01-01',
            'finish_date': '2024-01-02',
            'reservation_status': 'active',
        }
        response = self.client.post(reverse('add_reservation'), data)
        self.assertEqual(response.url, reverse('employee_reservations'))
        self.assertTrue(self.user.reservation_set.filter(car=data['car']).exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Rezerwacja została dodana pomyślnie!')
        
class EditAndDeleteReservationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.car_type = CarType.objects.create(name='Test')
        self.car = Car.objects.create(
            brand='Test',
            model='Test',
            air_conditioning=Car.AirConditioning.NO,
            car_type=self.car_type,
            doors_quantity=Car.DoorsQuantity.TWO_DOOR,
            people_quantity=2,
            fuel_type=Car.FuelType.LPG,
            transmission_type=Car.TransmissionType.MANUAL,
            description='Test',
            price=1000.00
        )
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword',
            first_name='test',
        )
        self.user.groups.create(name='Employees')
        self.reservation = Reservation.objects.create(
            user=self.user,
            car_id=self.car.id,
            start_date='2024-01-01',
            finish_date='2024-01-02',
            reservation_status='active',
        )
    def test_edit_reservation(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'user': self.user.id,
            'car': self.car.id,
            'start_date': '2024-02-01',
            'finish_date': '2024-02-02',
            'reservation_status': 'active',
        }
        response = self.client.post(reverse('edit_reservation', args=[self.reservation.id]), data)
        self.assertEqual(response.url, reverse('employee_reservations'))
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.start_date, date(2024, 2, 1))
        self.assertEqual(self.reservation.finish_date, date(2024, 2, 2))
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Rezerwacja została zedytowana pomyślnie!')
        
    def test_delete_reservation(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.post(reverse('delete_reservation', args=[self.reservation.id]))
        self.assertEqual(response.url, reverse('employee_reservations'))
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Rezerwacja została usunięta pomyślnie!')
