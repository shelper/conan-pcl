import os

from conans import ConanFile, CMake, tools


class LibPCLConan(ConanFile):
    name = "pcl"
    version = "1.11.0"

    exports = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "cuda": ["9.2", "10.0", "10.1", "None"]}
    default_options = ["shared=True", "fPIC=True", "cuda=None"]
    default_options = tuple(default_options)
    license = "BSD License"
    description = "The Point Cloud Library is for 2D/3D image and point cloud processing."
    source_subfolder = "source_subfolder"
    short_paths = True

    scm = {
        "type": "git",
        "subfolder": source_subfolder,
        "url": "https://github.com/PointCloudLibrary/pcl.git",
        "revision": "-".join([name, version]),
    }

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):

        if "CI" not in os.environ:
            os.environ["CONAN_SYSREQUIRES_MODE"] = "verify"

    def requirements(self):
        self.requires("boost/1.72.0")
        self.requires("eigen/3.3.7")
        self.requires("flann/1.9.1")
        self.requires("libpng/1.6.37")
        # self.requires("common/1.0.2")  # package from https://git.ircad.fr/conan/conan-common
        # self.requires("openni/2.2.0")  #
        # self.requires("qt/5.14.1")
        # self.requires("vtk/8.2.0") #

        if tools.os_info.is_windows:
            self.requires("zlib/1.2.11")

    def build(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_segmentation"] = "ON"
        cmake.definitions["BUILD_registration"] = "ON"
        cmake.definitions["BUILD_2d"] = "ON"
        cmake.definitions["BUILD_features"] = "ON"
        cmake.definitions["BUILD_filters"] = "ON"
        cmake.definitions["BUILD_geometry"] = "ON"
        cmake.definitions["BUILD_io"] = "ON"
        cmake.definitions["BUILD_kdtree"] = "ON"
        cmake.definitions["BUILD_octree"] = "ON"
        cmake.definitions["BUILD_search"] = "ON"
        cmake.definitions["BUILD_ml"] = "ON"
        cmake.definitions["PCL_SHARED_LIBS"] = "ON"
        cmake.definitions["BUILD_sample_consensus"] = "ON"
        cmake.definitions["PCL_BUILD_WITH_BOOST_DYNAMIC_LINKING_WIN32"] = self.options["boost"].shared
        cmake.definitions["PCL_BUILD_WITH_FLANN_DYNAMIC_LINKING_WIN32"] = self.options["flann"].shared
        cmake.definitions["BUILD_common"] = "ON"
        cmake.definitions["BUILD_tools"] = "OFF"
        cmake.definitions["BUILD_apps"] = "OFF"
        cmake.definitions["BUILD_examples"] = "OFF"
        cmake.definitions["WITH_LIBPNG"] = "ON"
        cmake.definitions["WITH_PCAP"] = "OFF"
        cmake.definitions["WITH_DAVIDSDK"] = "OFF"
        cmake.definitions["WITH_ENSENSO"] = "OFF"
        cmake.definitions["WITH_OPENNI"] = "OFF"
        cmake.definitions["WITH_OPENNI2"] = "OFF"
        cmake.definitions["WITH_RSSDK"] = "OFF"
        cmake.definitions["WITH_RSSDK2"] = "OFF"
        cmake.definitions["WITH_DSSDK"] = "OFF"
        cmake.definitions["WITH_LIBUSB"] = "OFF"
        cmake.definitions["WITH_OPENGL"] = "OFF"
        cmake.definitions["WITH_QHULL"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_simulation"] = "OFF"

        if self.options.cuda != "None":
            cmake.definitions["BUILD_CUDA"] = "ON"
            cmake.definitions["BUILD_GPU"] = "ON"
            cmake.definitions["BUILD_gpu_kinfu"] = "ON"
            cmake.definitions["BUILD_gpu_kinfu_large_scale"] = "ON"
            cmake.definitions["BUILD_visualization"] = "ON"
            cmake.definitions["BUILD_surface"] = "ON"
            cmake.definitions["CUDA_ARCH_BIN"] = "3.0 3.5 3.7 5.0 5.2 6.0 6.1 7.0 7.5"

        if tools.os_info.is_windows:
            cmake.definitions["CUDA_PROPAGATE_HOST_FLAGS"] = "ON"
        else:
            cmake.definitions["CUDA_PROPAGATE_HOST_FLAGS"] = "OFF"

        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os != "Android":
            version_short = ".".join(self.version.split(".")[:2])
            self.cpp_info.includedirs = ["include/pcl-{}".format(version_short)]
