from .models import Recipe, Tag


def filter_tags(tag_list):
    tags = {}
    for tag in Tag.objects.all():
        tags[tag.slug] = tag
        if tag.slug in tag_list:
            tag.active = True
    return tags


def filter_list_by_tags(tag_list, objects, recipe_model=None):
    if not tag_list:
        return objects
    if recipe_model:
        return objects.filter(tag__slug__in=tag_list).distinct()
    return objects.filter(recipe__tag__slug__in=tag_list).distinct()
