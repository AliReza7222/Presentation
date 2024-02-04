from presentations.models import Tag


class TagObject:

    @staticmethod
    def create_list_obj_tags(tag_names):
        tags = list()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(str(tag.id))
        return tags

    @staticmethod
    def add_tags_valid_data(serilizer_obj, tags):
        valid_data = serilizer_obj.data
        valid_data['tags'] = tags
        return valid_data

    def check_unique_tag(self, tag_id):
        unique = False
        tag = Tag.objects.get(id=tag_id)
        if len(tag.presentation_set.all()) == 1:
            unique = True
        return unique

    def delete_unique_tag(self, tags):
        for tag_id in tags:
            if self.check_unique_tag(tag_id):
                Tag.objects.get(id=tag_id).delete()
