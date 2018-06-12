box_filters = {
    'length_more_than': 'length__gte',
    'length_less_than': 'length__lt',
    'breadth_more_than': 'breadth__gte',
    'breadth_less_than': 'breadth__lt',
    'height_more_than': 'height__gte',
    'height_less_than': 'height__lt',
    'area_more_than': 'area__gte',
    'area_less_than': 'area__lte',
    'volume_more_than': 'volume__gte',
    'volume_less_than': 'volume__lt',
    'created_by': 'created_by__username',
    'created_after': 'created_at__gte',
    'created_before': 'created_at__lt'
}

staff_user_params = ('id', 'length', 'width', 'height', 'last_updated', 'area', 'volume', 'created_by')
user_params = ('id', 'length', 'width', 'height', 'area', 'volume')