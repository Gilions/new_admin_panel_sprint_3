from config.settings import PAGINATION_SIZE
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.all().values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True
            ),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='actor'),
                distinct=True
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='director'),
                distinct=True
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role='writer'),
                distinct=True
            )
        )
        return queryset

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, _ = self.paginate_queryset(self.get_queryset(), self.paginate_by)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)['object']
        return context
