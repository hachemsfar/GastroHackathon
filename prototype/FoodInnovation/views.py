import json
import ast
import copy
import textrazor


import logging
import logging.handlers

from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from speech_reco.models import FoodModel

def treatText(text):
	textrazor.api_key = "15b0ce0c761517455672468148c24823dbaf06f0c67eda66d1cf4a7e"

	client = textrazor.TextRazor(extractors=["words", "entities","dependency-trees"])
	response = client.analyze(text)

	with_dict = {"with", "add", "some", "want"}
	without_dict = {"without", "remove", "no"}

	food_entities = []
	for entity in response.entities():
		food_entities.append({"entity" : entity.id.lower(), "type" : entity.freebase_types, "with" : 0 })



	graph_dependency = {}
	for word in response.words():
		graph_dependency[word.token.lower()] = word.parent_position

	for entity in food_entities:
		parent_position = 0
		word = entity["entity"]
		parent_position = graph_dependency[word]
		while (parent_position != None):
			
			keys = list(graph_dependency.keys())
			parent_word = keys[parent_position]
			if parent_word in with_dict:
				entity["with"] = 1
				break
			elif parent_word in without_dict:
				entity["with"] = -1
				break
			word = parent_word
			parent_position = graph_dependency[word]

	return food_entities

def success(request):
	messages.success(request, 'Order placed successfully.')
	return redirect("home")

def home(request):

	if 'GET' == request.method:
		context = {}
	return render(request,"speech_reco.html", context)


def confirm_order(request):
	if 'GET' == request.method:
		recievedData = request.GET.get('data')

		print(recievedData)
		
		ingredients_list = []
		dishObj = None
		Note = ''

		try:
			result = treatText(recievedData)
			ingredients = FoodModel.objects.filter(type='Ingredient')
			for ing in ingredients:
				ingredients_list.append({'obj':ing, 'with':-1})
			
			for element in result:
				
				print(element['entity'])

				
				foodName = element['entity']
				foodObjs =  FoodModel.objects.filter(name__icontains=foodName)
				if len(foodObjs) == 0:
					Note+=foodName +', '
				else:
					foodObj = foodObjs[0]
					if 'Dish' == foodObj.type:
						dishObj = foodObj
					elif 'Ingredient' == foodObj.type:

						for elem in ingredients_list:

							if elem['obj'].name == foodObj.name:
								elem['with'] = element['with']
						
		except:
			pass


		context = {'recievedData':recievedData,
					'ingredients_list':ingredients_list,
					'dish':dishObj,
					'Note':Note
		}
		return render(request,"confirm_order.html", context)
	else:
		context = {}
		return render(request,"confirm_order.html", context)
