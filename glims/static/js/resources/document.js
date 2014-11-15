main.factory('Document', function ($resource) {
  return $resource('/manage/api/documents/:id/', {id:'@id'}, {
    query: { method: 'GET', isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' }
  });
});