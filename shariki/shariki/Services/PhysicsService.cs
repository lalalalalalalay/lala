using System;
using System.Collections.Generic;

namespace BallCollisionWPF
{
    public static class PhysicsService
    {
        // Constants for collision response
        private const double Damping = 2.0;       // energy loss on collision (0..1)
        // Speed cap increased by 30% (previously 600 -> now 780 px/s)
        private const double MaxSpeed = 780.0;

        public static void ApplyForces(Ball ball, List<Ball> allBalls, double width, double height, double dt)
        {
            // 1) Update position from current velocity
            ball.X += ball.VX * dt;
            ball.Y += ball.VY * dt;

            // 2) Wall collisions (elastic with damping)
            if (ball.X - ball.Radius < 0)
            {
                ball.X = ball.Radius;
                ball.VX = -ball.VX * Damping;
            }
            else if (ball.X + ball.Radius > width)
            {
                ball.X = width - ball.Radius;
                ball.VX = -ball.VX * Damping;
            }
            if (ball.Y - ball.Radius < 0)
            {
                ball.Y = ball.Radius;
                ball.VY = -ball.VY * Damping;
            }
            else if (ball.Y + ball.Radius > height)
            {
                ball.Y = height - ball.Radius;
                ball.VY = -ball.VY * Damping;
            }

            // 3) Ball-ball collisions (elastic with damping)
            for (int i = 0; i < allBalls.Count; i++)
            {
                var other = allBalls[i];
                if (other == ball) continue;

                double dx = ball.X - other.X;
                double dy = ball.Y - other.Y;
                double dist = Math.Sqrt(dx * dx + dy * dy);
                double minDist = ball.Radius + other.Radius;

                if (dist > 0 && dist < minDist)
                {
                    // Normalized collision axis
                    double nx = dx / dist;
                    double ny = dy / dist;

                    // Relative velocity along normal
                    double dvx = ball.VX - other.VX;
                    double dvy = ball.VY - other.VY;
                    double relVel = dvx * nx + dvy * ny;

                    // Only apply if balls are moving towards each other
                    if (relVel < 0)
                    {
                        double impulse = -(1 + Damping) * relVel / 2;
                        ball.VX += impulse * nx;
                        ball.VY += impulse * ny;
                        other.VX -= impulse * nx;
                        other.VY -= impulse * ny;
                    }

                    // Separate overlap
                    double overlap = minDist - dist;
                    ball.X += nx * (overlap / 2);
                    ball.Y += ny * (overlap / 2);
                    other.X -= nx * (overlap / 2);
                    other.Y -= ny * (overlap / 2);
                }
            }

            // 4) Speed cap to prevent runaway velocities
            double speed = Math.Sqrt(ball.VX * ball.VX + ball.VY * ball.VY);
            if (speed > MaxSpeed)
            {
                ball.VX = (ball.VX / speed) * MaxSpeed;
                ball.VY = (ball.VY / speed) * MaxSpeed;
            }
        }
    }
}
