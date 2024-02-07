from presentation.models import Tag


class TagObject:

    def create_list_obj_tags(self, tag_names):
        tags = list()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(str(tag.id))
        return tags

    def add_tags_valid_data(self, serilizer_obj, tags):
        valid_data = serilizer_obj.data
        valid_data['tags'] = tags
        return valid_data

    def get_and_set_tags(self, data):
        tags = data.pop('tags', [])
        if tags:
            data.setlist('tags', self.create_list_obj_tags(tag_names=tags))
        return data, tags

    def check_relation_tag(self, tag_id):
        unique = False
        tag = Tag.objects.get(id=tag_id)
        tag_number_relation = tag.presentation_set.all()
        if len(tag_number_relation) == 1 or len(tag_number_relation) == 0:
            unique = True
        return unique

    def delete_tag(self, tags):
        for tag_id in tags:
            if self.check_relation_tag(tag_id):
                Tag.objects.get(id=tag_id).delete()
