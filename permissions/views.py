from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.template.context import RequestContext
from guardian.shortcuts import assign_perm, get_perms, remove_perm
from forms import PermissionForm, UserForm, GroupForm
from django.conf import settings
from permissions.manage import get_object_permissions, get_inherited_objects
# Create your views here.
def manage_permissions(request, model, pk):
    ct = ContentType.objects.get(model=model)
    klass = ct.model_class()
    obj = klass.objects.get(pk=pk)
    inherited = get_inherited_objects(obj)
    user_form = UserForm()
    group_form = GroupForm()
    permissions = get_object_permissions(obj)
    for k,v in permissions['groups'].items():
        print k
        print v
    users = User.objects.all()
    return render(request, settings.PERMISSIONS_APP['manage_template'], {'user_form':user_form,'group_form':group_form,'obj':obj,'permissions':permissions,'users':users,'model':model,'inherited':inherited} ,context_instance=RequestContext(request))
    
    
def manage_user_permissions(request, model, pk, user_id):
    ct = ContentType.objects.get(model=model)
    klass = ct.model_class()
    obj = klass.objects.get(pk=pk)
    user = User.objects.get(pk=user_id)
    permissions = get_perms(user,obj)
    form = PermissionForm(initial={'permissions':permissions},model=klass)
    status = ''
    if request.method == 'POST':
        form = PermissionForm(request.POST,model=klass)
        if form.is_valid():
            removed = list(set(permissions) - set(form.cleaned_data['permissions']))
            added = list(set(form.cleaned_data['permissions']) - set(permissions))
            for perm in removed:
                remove_perm(perm,user,obj)
            for perm in added:
                assign_perm(perm,user,obj)
            status = 'Permissions have been successfully updated'
        else:
            status = 'There was an error with assigning permissions'
    return render(request, settings.PERMISSIONS_APP['manage_user_template'], {'form':form,'obj':obj, 'model':model,'user':user,'status':status}, context_instance=RequestContext(request))

def manage_group_permissions(request, model, pk, group_id):
    ct = ContentType.objects.get(model=model)
    klass = ct.model_class()
    obj = klass.objects.get(pk=pk)
    group = Group.objects.get(pk=group_id)
    permissions = get_perms(group,obj)
    form = PermissionForm(initial={'permissions':permissions},model=klass)
    status = ''
    if request.method == 'POST':
        form = PermissionForm(request.POST,model=klass)
        if form.is_valid():
            removed = list(set(permissions) - set(form.cleaned_data['permissions']))
            added = list(set(form.cleaned_data['permissions']) - set(permissions))
            for perm in removed:
                remove_perm(perm,group,obj)
            for perm in added:
                assign_perm(perm,group,obj)
            status = 'Permissions have been successfully updated'
        else:
            status = 'There was an error with assigning permissions'
    return render(request, settings.PERMISSIONS_APP['manage_group_template'], {'form':form,'obj':obj, 'model':model,'group':group,'status':status}, context_instance=RequestContext(request))