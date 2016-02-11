from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
#use_plugin("python.coverage")
use_plugin("python.distutils")

name = "status-cake-to-graphite"
default_task = "publish"


@init
def set_properties(project):
    project.build_depends_on("boto3")
    project.build_depends_on("requests")
    project.build_depends_on("succubus")
    project.build_depends_on("yamlreader")
