from presentations.models import Tag


class CreateObjectTag:

    @staticmethod
    def create_list_obj_tags(tag_names):
        tags = list()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag.id)
        return tags

    @staticmethod
    def add_tags_valid_data(serilizer_obj, tags):
        valid_data = serilizer_obj.data
        valid_data['tags'] = tags
        return valid_data
