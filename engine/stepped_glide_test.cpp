// stepped_glide_test.cpp -- checks for stepped_glide.h (run_glide_test.bat)
#include "stepped_glide.h"
#include <cstdio>
#include <cstdlib>

static int fails = 0;
static void check(bool ok, const char* what)
{
	std::printf("%s  %s\n", ok ? "ok  " : "FAIL", what);
	if (!ok) ++fails;
}

typedef float M34[3][4];

static void yawPose(M34& m, double deg, double x, double y, double z)
{
	const double a = deg * 3.14159265358979323846 / 180.0;
	m[0][0] = (float)cos(a);  m[0][1] = 0; m[0][2] = (float)sin(a); m[0][3] = (float)x;
	m[1][0] = 0;              m[1][1] = 1; m[1][2] = 0;             m[1][3] = (float)y;
	m[2][0] = (float)-sin(a); m[2][1] = 0; m[2][2] = (float)cos(a); m[2][3] = (float)z;
}

static double maxDiff(const M34& a, const M34& b)
{
	double d = 0;
	for (int r = 0; r < 3; ++r) for (int c = 0; c < 4; ++c) { double e = fabs(a[r][c] - b[r][c]); if (e > d) d = e; }
	return d;
}

int main()
{
	// 1. matrix -> pose -> matrix gives the same matrix, for rotations in every quadrant
	{
		double worst = 0;
		for (int deg = -180; deg <= 180; deg += 15)
		{
			M34 a, b; yawPose(a, deg, 0.1, 1.2, -0.3);
			sgl::ToMatrix(sgl::FromMatrix(a), b);
			double d = maxDiff(a, b); if (d > worst) worst = d;
		}
		check(worst < 1e-5, "matrix -> pose -> matrix round trip");
	}
	// 2. a hand that does not move: the gun does not move
	{
		sgl::Glide g; M34 a; yawPose(a, 30, 0, 1, 0);
		const sgl::Pose live = sgl::FromMatrix(a);
		double worst = 0;
		for (int f = 0; f < 180; ++f)
		{
			const sgl::Pose& s = g.Update(live, f / 90.0, 10, 100);
			for (int i = 0; i < 3; ++i) { double e = fabs(s.pos[i] - live.pos[i]); if (e > worst) worst = e; }
		}
		check(worst < 1e-9, "still hand = still gun");
	}
	// 3. a hand moving steadily at 1 m/s, 90 frames a second, 10 steps a second:
	//    the biggest move in one frame stays small (no teleport), where the old freeze-and-jump
	//    moved a whole step (10 cm) in one frame; and the gun never falls further behind than two steps.
	{
		sgl::Glide g; double prev = 0, biggest = 0, behind = 0; bool moved = false;
		for (int f = 0; f < 900; ++f)
		{
			const double t = f / 90.0;
			sgl::Pose live{}; live.rot = { 1, 0, 0, 0 }; live.pos[0] = t;	// 1 m/s along x
			const double x = g.Update(live, t, 10, 100).pos[0];
			if (f > 30)
			{
				if (fabs(x - prev) > biggest) biggest = fabs(x - prev);
				if (t - x > behind) behind = t - x;
				if (x != prev) moved = true;
			}
			prev = x;
		}
		std::printf("      biggest move in one frame %.1f mm (a jump would be 100 mm), furthest behind %.0f mm\n", biggest * 1000, behind * 1000);
		check(biggest < 0.020, "no frame moves the gun more than 2 cm at 1 m/s");
		check(behind < 0.21, "never more than two steps behind");
		check(moved, "the gun does follow");
	}
	// 4. the hand stops: the gun arrives exactly, within two steps
	{
		sgl::Glide g; sgl::Pose a{}; a.rot = { 1, 0, 0, 0 }; sgl::Pose b = a; b.pos[2] = 0.5;
		g.Update(a, 0.0, 10, 100);
		double z = 0;
		for (int f = 1; f <= 27; ++f) z = g.Update(b, f / 90.0, 10, 100).pos[2];	// 0.3 s
		check(fabs(z - 0.5) < 1e-9, "arrives exactly where the hand stopped");
	}
	// 5. a turn takes the short way round (170 -> -170 degrees is 20 degrees, not 340)
	{
		M34 a, b; yawPose(a, 170, 0, 0, 0); yawPose(b, -170, 0, 0, 0);
		M34 mid; sgl::ToMatrix(sgl::Blend(sgl::FromMatrix(a), sgl::FromMatrix(b), 0.5), mid);
		M34 want; yawPose(want, 180, 0, 0, 0);
		check(maxDiff(mid, want) < 1e-5, "rotation blends the short way round");
	}
	// 6. a long pause (menu, loading) does not become a glide across the room
	{
		sgl::Glide g; sgl::Pose a{}; a.rot = { 1, 0, 0, 0 }; sgl::Pose b = a; b.pos[0] = 3;
		g.Update(a, 0.0, 10, 100);
		check(fabs(g.Update(b, 5.0, 10, 100).pos[0] - 3) < 1e-12, "after a long pause the gun is simply at the hand");
	}
	// 7. glide 50 %: the gun has arrived by the middle of the step and rests
	{
		sgl::Glide g; sgl::Pose a{}; a.rot = { 1, 0, 0, 0 }; sgl::Pose b = a; b.pos[0] = 1;
		g.Update(a, 0.0, 10, 50);
		g.Update(b, 0.10, 10, 50);										// new step starts
		const double atHalf = g.Update(b, 0.15, 10, 50).pos[0];
		const double later = g.Update(b, 0.19, 10, 50).pos[0];
		check(fabs(atHalf - 1) < 1e-9 && fabs(later - 1) < 1e-9, "glide 50 %: arrived by half the step, then resting");
	}
	std::printf(fails ? "\n%d FAILED\n" : "\nall passed\n", fails);
	return fails ? 1 : 0;
}
