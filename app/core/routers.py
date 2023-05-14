#app/core/routers.py
import importlib
from pathlib import Path

def discover_routers():
    api_dir = Path(__file__).parent.parent / "api"
    router_files = list(api_dir.rglob('router.py'))
    routers = []

    # Sort router files so 'user' and 'auth' are first
    sorted_router_files = sorted(
        router_files,
        key=lambda x: (x.parent.stem != 'user', x.parent.stem != 'auth', x)
    )
    for router_file in sorted_router_files:
        relative_path = router_file.parent.relative_to(api_dir)  # get the relative path to the api folder
        module_path = "app.api." + str(relative_path).replace("/", ".").replace('\\','.')  # make sure it works on Windows too
        router_module = importlib.import_module(f"{module_path}.router")
        for router in router_module.routers:
            routers.append(router)  # change this line

    return routers

def setup_routers(app):
    # generate file route
    for router in discover_routers():
        app.include_router(router)
