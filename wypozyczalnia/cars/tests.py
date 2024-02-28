from django.test import TestCase, Client
from .models import Car, CarType
from django.urls import reverse
from django.contrib.auth import get_user_model

class CarAndCarTypeModelTest(TestCase):

    def setUp(self):
        self.car_type = CarType.objects.create(name='Test')

    def test_create_multiple_cars(self):
        for i in range(1000):
            car = Car.objects.create(
                brand=f'TestBrand{i}',
                model=f'TestModel{i}',
                air_conditioning=Car.AirConditioning.YES,
                car_type=self.car_type,
                doors_quantity=Car.DoorsQuantity.FIVE_DOOR,
                people_quantity=4,
                fuel_type=Car.FuelType.GASOLINE,
                transmission_type=Car.TransmissionType.MANUAL,
                description=f'Test Description {i}',
                price=1000.00
            )
            self.assertIsNotNone(car)
            self.assertIsInstance(car, Car)

class AddCarAndCarTypeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.car_type = CarType.objects.create(name='Test')
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword',
            first_name='test',
        )
        self.user.groups.create(name='Employees')
        
    def test_add_car_type(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'name': 'test2',
            'description': 'test2',
        }
        response = self.client.post(reverse('add_car_type'), data)
        self.assertEqual(response.url, reverse('employee_car_types'))
        self.assertTrue(CarType.objects.filter(name='test2').exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Typ samochodu został dodany pomyślnie!')
        
    def test_add_car(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'brand': 'test',
            'model': 'test',
            'air_conditioning': 'YES',
            'car_type': self.car_type.id,
            'doors_quantity': 'FIV',
            'people_quantity': 5,
            'fuel_type': 'GAS',
            'transmission_type': 'M',
            'description': 'Opis nowego samochodu',
            'price': 500.00,
        }
        response = self.client.post(reverse('add_car'), data)
        self.assertEqual(response.url, reverse('employee_cars'))
        self.assertTrue(Car.objects.filter(brand='test', model='test').exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Samochód został dodany pomyślnie!')

class EditDeleteCarAndCarTypeTest(TestCase):
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
        
    def test_edit_car(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'brand': 'newtest',
            'model': 'newtest',
            'air_conditioning': 'YES',
            'car_type': self.car_type.id,
            'doors_quantity': 'THR',
            'people_quantity': 3,
            'fuel_type': 'DIE',
            'transmission_type': 'A',
            'description': 'newtest',
            'price': 600.00,
        }
        response = self.client.post(reverse('edit_car', args=[self.car.id]), data)
        self.assertEqual(response.url, reverse('employee_cars'))
        self.car.refresh_from_db()
        self.assertEqual(self.car.brand, 'newtest')
        self.assertEqual(self.car.model, 'newtest')
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Samochód został zedytowany pomyślnie!')
    
    def test_delete_car(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.post(reverse('delete_car', args=[self.car.id]))
        self.assertEqual(response.url, reverse('employee_cars'))
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Samochód został usunięty pomyślnie!')
    
    def test_edit_car_type(self):
        self.client.login(email='test@test.com', password='testpassword')
        data = {
            'name': 'newtest',
            'description': 'newtest',
        }
        response = self.client.post(reverse('edit_car_type', args=[self.car_type.id]), data)
        self.assertEqual(response.url, reverse('employee_car_types'))
        self.car_type.refresh_from_db()
        self.assertEqual(self.car_type.name, 'newtest')
        self.assertEqual(self.car_type.description, 'newtest')
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Typ samochodu został zedytowany pomyślnie!')
    
    def test_delete_car(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.post(reverse('delete_car_type', args=[self.car_type.id]))
        self.assertEqual(response.url, reverse('employee_car_types'))
        self.assertFalse(CarType.objects.filter(id=self.car_type.id).exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Typ samochodu został usunięty pomyślnie!')