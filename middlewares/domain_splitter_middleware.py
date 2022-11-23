def splitter_middleware(get_response):
    """
    Deprecated

    :param get_response:
    :return:
    """
    def middleware(request):
        full_domain = request.get_host()
        domain_pieces = full_domain.split(".")
        print(full_domain)
        request.subdomain = domain_pieces[0] if domain_pieces else None

        return get_response(request)

    return middleware
