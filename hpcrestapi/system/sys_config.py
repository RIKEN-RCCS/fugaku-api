import importlib

def load_system_function(system_type):
    global system
    system = importlib.import_module(f"hpcrestapi.system.{system_type}")
