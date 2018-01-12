cmake_minimum_required(VERSION 2.8.9)

project(AlignCrop3DSlicerModule)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/AlignCrop3DSlicerModule")
set(EXTENSION_CATEGORY "Otolaryngology")
set(EXTENSION_CONTRIBUTORS "John Doe (AnyWare Corp.)")
set(EXTENSION_DESCRIPTION "This is an extension that aligns volumes to an ENT clinical reference and crops volumes")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/AlignCrop3DSlicerModule.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/AlignCrop3DSlicerModule/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(AlignCrop3DSlicerModule)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
