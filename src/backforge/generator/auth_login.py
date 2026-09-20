import secrets


def generate_login_route() -> str:
    return """import { NextRequest } from "next/server";
import { prisma } from "@/lib/prisma";
import { compare } from "bcryptjs";
import { randomBytes } from "crypto";

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

  const token = randomBytes(32).toString("hex");

  const expiresAt = new Date(
    Date.now() + 7 * 24 * 60 * 60 * 1000
  );

  const session = await prisma.session.create({
    data: {
      token,
      userId: user.id,
      expiresAt,
    },
  });

  const response = Response.json(
    {
      id: user.id,
      email: user.email,
      authenticated: true,
    },
    { status: 200 }
  );

  response.headers.set(
    "Set-Cookie",
    `session_token=${session.token}; HttpOnly; Path=/; Max-Age=604800; SameSite=Lax`
  );

  return response;
}
"""