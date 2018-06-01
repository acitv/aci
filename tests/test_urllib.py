import urllib

aci = {"shows": [], "movies": [], "cable": []}

def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    # return VIDEOS.iterkeys()
    return aci.iterkeys()


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format("plugin://plugin.video.aci/", urllib.urlencode(kwargs))


for item in get_categories():
    print(item)
    print(type(item))
    url = get_url(action="listing", category=item)
    print(url)



