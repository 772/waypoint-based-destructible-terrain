# waypoint_based_destructible_terrain

waypoint_based_destructible_terrain is a small techdemo showcasing an artificial intelligence (AI)-compatible destructible terrain designed for side-scrolling games. The functionality is achieved through the implementation of a dynamic waypoint network, utilized concurrently for AI player navigation and landscape rendering.

Why? In the context of destructible two-dimensional (2D) landscapes, conventional methodologies involve the usage of either a vast grid comprising individual pixels (bitmap) or a polygon-based approach. Techniques such as marching squares or quadtrees are often employed to enhance these approaches. However, both approaches (bitmaps and polygons) encounter challenges when moving AI players within an unstable environment.

## Preview

https://github.com/772/waypoint_based_destructible_terrain/assets/13351564/2e215245-0819-42ef-a44e-eef445ed8d73

## Build

```
git clone https://github.com/772/waypoint_based_destructible_terrain
pip install pygame
python waypoint_based_destructible_terrain/waypoint_based_destructible_terrain.py
```
