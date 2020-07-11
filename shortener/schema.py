import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import URL

class URLType(DjangoObjectType):
    class Meta:
        model = URL

class Query(graphene.ObjectType):
    urls = graphene.List(URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs):
        queroset = URL.objects.all()

        if url:
            _filter = Q(full_url__icontains=url)
            queroset = queroset.filter(_filter)

        if first:
            queroset = queroset[:first]

        if skip:
            queroset = queroset[skip:]

        return queroset

class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()

    def mutate(self, info, full_url):
        url = URL(full_url=full_url)
        url.save()

        return CreateURL(url=url)

class Mytation(graphene.ObjectType):
    create_url = CreateURL.Field()
