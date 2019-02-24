import json
from products.models import Category, Product
from api.serializers import serialize_product_as_json

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# complete the View below with all REST functionality

# @csrf_exempt
class ProductView(View):
    
    fields = ['name','sku','category','description','price'] 
    
    def _get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if product_id:
            product = self._get_object(product_id)
            if not product:
                return JsonResponse({'Success': False, 'Message':'Could not find product with id {}'.format(product_id)}, status=400)
            else:
                data = serialize_product_as_json(product)
        else:
            qs = Product.objects.all()
            data = [serialize_product_as_json(product) for product in qs]
        return JsonResponse(data, status=200, safe=False)

    def post(self, *args, **kwargs):
        if 'product_id' in kwargs:
            return JsonResponse({'Success': False, 'Message':'Product already exist'}, status=400)
            
        try:
            payload = json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            return JsonResponse({'Success': False, 'Message':'Provide valid Json response'}, status=400)
            
        try:
            product = Product.objects.create(
                name=payload['name'],
                sku=payload['sku'],
                category=payload['category'],
                description=payload['description'],
                price=payload['price']
                )
        except (KeyError, ValueError):
            return JsonResponse({'Success': False, 'Message':'Invalid Response'}, status=400)
            
        data=serialize_product_as_json(product)
        return JsonResponse(data, status=200, safe=False)

    def delete(self, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if not product_id:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
            
        product=self._get_object(product_id)
        if not product:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
        
        product.delete()
        return JsonResponse({'Success':True}, status=201, safe=False)
        
        

    def patch(self, *args, **kwargs):
        fields = ['name','sku','category','description','price']
       
        product_id=kwargs.get('product_id')
        product=self._get_object(product_id)
        
        if not product:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
        
        try:
            payload=json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
        
        
        
        try:
            for field in fields:
                setattr(product, field, payload['field'])
                product.save()
        except ValueError:
            return JsonResponse({'Success':False, 'Message':'Payload provided is invalid'}, status=400)
                
        data = serialize_product_as_json(product)
        return JsonResponse(data, status=200, safe=False)

    def put(self, *args, **kwargs):
        product_id=kwargs.get('product_id')
        product=self._get_object(product_id)
        
        if not product:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
        
        try:
            payload=json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            return JsonResponse({'Success':False, 'Message':'Product does not exist'}, status=400)
        
        try:
            for field in fields:
                setattr(product, field, payload['field'])
                product.save()
        except ValueError:
            return JsonResponse({'Success':False, 'Message':'Payload provided is invalid'}, status=400)
                
        data = serialize_product_as_json(product)
        return JsonResponse(data, status=200, safe=False)
