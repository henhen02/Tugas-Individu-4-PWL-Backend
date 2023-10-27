def add_rules(userid, request):
    return [f'{request.jwt_claims.get("role", [])}']
