def generate_register_route() -> str:
    """
    Generate a Next.js email/password registration route.
    """

    return """import { NextRequest } from "next/server";
import { prisma } from "@/lib/prisma";
import { hash } from "bcryptjs";

export async function POST(
  request: NextRequest
) {
  const body = await request.json();

  if (!body.email) {
    return Response.json(
      { error: "email is required" },
      { status: 400 }
    );
  }

  if (!body.password) {
    return Response.json(
      { error: "password is required" },
      { status: 400 }
    );
  }

  const existingUser = await prisma.user.findUnique({
    where: {
      email: body.email,
    },
  });

  if (existingUser) {
    return Response.json(
      { error: "User already exists" },
      { status: 409 }
    );
  }

  const passwordHash = await hash(
    body.password,
    12
  );

  const user = await prisma.user.create({
    data: {
      email: body.email,
      passwordHash,
    },
    select: {
      id: true,
      email: true,
    },
  });

  return Response.json(
    user,
    { status: 201 }
  );
}
"""