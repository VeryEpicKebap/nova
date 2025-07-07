import sys, os,time
components_path = os.path.join(os.getcwd(), "components")
col = os.get_terminal_size().columns
lin = os.get_terminal_size().lines
if os.path.exists(components_path):
    sys.path.insert(0, components_path)
    try:
        print("[ init ] novascr")
        import novascr
    except ImportError:
        print("Failure importing novascr")
        sys.exit()

    try:
        print("[ init ] novaio")
        import novaio
    except ImportError:
        print("Failure importing novaio")
        sys.exit()
else:
    print(f"Components folder not found: {components_path}")
    sys.exit()

