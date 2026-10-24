import os


def launch_application(app):
    try:
        os.startfile(app["path"])
        return True, None

    except Exception as error:
        return False, str(error)


def launch_workspace(applications):

    results = []

    for app in applications:

        if app["variable"].get():

            success, error = launch_application(app)

            results.append({
                "name": app["name"],
                "success": success,
                "error": error
            })

    return results