import json

PRISMA_VERSION = "7.10.0"


def generate_package_json() -> str:
    package = {
        "name": "backforge-generated-backend",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "build": "next build",
            "dev": "next dev",
            "start": "next start",
            "prisma:generate": "prisma generate",
        },
        "dependencies": {
            "@prisma/client": PRISMA_VERSION,
            "bcryptjs": "3.0.2",
            "next": "15.5.0",
            "react": "19.1.0",
            "react-dom": "19.1.0",
            "@prisma/adapter-pg": "7.10.0",
"pg": "8.16.3",
        },
        "devDependencies": {
            "prisma": PRISMA_VERSION,
            "typescript": "5.9.2",
            "@types/node": "24.3.0",
            "@types/react": "19.1.12",
            "@types/react-dom": "19.1.9",
            "@types/bcryptjs": "2.4.6",
        },
    }

    return json.dumps(package, indent=2)