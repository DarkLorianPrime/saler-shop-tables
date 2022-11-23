def get_subdomain(request):
    subdomain = request.get_host().encode().decode("idna").split(".")[0]
    return subdomain if subdomain != "страж" else ""
