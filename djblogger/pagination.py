from django.core.paginator import Paginator


def paginate_queryset(request, queryset, num_items):
    paginator = Paginator(queryset, num_items)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
