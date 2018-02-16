cmake_minimum_required(VERSION 2.8.9)

project(AlignCrop3DSlicerExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/Ear3DSlicerExtension")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "John Eniolu (HML & SKA Lab.)")
set(EXTENSION_DESCRIPTION "This is the Auditory Medical Biophysics Extension")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/Ear3DSlicerExtension.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/AlignCrop3DSlicerExtension/Screenshots/1.png")
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
