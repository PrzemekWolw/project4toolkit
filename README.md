# Project4: Toolkit
![Untitled](https://user-images.githubusercontent.com/122072742/216810478-9a70e817-377e-4f21-baff-9e35a2bbb7d3.png)

## Features

This toolkit is a tool for the exportation of file formats used in the RAGE Engine built Grand Theft Auto Games.

This includes formats for models, meshes, and world placement conversion to more commonplace file formats, including .obj and .dae.


It also supports the direct conversion of locally stored assets to 2 currently supported game packages: BeamNG.Drive and Assetto Corsa.

It supports proper material mapping for modifications to be done in blender or .3DS MAX, and supports native positional and quaternion rotations normally applied to models during engine runtime. 

## LOD Features
The tool supports the creation of new LOD meshes or the exportation of LOD meshes contained within .wdb libraries with proper matching to the LOD0 model it corresponds to.

## Requirements
Python 3.11

Blender 3.4

OpenIV

Grand Theft Auto IV (1.0.4.0 - Complete Edition Steam/RGL) [Must have a valid license and non-pirated version, it will check the hash and .exe, there is no way of circumventing this, buy the game.]

## Games Supported
Grand Theft Auto IV (.wpl, .wdr, .wdb)

Grand Theft Auto V (.ymap, .ydr, .ydb)

## Support Planned
Blender GUI support for reading, writing, and repacking to native formats.

Collision model exportation.

Multiple .wpl instance duplication support for .wdrs.

Renderware game support (III, SA, VC).
