def compare_api_contracts(
    frontend_routes: list[dict],
    backend_routes: list[dict],
) -> dict:
    """
    Compare frontend API requirements with
    backend API implementations.
    """

    frontend_set = {
        (
            route["method"].upper(),
            route["endpoint"],
        )
        for route in frontend_routes
    }

    backend_set = {
        (
            route["method"].upper(),
            route["endpoint"],
        )
        for route in backend_routes
    }

    implemented = frontend_set & backend_set
    missing = frontend_set - backend_set
    extra = backend_set - frontend_set

    return {
        "implemented": [
            {
                "method": method,
                "endpoint": endpoint,
            }
            for method, endpoint in sorted(
                implemented
            )
        ],
        "missing": [
            {
                "method": method,
                "endpoint": endpoint,
            }
            for method, endpoint in sorted(
                missing
            )
        ],
        "extra": [
            {
                "method": method,
                "endpoint": endpoint,
            }
            for method, endpoint in sorted(
                extra
            )
        ],
    }