from cors import add_cors_headers


def create_api_blueprints(manager, models):
    blueprints = []

    for model in models:
        options = {
            'model': model,
            'methods': ['GET', 'PUT', 'POST', 'DELETE']
        }

        blueprint = manager.create_api_blueprint(**options)
        blueprint.after_request(add_cors_headers)

        blueprints.append(blueprint)

    return blueprints