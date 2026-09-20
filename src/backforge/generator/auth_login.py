def generate_login_route() -> str:
    return """import { NextRequest } from "next/server";
import { prisma } from "@/lib/prisma";
import { compare } from "bcryptjs";

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

  const user = await prisma.user.findUnique({
    where: {
      email: body.email,
    },
  });

  if (!user) {
    return Response.json(
      { error: "Invalid email or password" },
      { status: 401 }
    );
  }

  const passwordValid = await compare(
    body.password,
    user.passwordHash
  );

  if (!passwordValid) {
    return Response.json(
      { error: "Invalid email or password" },
      { status: 401 }
    );
  }

  return Response.json(
    {
      id: user.id,
      email: user.email,
      authenticated: true,
    },
    { status: 200 }
  );
}
"""