import os
import sys
import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class PduGeneratorHook(BuildHookInterface):
    """
    Custom build hook for PDU code generation.
    This hook is registered in pyproject.toml and will be automatically discovered by Hatchling.
    """
    PLUGIN_NAME = 'pdu-generator'

    def initialize(self, version, build_data):
        """
        Initialize the build hook.
        This method is called by Hatchling during the build process.
        """
        # Ensure the directory exists
        codegen_dir = os.path.join(self.root, "src", "pdu_codegen")

        # We need to add src to sys.path if we want to import the generator,
        # or just call it as a subprocess. Subprocess is safer for isolation.
        print("--- Running PDU code generation ---")

        # Change working directory to the codegen folder so relative paths in script work
        original_cwd = os.getcwd()
        os.chdir(codegen_dir)
        try:
            # We call the script using the current python executable
            subprocess.check_call([sys.executable, "run_transform.py"])
        finally:
            os.chdir(original_cwd)
        print("--- PDU code generation complete ---")

