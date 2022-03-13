from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.views.generic import ( ListView , 
                    CreateView , 
                    UpdateView , 
                    DeleteView ,)
from .models import ToDoList, ToDoItem


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"



class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_items.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ['title']

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context['title'] = 'Add a new ToDo list'
        return context 

class ItemCreate(CreateView):
    model = ToDoItem
    fields =[
        'title',
        'description',
        'due_date',
        'todo_list',
    ]

    # get initial and get context data are overriden to provide useful information to the templates 
    
    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new ToDo item"
        return context
    
    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

         # after success, it reverses to the list of other items associated with that list 
    def get_success_url(self) -> str:
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields =[
        'title',
        'description',
        'due_date',
        'todo_list',
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList
    # better to use reverse_lazy instead of urls as the files are not loaded when the file is imported 
    success_url = reverse_lazy('index') # it goes back to index.html 

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context