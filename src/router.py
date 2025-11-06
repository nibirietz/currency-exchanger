from parse import compile


class Router:
    def __init__(self):
        self.routes = {}
        self.pattern_routes = []

    def route(self, method: str, path: str):
        def decorator(func):
            if '{' in path or '}' in path:
                parser = compile(path)
                self.pattern_routes.append(
                    {
                        "parser": parser,
                        "function": func,
                        "method": method,
                        "path": path,
                    }
                )

            self.routes[(method, path)] = func

            return func

        return decorator
