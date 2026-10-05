from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class ProductoModelTests(TestCase):
    def test_producto_no_permite_precio_negativo(self):
        producto = Producto(nombre='Teclado', precio=-1, stock=1)
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_producto_no_permite_stock_negativo(self):
        producto = Producto(nombre='Mouse', precio=10, stock=-1)
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_producto_ordenado_por_nombre(self):
        Producto.objects.create(nombre='Zeta', precio=1, stock=1)
        Producto.objects.create(nombre='Alfa', precio=1, stock=1)
        nombres = list(Producto.objects.values_list('nombre', flat=True))
        self.assertEqual(nombres, ['Alfa', 'Zeta'])


class ProductoViewTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Notebook',
            precio=500,
            descripcion='16GB RAM',
            stock=5,
        )

    def test_producto_list(self):
        response = self.client.get(reverse('producto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notebook')

    def test_producto_detail(self):
        response = self.client.get(reverse('producto_detail', args=[self.producto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notebook')

    def test_producto_create_get(self):
        response = self.client.get(reverse('producto_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_producto_create_post_valido(self):
        response = self.client.post(
            reverse('producto_create'),
            {'nombre': 'Monitor', 'precio': 150, 'descripcion': '24"', 'stock': 2},
        )
        self.assertRedirects(response, reverse('producto_list'))
        self.assertTrue(Producto.objects.filter(nombre='Monitor').exists())

    def test_producto_create_post_invalido_re_renderiza_formulario(self):
        response = self.client.post(
            reverse('producto_create'),
            {'nombre': 'Monitor', 'precio': -10, 'descripcion': '24"', 'stock': 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('precio', response.context['form'].errors)

    def test_producto_update_post_valido(self):
        response = self.client.post(
            reverse('producto_update', args=[self.producto.pk]),
            {'nombre': 'Notebook Pro', 'precio': 600, 'descripcion': '32GB RAM', 'stock': 3},
        )
        self.assertRedirects(response, reverse('producto_list'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Notebook Pro')

    def test_producto_update_post_invalido_re_renderiza_formulario(self):
        response = self.client.post(
            reverse('producto_update', args=[self.producto.pk]),
            {'nombre': 'Notebook', 'precio': 500, 'descripcion': '16GB RAM', 'stock': -1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('stock', response.context['form'].errors)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 5)

    def test_producto_delete_post_elimina_y_redirige(self):
        response = self.client.post(reverse('producto_delete', args=[self.producto.pk]))
        self.assertRedirects(response, reverse('producto_list'))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
