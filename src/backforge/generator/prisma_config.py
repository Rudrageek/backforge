def generate_prisma_config() -> str:
    """
    Generate Prisma 7 configuration.
    """

    return """import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
"""