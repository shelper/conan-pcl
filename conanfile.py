import os

from fnmatch import fnmatch
from conans import ConanFile, CMake, tools


class LibPCLConan(ConanFile):
    name = "pcl"
    upstream_version = "1.9.1"
    package_revision = "-r6"
    version = "{0}{1}".format(upstream_version, package_revision)

    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "cuda": ["9.2", "10.0", "10.1", "None"]
    }
    default_options = [
        "shared=True",
        "fPIC=True",
        "cuda=None"
    ]
    default_options = tuple(default_options)
    exports = [
        "patches/clang_macos.diff",
        "patches/kinfu.diff",
        "patches/pcl_eigen.diff",
        "patches/pcl_gpu_error.diff",
        "patches/point_cloud.diff"
    ]
    url = "https://git.ircad.fr/conan/conan-pcl"
    license = "BSD License"
    description = "The Point Cloud Library is for 2D/3D image and point cloud processing."
    source_subfolder = "source_subfolder"
    short_paths = True

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        # PCL is not well prepared for c++ standard > 11...
        del self.settings.compiler.cppstd

        if 'CI' not in os.environ:
            os.environ["CONAN_SYSREQUIRES_MODE"] = "verify"

    def requirements(self):
        self.requires("common/1.0.2@sight/stable")
        self.requires("qt/5.14.1@sight/testing")
        self.requires("eigen/3.3.7-r3@sight/stable")
        self.requires("boost/1.69.0-r4@sight/stable")
        self.requires("vtk/8.2.0-r5@sight/testing")
        self.requires("openni/2.2.0-r5@sight/stable")
        self.requires("flann/1.9.1-r5@sight/stable")

        if tools.os_info.is_windows:
            self.requires("zlib/1.2.11-r4@sight/stable")

    def build_requirements(self):
        if tools.os_info.linux_distro == "linuxmint":
            installer = tools.SystemPackageTool()
            installer.install("zlib1g-dev")

    def system_requirements(self):
        if tools.os_info.linux_distro == "linuxmint":
            installer = tools.SystemPackageTool()
            installer.install("zlib1g")

    def source(self):
        tools.get(
            "https://github.com/PointCloudLibrary/pcl/archive/pcl-{0}.tar.gz".format(
                self.upstream_version))
        os.rename(
            "pcl-pcl-{0}".format(self.upstream_version),
            self.source_subfolder)

    def build(self):
        pcl_source_dir = os.path.join(
            self.source_folder, self.source_subfolder)
        tools.patch(pcl_source_dir, "patches/clang_macos.diff")
        tools.patch(pcl_source_dir, "patches/kinfu.diff")
        tools.patch(pcl_source_dir, "patches/pcl_eigen.diff")
        tools.patch(pcl_source_dir, "patches/pcl_gpu_error.diff")
        tools.patch(pcl_source_dir, "patches/point_cloud.diff")

        # patch for cuda arch >7.0

        for path, subdirs, names in os.walk(pcl_source_dir,):
            for name in names:
                if fnmatch(name, "*.cu"):
                    wildcard_file = os.path.join(path, name)

                    # Fix package_folder paths
                    tools.replace_in_file(
                        wildcard_file, "__all(", "__all_sync(0xFFFFFFFF,", strict=False)
                    tools.replace_in_file(
                        wildcard_file, "__any(", "__any_sync(0xFFFFFFFF,", strict=False)
                    tools.replace_in_file(
                        wildcard_file, "__ballot(",
                        "__ballot_sync(0xFFFFFFFF,", strict=False)

        # Use our own FindFLANN which take care of conan..
        os.remove(
            os.path.join(
                pcl_source_dir,
                'cmake',
                'Modules',
                'FindFLANN.cmake'))

        # Import common flags and defines
        import common

        # Generate Cmake wrapper
        common.generate_cmake_wrapper(
            cmakelists_path='CMakeLists.txt',
            source_subfolder=self.source_subfolder,
            build_type=self.settings.build_type,
            setup_cuda=True
        )

        cmake = CMake(self)

        cmake.definitions["BUILD_apps"] = "OFF"
        cmake.definitions["BUILD_examples"] = "OFF"
        cmake.definitions["BUILD_common"] = "ON"
        cmake.definitions["BUILD_2d"] = "ON"
        cmake.definitions["BUILD_features"] = "ON"
        cmake.definitions["BUILD_filters"] = "ON"
        cmake.definitions["BUILD_geometry"] = "ON"
        cmake.definitions["BUILD_io"] = "ON"
        cmake.definitions["BUILD_kdtree"] = "ON"
        cmake.definitions["BUILD_octree"] = "ON"
        cmake.definitions["BUILD_sample_consensus"] = "ON"
        cmake.definitions["BUILD_search"] = "ON"
        cmake.definitions["BUILD_tools"] = "OFF"
        cmake.definitions["PCL_BUILD_WITH_BOOST_DYNAMIC_LINKING_WIN32"] = "ON"
        cmake.definitions["PCL_SHARED_LIBS"] = "ON"
        cmake.definitions["WITH_PCAP"] = "OFF"
        cmake.definitions["WITH_DAVIDSDK"] = "OFF"
        cmake.definitions["WITH_ENSENSO"] = "OFF"
        cmake.definitions["WITH_OPENNI"] = "OFF"
        cmake.definitions["WITH_OPENNI2"] = "OFF"
        cmake.definitions["WITH_RSSDK"] = "OFF"
        cmake.definitions["WITH_QHULL"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_ml"] = "ON"
        cmake.definitions["BUILD_simulation"] = "OFF"
        cmake.definitions["BUILD_segmentation"] = "ON"
        cmake.definitions["BUILD_registration"] = "ON"

        if self.options.cuda != "None":
            cmake.definitions["BUILD_CUDA"] = "ON"
            cmake.definitions["BUILD_GPU"] = "ON"
            cmake.definitions["BUILD_gpu_kinfu"] = "ON"
            cmake.definitions["BUILD_gpu_kinfu_large_scale"] = "ON"
            cmake.definitions["BUILD_visualization"] = "ON"
            cmake.definitions["BUILD_surface"] = "ON"
            cmake.definitions["CUDA_ARCH_BIN"] = ' '.join(
                common.get_cuda_arch())

        if tools.os_info.is_macos:
            cmake.definitions["BUILD_gpu_features"] = "OFF"

        if tools.os_info.is_windows:
            cmake.definitions["CUDA_PROPAGATE_HOST_FLAGS"] = "ON"
        else:
            cmake.definitions["CUDA_PROPAGATE_HOST_FLAGS"] = "OFF"

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        # Import common flags and defines
        import common

        common.fix_conan_path(self, self.package_folder, '*.cmake')

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
