# generative-cars

Computing a possible raceline and speed profile given a simple car model. All the project exploits Genetic Algorithms in order to search a suitable solution.

### Info

A Genetic Algorithm approach to the problem of finding a possible raceline and speed profile for a given car model. Project is designed for a 2D track described by a .np file containing: inner_border, outer_border and center_line. Cars improve, generation by generation, their policy until one of them reach the end of the track. Slow laps are penalized but there is a huge bonus for individuals that drive longer before crashing.
