from django.shortcuts import render, get_object_or_404, redirect
from .models import Contacto
from .forms import ContactoForm

from django.views.decorators.csrf import csrf_protect

# Create your views here.
def contacto_list(request):
    query = request.GET.get('q', '').strip()
    contactos = Contacto.objects.all()
    if query:
        contactos = contactos.filter(
            nombre__icontains=query
        ) | contactos.filter(
            correo__icontains=query
        ) | contactos.filter(
            telefono__icontains=query
        ) | contactos.filter(
            direccion__icontains=query
        )
    return render(
        request,
        'Agenda/contacto_list.html',
        {'object_list': contactos, 'query': query},
    )

def contacto_detail(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'Agenda/contacto_detail.html', {'object': contacto})

def contacto_create(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacto_list')
        
    else:
        form = ContactoForm()
    return render(request, 'Agenda/contacto_form.html', {'form': form})

def contacto_update(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)

        if form.is_valid():
            form.save()
            return redirect('contacto_list')

    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'Agenda/contacto_form.html', {'form': form})

def contacto_delete(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        contacto.delete()
        return redirect('contacto_list')
    return render(request, 'Agenda/contacto_confirm_delete.html', {'object': contacto})

def filtro_contactos(request):
    return contacto_list(request)