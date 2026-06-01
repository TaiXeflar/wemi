




import os
import subprocess
from pathlib import Path

from .refs import FindSDK
from utils import regedit, message

class FindMSMPI(FindSDK):

    _name_desc = 'Microsoft MPI'

    def __init__(self):
        super().__init__()

        self.es: Path

    def __WINDOWS__(self):

        if os.getenv("PROCESSOR_ARCHITECTURE") not in ("AMD64", "i686"):
            message("WARNING", "Found ARM/ARM64/ARM64EC devices. Disable MSMPI support.")
            return
        
        msmpi_regedit_root = (
            Path(raw_path) 
            if (raw_path := regedit("HKLM", r"SOFTWARE\Microsoft\MPI", key_name="InstallRoot")) 
            else None   
        )

        if not msmpi_regedit_root:
            message("WARNING", "Warning: Failed to compile MSMPI modulefile object due to no results.")
            return

        try:
            mpiexec_dir_list = [
                Path(mpiexec).resolve()
                for mpiexec in subprocess.run([self.es, r"mpiexec.exe"], 
                                              capture_output=True,
                                              check=True,
                                              text=True).stdout.splitlines()
            ]

            msmpi_mpiexec = [d for d in mpiexec_dir_list if d == (msmpi_regedit_root/"Bin/mpiexec.exe")]

        except Exception as e:
            # message("WARNING", "Warning: Failed to compile MSMPI modulefile object due to no results.")
            return

        if not msmpi_mpiexec:
            # message("WARNING", "Warning: Failed to compile MSMPI modulefile object due to no results.")
            return
        
        self.add_rule(Module="microsoft/msmpi/mpiexec",
                      mode="tcl",
                      Include_file="template_msmpi_mpiexec",
                      conflicts=["intel/oneapi/mpi", "microsoft/msmpi"],
                      root=msmpi_regedit_root.resolve().as_posix(),
                      ENVs={
                        "MSMPI_BIN": (msmpi_regedit_root/"Bin").resolve().as_posix()
                      },
                      PATH=["$env(MSMPI_BIN)"])


