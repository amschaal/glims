from guardian.shortcuts import get_users_with_perms, get_groups_with_perms, get_perms, get_objects_for_user
def get_object_permissions(obj):
    perms = {}
    perms['users']=get_users_with_perms(obj, attach_perms=True, with_group_users=False)
    perms['groups']=get_groups_with_perms(obj, attach_perms=True)
    return perms
def get_inherited_objects(obj):
    if hasattr(obj,'inherit_from'):
        return obj.inherit_from()
    else:
        return []
def has_any_permission(user_or_group, obj, permissions):
    all_perms = get_perms(user_or_group, obj)
    for inherit in get_inherited_objects(obj):
        all_perms += get_perms(user_or_group, inherit)
    return len(set(permissions).intersection(all_perms)) > 0

def has_all_permissions(user_or_group, obj, permissions):
    all_perms = get_perms(user_or_group, obj)
    for inherit in get_inherited_objects(obj):
        all_perms += get_perms(user_or_group, inherit)
    for perm in permissions:
        if perm not in all_perms:
            return False
    return True

def get_all_user_objects(user, permissions, klass,use_groups=True,any_perm=False):
    qs = get_objects_for_user(user,permissions,klass,use_groups,any_perm)
    if not hasattr(klass,'get_all_objects'):
        return qs
    params = {klass.__name__: qs.values_list('id', flat=True)}
    for inherited in klass.inherited_classes:
        qs = get_objects_for_user(user,permissions,inherited,use_groups,any_perm)
        params[inherited.__name__]=qs.values_list('id', flat=True)
    return klass.get_all_objects(params)
