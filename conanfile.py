# -*- coding: utf-8 -*-

import os

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class LibPclConan(ConanFile):
    name = "pcl"
    version = "1.11.0"  # TODO: change later
    description = (
        "The Point Cloud Library is a standalone, large scale, open project for 2D/3D image and point cloud processing"
    )
    url = "https://github.com/PointCloudLibrary/pcl"
    homepage = "http://www.pointclouds.org/"
    license = "BSD-3-Clause"
    exports = "CMakeLists.txt"
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        # Options for modules
        "module_2d": [True, False],
        "module_cuda": [True, False],
        "module_features": [True, False],
        "module_filters": [True, False],
        "module_geometry": [True, False],
        "module_gpu": [True, False],
        "module_io": [True, False],
        "module_kdtree": [True, False],
        "module_keypoints": [True, False],
        "module_ml": [True, False],
        "module_octree": [True, False],
        "module_outofcore": [True, False],
        "module_people": [True, False],
        "module_recognition": [True, False],
        "module_registration": [True, False],
        "module_sample_consensus": [True, False],
        "module_search": [True, False],
        "module_segmentation": [True, False],
        "module_simulation": [True, False],
        "module_stereo": [True, False],
        "module_surface": [True, False],
        "module_surface_on_nurbs": [True, False],
        "module_tracking": [True, False],
        "module_visualization": [True, False],
        # Options for dependencies
        "with_cuda": [True, False],
        "with_davidsdk": [True, False],
        "with_dssdk": [True, False],
        "with_ensenso": [True, False],
        "with_libpng": [True, False],
        "with_libusb": [True, False],
        "with_opengl": [True, False],
        "with_openni": [True, False],
        "with_openni2": [True, False],
        "with_pcap": [True, False],
        "with_qhull": [True, False],
        "with_qt": [True, False],
        "with_rssdk": [True, False],
        "with_rssdk2": [True, False],
        "with_vtk": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        # TODO: choose which modules are enabled by default
        "module_2d": True,
        "module_cuda": True,
        "module_features": True,
        "module_filters": True,
        "module_geometry": True,
        "module_gpu": True,
        "module_io": True,
        "module_kdtree": True,
        "module_keypoints": True,
        "module_ml": True,
        "module_octree": True,
        "module_outofcore": False,
        "module_people": False,
        "module_recognition": True,
        "module_registration": True,
        "module_sample_consensus": True,
        "module_search": True,
        "module_segmentation": True,
        "module_simulation": False,
        "module_stereo": True,
        "module_surface": True,
        "module_surface_on_nurbs": True,
        "module_tracking": True,
        "module_visualization": False,
        # TODO: choose which options are enabled by default
        "with_cuda": False,
        "with_davidsdk": False,
        "with_dssdk": False,
        "with_ensenso": False,
        "with_libpng": True,
        "with_libusb": False,  # android has to be false
        "with_opengl": False,  # android has to be false
        "with_openni": False,
        "with_openni2": False,
        "with_pcap": False,
        "with_qhull": False,
        "with_qt": False,
        "with_rssdk": False,
        "with_rssdk2": False,
        "with_vtk": False,
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    scm = {
        "type": "git",
        "subfolder": _source_subfolder,
        "url": "https://github.com/PointCloudLibrary/pcl.git",
        "revision": "-".join([name, version]),
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.with_cuda:
            raise ConanInvalidConfiguration("Option 'with_cuda' is not supported yet")
        if self.options.with_davidsdk:
            raise ConanInvalidConfiguration("Option 'with_davidsdk' is not supported yet")
        if self.options.with_dssdk:
            raise ConanInvalidConfiguration("Option 'with_dssdk' is not supported yet")
        if self.options.with_ensenso:
            raise ConanInvalidConfiguration("Option 'with_ensenso' is not supported yet")
        if self.options.with_openni:
            raise ConanInvalidConfiguration("Option 'with_openni' is not supported yet")
        if self.options.with_openni2:
            raise ConanInvalidConfiguration("Option 'with_openni2' is not supported yet")
        if self.options.with_pcap:
            raise ConanInvalidConfiguration("Option 'with_pcap' is not supported yet")
        if self.options.with_qhull:
            raise ConanInvalidConfiguration("Option 'with_qhull' is not supported yet")
        if self.options.with_qt:
            raise ConanInvalidConfiguration("Option 'with_qt' is not supported yet")
        if self.options.with_rssdk:
            raise ConanInvalidConfiguration("Option 'with_rssdk' is not supported yet")
        if self.options.with_rssdk2:
            raise ConanInvalidConfiguration("Option 'with_rssdk2' is not supported yet")
        if self.options.with_vtk:
            raise ConanInvalidConfiguration("Option 'with_vtk' is not supported yet")

        if self.options.module_outofcore:
            raise ConanInvalidConfiguration("Module 'outofcore' is not supported yet")
        if self.options.module_people:
            raise ConanInvalidConfiguration("Module 'people' is not supported yet")
        if self.options.module_simulation:
            raise ConanInvalidConfiguration("Module 'simulation' is not supported yet")
        if self.options.module_visualization:
            raise ConanInvalidConfiguration("Module 'visualization' is not supported yet")

    def source(self):
        # Make sure PCL can find Conan's Boost no matter the version
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "PCLConfig.cmake.in"), "find_package(Boost ", "find_package(Boost) #"
        )

    def requirements(self):
        # Mandatory requirements
        self.requires("boost/1.72.0")
        self.requires("eigen/3.3.7")
        self.requires("flann/1.9.1")

        # Optional requirements
        if self.options.with_libpng:
            self.requires("libpng/1.6.37")
        if self.options.with_libusb:
            self.requires("libusb/1.0.23")

        # Module-dependent requirements
        if self.options.module_simulation:
            self.requires("glew/2.1.0@bincrafters/stable")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)

        # Adjust linking options
        self._cmake.definitions["PCL_SHARED_LIBS"] = self.options.shared
        self._cmake.definitions["PCL_BUILD_WITH_BOOST_DYNAMIC_LINKING_WIN32"] = self.options["boost"].shared
        self._cmake.definitions["PCL_BUILD_WITH_FLANN_DYNAMIC_LINKING_WIN32"] = self.options["flann"].shared
        if self.options.with_qhull:
            self._cmake.definitions["PCL_BUILD_WITH_QHULL_DYNAMIC_LINKING_WIN32"] = self.options["qhull"].shared

        # Do not build extra tooling & options
        self._cmake.definitions["BUILD_all_in_one_installer"] = False
        self._cmake.definitions["BUILD_apps"] = False
        self._cmake.definitions["BUILD_examples"] = False
        self._cmake.definitions["BUILD_global_tests"] = False
        self._cmake.definitions["BUILD_tools"] = False
        self._cmake.definitions["WITH_DOCS"] = False

        # Build modules as needed
        self._cmake.definitions["BUILD_2d"] = self.options.module_2d
        self._cmake.definitions["BUILD_common"] = True  # Always build at least common
        self._cmake.definitions["BUILD_CUDA"] = self.options.module_cuda
        self._cmake.definitions["BUILD_features"] = self.options.module_features
        self._cmake.definitions["BUILD_filters"] = self.options.module_filters
        self._cmake.definitions["BUILD_geometry"] = self.options.module_geometry
        self._cmake.definitions["BUILD_GPU"] = self.options.module_gpu
        self._cmake.definitions["BUILD_io"] = self.options.module_io
        self._cmake.definitions["BUILD_kdtree"] = self.options.module_kdtree
        self._cmake.definitions["BUILD_keypoints"] = self.options.module_keypoints
        self._cmake.definitions["BUILD_ml"] = self.options.module_ml
        self._cmake.definitions["BUILD_octree"] = self.options.module_octree
        self._cmake.definitions["BUILD_outofcore"] = self.options.module_outofcore
        self._cmake.definitions["BUILD_people"] = self.options.module_people
        self._cmake.definitions["BUILD_recognition"] = self.options.module_recognition
        self._cmake.definitions["BUILD_registration"] = self.options.module_registration
        self._cmake.definitions["BUILD_sample_consensus"] = self.options.module_sample_consensus
        self._cmake.definitions["BUILD_search"] = self.options.module_search
        self._cmake.definitions["BUILD_segmentation"] = self.options.module_segmentation
        self._cmake.definitions["BUILD_simulation"] = self.options.module_simulation
        self._cmake.definitions["BUILD_stereo"] = self.options.module_stereo
        self._cmake.definitions["BUILD_surface"] = self.options.module_surface
        self._cmake.definitions["BUILD_surface_on_nurbs"] = self.options.module_surface_on_nurbs
        self._cmake.definitions["BUILD_tracking"] = self.options.module_tracking
        self._cmake.definitions["BUILD_visualization"] = self.options.module_visualization

        # Configure dependencies as needed
        self._cmake.definitions["WITH_CUDA"] = self.options.with_cuda
        self._cmake.definitions["WITH_DAVIDSDK"] = self.options.with_davidsdk
        self._cmake.definitions["WITH_DSSDK"] = self.options.with_dssdk
        self._cmake.definitions["WITH_ENSENSO"] = self.options.with_ensenso
        self._cmake.definitions["WITH_LIBUSB"] = self.options.with_libusb
        self._cmake.definitions["WITH_OPENGL"] = self.options.with_opengl
        self._cmake.definitions["WITH_OPENNI"] = self.options.with_openni
        self._cmake.definitions["WITH_OPENNI2"] = self.options.with_openni2
        self._cmake.definitions["WITH_PCAP"] = self.options.with_pcap
        self._cmake.definitions["WITH_PNG"] = self.options.with_libpng
        self._cmake.definitions["WITH_QHULL"] = self.options.with_qhull
        self._cmake.definitions["WITH_QT"] = self.options.with_qt
        self._cmake.definitions["WITH_RSSDK"] = self.options.with_rssdk
        self._cmake.definitions["WITH_RSSDK2"] = self.options.with_rssdk2
        self._cmake.definitions["WITH_VTK"] = self.options.with_vtk

        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        cmake.patch_config_paths()

        self.copy("LICENSE.txt", src=self._source_subfolder, dst="licenses")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "PCL"
        self.cpp_info.names["cmake_find_package_multi"] = "PCL"
        self.cpp_info.libs = tools.collect_libs(self)

        # version_short = ".".join(self.version.split(".")[:2])
        # self.cpp_info.includedirs = ["include/pcl-{}".format(version_short)]
