from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(build_policy="missing")
    builder.visual_runtimes = ["MD", "MDd"]
    builder.add_common_builds(shared_option_name="SimpleAmqpClient:shared", pure_c=False)

    # The library cannot be built as a static library on Win32.
    if platform.system() == "Windows":
        shared_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if options.get("SimpleAmqpClient:shared"):
                shared_builds.append([settings, options, env_vars, build_requires])

        builder.builds = shared_builds

    builder.run()

