from pathlib import Path

def discover_routers():
    api_dir = Path(__file__).parent.parent / "api"
    router_files = list(api_dir.rglob('router.py'))
    routers = []

    for router_file in router_files:
        relative_path = router_file.parent.relative_to(Path(__file__).parent.parent)
        module_path = str(relative_path).replace("/", ".")
        router_module = __import__(f"{module_path}.router", fromlist=["router"])
        routers.append((router_module.router, f"/api"))

    return routers

def setup_routers(app):
    for router, prefix in discover_routers():
        app.include_router(router, prefix=prefix)

