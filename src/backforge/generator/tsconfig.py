import json


def generate_tsconfig() -> str:
    """
    Generate TypeScript configuration for the
    BackForge-generated Next.js backend.
    """

    config = {
        "compilerOptions": {
            "target": "ES2017",
            "lib": [
                "dom",
                "dom.iterable",
                "esnext",
            ],
            "allowJs": False,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,

            "plugins": [
                {
                    "name": "next"
                }
            ],

            "baseUrl": ".",
            "paths": {
                "@/*": [
                    "./src/*"
                ]
            },
        },
        "include": [
            "next-env.d.ts",
            ".next/types/**/*.ts",
            "**/*.ts",
            "**/*.tsx",
        ],
        "exclude": [
            "node_modules",
        ],
    }

    return json.dumps(
        config,
        indent=2,
    )