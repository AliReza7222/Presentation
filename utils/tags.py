from django.http import QueryDict

from presentation.models import Tag


class TagOperations:
    """
        This code performs tasks related to tags,
        such as creating and deleting tags or returning tag information.
    """

    @staticmethod
    def create_list_obj_tags(tag_names: list) -> list:
        tags = list()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(str(tag.id))
        return tags

    @classmethod
    def get_tags(cls, data: dict) -> dict:
        tags = data.pop('tags', [])
        if tags:
            tags = cls.create_list_obj_tags(tags)
        return data, tags

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

    @classmethod
    def data_with_tags_name(cls, data: dict) -> dict:
        tag_ids = data.get('tags', [])
        tags = [Tag.objects.get(id=tag_id).name for tag_id in tag_ids]
        data['tags'] = tags
        return data
