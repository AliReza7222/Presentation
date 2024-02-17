from django.http import QueryDict

from presentation.models import Tag


class TagOperations:

    @staticmethod
    def create_list_obj_tags(tag_names: list) -> list:
        tags = list()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(str(tag.id))
        return tags

    @staticmethod
    def get_and_set_tags(data: QueryDict) -> QueryDict:
        tags = data.getlist('tags', [])
        if tags:
            data.setlist('tags', TagOperations.create_list_obj_tags(tag_names=tags))
        else:
            data.setlist('tags', tags)
        return data

    @staticmethod
    def check_relation_tag(tag_id: int) -> bool:
        unique = False
        tag = Tag.objects.get(id=tag_id)
        tag_number_relation = tag.presentation_set.all()
        if len(tag_number_relation) == 1 or len(tag_number_relation) == 0:
            unique = True
        return unique

    @classmethod
    def delete_tag(cls, tags: list) -> None:
        for tag_id in tags:
            if cls.check_relation_tag(tag_id):
                Tag.objects.get(id=tag_id).delete()
