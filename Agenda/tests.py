from django.test import TestCase
from django.urls import reverse

from .models import Contacto


class ContactoModelTests(TestCase):
    def test_contacto_telefono_tiene_default(self):
        contacto = Contacto(nombre='Ana')
        self.assertEqual(contacto.telefono, '+56 9 ')


class ContactoViewTests(TestCase):
    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre='Juan Perez',
            telefono='+56 9 12345678',
            correo='juan@example.com',
            direccion='Santiago',
        )
        self.otro_contacto = Contacto.objects.create(
            nombre='Maria Gomez',
            telefono='+56 9 99999999',
            correo='maria@example.com',
            direccion='Valparaiso',
        )

    def test_contacto_list(self):
        response = self.client.get(reverse('contacto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Perez')
        self.assertContains(response, 'Maria Gomez')

    def test_contacto_detail(self):
        response = self.client.get(reverse('contacto_detail', args=[self.contacto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'juan@example.com')

    def test_contacto_create_get(self):
        response = self.client.get(reverse('contacto_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_contacto_create_post_valido(self):
        response = self.client.post(
            reverse('contacto_create'),
            {
                'nombre': 'Pedro Soto',
                'telefono': '+56 9 88888888',
                'correo': 'pedro@example.com',
                'direccion': 'Concepcion',
            },
        )
        self.assertRedirects(response, reverse('contacto_list'))
        self.assertTrue(Contacto.objects.filter(nombre='Pedro Soto').exists())

    def test_contacto_create_post_invalido_re_renderiza_formulario(self):
        response = self.client.post(
            reverse('contacto_create'),
            {
                'nombre': 'Pedro Soto',
                'telefono': '+56 9 88888888',
                'correo': 'correo-invalido',
                'direccion': 'Concepcion',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('correo', response.context['form'].errors)

    def test_contacto_update_post_valido(self):
        response = self.client.post(
            reverse('contacto_update', args=[self.contacto.pk]),
            {
                'nombre': 'Juan Actualizado',
                'telefono': '+56 9 12345678',
                'correo': 'juan@example.com',
                'direccion': 'Santiago Centro',
            },
        )
        self.assertRedirects(response, reverse('contacto_list'))
        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.nombre, 'Juan Actualizado')

    def test_contacto_update_post_invalido_re_renderiza_formulario(self):
        response = self.client.post(
            reverse('contacto_update', args=[self.contacto.pk]),
            {
                'nombre': '',
                'telefono': '+56 9 12345678',
                'correo': 'juan@example.com',
                'direccion': 'Santiago',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('nombre', response.context['form'].errors)

    def test_contacto_delete_post_elimina_y_redirige(self):
        response = self.client.post(reverse('contacto_delete', args=[self.contacto.pk]))
        self.assertRedirects(response, reverse('contacto_list'))
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())

    def test_contacto_busqueda_filtra_resultados(self):
        response = self.client.get(reverse('contacto_list'), {'q': 'maria@example.com'})
        self.assertEqual(response.status_code, 200)
        contactos = list(response.context['object_list'])
        self.assertEqual(len(contactos), 1)
        self.assertEqual(contactos[0].pk, self.otro_contacto.pk)

    def test_filtro_contactos_usa_misma_logica(self):
        response = self.client.get(reverse('filtro_contactos'), {'q': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Perez')
