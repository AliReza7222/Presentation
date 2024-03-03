from slide.serializers import SlideSerializer
from presentation.models import Presentation
from .tags import TagOperations


class GetDataPresentation:
    """
        This code is implemented in order to avoid repeating the logic in
        two places and to follow the principle of DRY.
    """

    @classmethod
    def data_presentation(cls, presentation_obj: Presentation,
        serializer_obj: SlideSerializer, slug_request=False) -> dict:
        if slug_request:
            presentation_obj.increment_views_count()
        slide_queryset = presentation_obj.presentation_slide.all()
        slide_serializer = SlideSerializer(slide_queryset, many=True)
        data = TagOperations.data_with_tags_name(serializer_obj.data)
        data['slides'] = slide_serializer.data
        return data
