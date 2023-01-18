# Project4 Toolkit

## Features

This toolkit is a reverse engineering tool for the exportation of file formats used in the RAGE Engine built Grand Theft Auto Games.

This includes formats for models, meshes, and world placement conversion to more commonplace file formats, including .obj and .dae.

It also supports the direct conversion of locally stored assets to 2 currently supported game packages: BeamNG.Drive and Assetto Corsa.

It supports proper material mapping for modifications to be done in blender or .3DS MAX, and supports native positional and quaternion rotations normally applied to models during engine runtime. 

## LOD Features
The tool supports the creation of new LOD meshes or the exportation of LOD meshes contained within .wdb libraries with proper matching to the LOD0 model it corresponds to.

## Games Supported
Grand Theft Auto IV (.wpl, .wdr, .wdb)

Grand Theft Auto V (.ymap, .ydr, .ydb)

## Support Planned
Blender GUI support for reading, writing, and repacking to native formats.

Collision model exportation.

Multiple .wpl instance duplication support for .wdrs.

Renderware game support (III, SA, VC).
