cl__1 = 1e+22;
Point(1) = {0.5, 0, 0, 1e+22};
Point(2) = {0, 0, 0, 1e+22};
Point(3) = {0.5, 0.006, 0, 1e+22};
Point(4) = {0.015, 0.006, 0, 1e+22};
Point(5) = {0, 0.006, 0, 1e+22};
Point(6) = {0.015, 0.011, 0, 1e+22};
Point(7) = {0, 0.011, 0, 1e+22};
Point(12) = {0.015, 0.0125, 0, 1e+22};
Point(13) = {0.0015, 0.0125, 0, 1e+22};
Point(14) = {0.0015, 0.046, 0, 1e+22};
Point(15) = {0.5, 0.046, 0, 1e+22};
Point(18) = {0, 0.0475, 0, 1e+22};
Point(24) = {0.5, 0.0475, 0, 1e+22};
Line(1) = {1, 2};
Line(2) = {3, 1};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {2, 5};
Line(6) = {6, 7};
Line(7) = {5, 7};
Line(9) = {4, 6};
Line(11) = {12, 6};
Line(12) = {13, 12};
Line(13) = {14, 13};
Line(14) = {15, 14};
Line(24) = {18, 24};
Line(15) = {15, 3};
Line(17) = {7, 18};
Line(23) = {24, 15};
Line Loop(2) = {1, 5, -4, -3, 2};
Plane Surface(2) = {1};
Line Loop(1) = {6, -7, -4, 9};
Plane Surface(1) = {2};
Line Loop(3) = {-9, -3, -15, 14, 13, 12, 11};
Plane Surface(3) = {3};
Line Loop(4) = {17, 24, 23, 14, 13, 12, 11, 6};
Plane Surface(4) = {4};
