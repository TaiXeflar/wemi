

# Documentation Noun Naming Meanings


## General

 - target: Usually means specified solution to develop with. On CPU Architectures, target means which CPU are develop for, like `x86`(`i686`), `x64`(`x86-64`/`AMD64`/`Intel 64`), `ARM`, `ARM64`(`aarch64`) etc.
 - Compiler: A executable can analyze, preprocessing, and compile language script to object file. Typically we can say compilers with its language frontend to identify what is the language compiler. 
   - C/C++ language frontend can be MSVC `cl.exe`, LLVM `clang`/`clang++`/`clang-cl`, GCC `gcc`/`g++`.
   - Fortran language frontend can be Intel Fortran `ifx`, GFortran `gfortran`, LLVM `flang`.
   - Swift language frontend is Apple-LLVM/Clang based swift compiler.
   - Codon, LLVM-Based Python compiler, developed by Exaloop Inc.
   - Visual Basic, C#, F#: .NET Framework based Roslyn compilers.

 - Interpreter: A executable running with Read-Eval-Print Loop(REPL) mode run code/language script directly. 
   - C-based Python Interpreter CPython `python.exe`.
   - RPython based Python Interpreter `pypy.exe`.
   - .NET Framework/ Roslyn C#, F# language REPL `csi.exe`, `fsi.exe`.

 - Shell: A kind of command-line interface(CLI) interactive environment run programs, system control tasks etc. Shell is also a REPL which is a kind of Interpreters.
   - Unix-Like environment: SH, BASH, CSH/TCSH, DASH, KSH, ZSH etc.
   - Windows: Classic Windows DOS batch/CMD command `cmd.exe`.
   - Windows modern .NET based cross-platform `PowerShell`.

 - Libraries/SDKs: Project's program with its referenced executables/shared libs/include headers/static libs/docs etc.
   - executable: Typically a program has been compiled to a callable executable as program's entry point.
   - header: Static include header files have imported references.
   - Static Library: Pre-Compiled libraries will be ready for linking to program.
   - Shared Library: Pre-Compiled libraries will be ready for calling dynamically when program is calling extended functionality.
   - Object File: Compiled program with a Intermediate state, used for next step linking.
   - 
   |System|Windows MSVC| Unix-Like / MinGW-based |
   |:---- |:-----:|:-------:|
   |executable| `*.exe` | ---- |
   | header | `*.h`/`*.hpp` | `*.h`/`*.hpp` |
   | Static Library | `*.lib` | `*.a` |
   | Shared Library | `*.dll` | `*.so`/`*.so.x` |
   | Export Definition File | `*.exp` | ---- |
   | Program Debug Database | `*.pdb` | ---- |
   | Incremental Link Database file | `*.ilk` | ---- |
   | Object File | `*.obj` | `*.o` |
   | Makefile | `*.mak` | `Makefile` |

 - Build Programs: Program's maintaince and build structure. CMake identify these programs as CMake generators.
   - CMake: A high level project maintainence with Compile rule support. CMake also can be the compile program to select compilers, generators, compile rule, build test etc building tests.
   - NMAKE: Microsoft Make Utility. By using `*.mak`/`*.vc` with NMAKE format file inside to define/manage the project compile rules. Some earlier utils (the age that have no CMake, MSBuild and ninja) will use NMAKE to maintain build porting on Windows. NMAKE program `NMAKE.exe` is combined with Visual C++ compilers. 

     To select this generator in cmake by `cmake ... -G "NMAKE Utility"`.

   - MSBuild: Microsoft .NET based build project generates `*.vcproj`/`*.vcxproj`/`*.sln` support for open Visual Studio Solution with IDE interface. These build files are also support to CLI build commands directly. To select this generator in cmake by `cmake ... -G "Visual Studio XX"`. 

   - Ninja-build: A Cross-Platform supported generator focus on speed. It will automatically generates `build.ninja`, `rules.ninja` etc. `*.ninja` files and CMake configured files to 
   set the compilation process.

   - GNU Make: GNU Make utility. By defines `Makefile` to set the compilation rules and build process with a GNU-POSIX standard shell compatiable script with build rules.
  

### Compiler Infastructure

A complete set of compiler choices, includes preprocessor, compiler, assembler, linker, archiver etc.

- MSVC: Microsoft Visual C++. CMake identification is `MSVC`.
    
  Microsoft Optimized C/C++ compiler for Windows Desktop development. 

- Roslyn: .NET based for Visual Basic/C# compiler.

- GCC: GNU Compiler collection. CMake identification is `GNU`. 

  GCC is a massive compiler sets with C/C++/Obj-C/D/Go/Fortran/Java/Ada/COBOL/etc. language frontend, follows POSIX standard and GNU standard. Please be aware like archiver, linker, assembler, dump, disassembler etc. are belongs to GNU Binutils, not in GCC. Also, GNU Make Utility, Autotools (Autoconf, Automake) are also not in GCC.
  For GCC running on Windows are build by MinGW GCC compilers.


- LLVM: LLVM(Low Level Virtual Machine) Compiler Infastructure. CMake identification is `Clang` and `Flang`.

  LLVM is for high performance, optimized toolsets for optimizing on different target microcontrollers, self designed language (like CUDA, HIP, swift, zig, Rust, codon, cangjie), LLVM backend optimized language frontend (like LLVM/Clang, LLVM/Flang, LDC, ...) high performance programs etc.

  LLVM is a required project for various platforms SDKs. Different platforms and IDE may contain its pre-compiled optimized LLVMN toolset for developers.

- CUDA: Compute Unified Device Architecture. Any GPGPU device is designed by NVIDIA with hardware specified for CUDA architecture/toolsets can be a operationable CUDA "Device". Any extended libraries based on CUDA for CUDA GPGPU compute are CUDA-X libraries, like `cuBLAS`, `cuDNN`, `cuFFT`, `cuTensor` etc. For CUDA language is using NVIDIA CUDA compiler program `nvcc`. 

- NVHPC: NVIDIA re-brand new HPC SDK from legacy PGI compilers. CMake identification is `NVHPC`. NVIDIA stopped Windows x64 support since 2020. Before version 2020.4 is PGI compilers last release, 2020.7 is re-branded NVIDIA HPC SDK 1st release, with long term "Windows x64 will be released at a later date" status and no any release.

- ROCm: AMD Radeon On Compute platform(ROCm). AMD's open sourced develop SDK platform, targeting for AMD products. ROCm libraries have with several projects:
   - AMD-LLVM. AMD optimiized LLVM, targeting for x86 and speThe CMake identification on AMD-LLVM compiler is Clang.
   - HIP: C++ Heterogeneous-Compute Interface for Portability. HIP can converts CUDA to standard C++ code and target to NVIDIA/AMD GPGPU Device. HIP is a part of ROCm. 
   - rocX/hip-X Libraries: Similiar GPU acceleration library implementation to NVIDIA CUDA-X libraries.
   - AOTriton: Ahead of Time Trion Math Library.

- TheRock: The HIP Environment and ROCm Kit, with capital chars' abbbrevation to TheRock.

  TheRock is a open sourced cmake super project to porting ROCm/HIP libraries from Linux/Windows only, to dual-platform 
  portable cross platform build capable solution. 
  
  You may need a High Level Gaming PC or HEDT/Server grade Windows/Linux operating systems
  to build native ROCm software stack, and ROCm specified PyTorch/JAX DL libraries.



- oneAPI: Intel Developer toolkit oneAPI. 

  Including Intel classic C/C++ `icl.exe`/`icc.exe`(deprecated), Intel Visual Fortran `ifort.exe` (deprecated), Intel DPC++/C++ `dpcpp.exe`(deprecated).

  Intel modern compilers are moving to its LLVM backend for high performance compilers, with `icx.exe`/`icx-cl.exe`, `ifx.exe`, `icpx.exe`. CMake identification is `IntelLLVM`.




## Environment Variable
System and standalone programs will use Environment Variable control its behavior.

On Unix-Like systems, users can export variables in Shell command line with `export VAR=val`/`set VAR=val`.

On Windows systems, users can use `sysdm.cpl` GUI and enter Environment Variables page to add variables. Using PowerShell can use `$env:VAR=val` to define it.

 - `PATH`: Controls and make it as executables' PATH conclusion. This system class variable will find all paths in this variable, and find all executables in these directory.
 - `INCLUDE`: Controls and make it as headers' PATH conclusion. macOS/Linux users can mention that Environment variable `CPATH` is also a INCLUDE PATH to `INCLUDE`. This env variable is not effect on Windows.
 - `LIB`: Controls and make it as static libraries' PATH conclusion.
 - `LD_LIBRARY_PATH`: Controls and make it as dynamic libraries(DLLs) / shared objects' PATH conclusion. On windows platform, DLLs should at the same directory with executables or in PATH together. On Unix-Like platforms sometimes need to specify this variable.
 - `RPATH`:
 - `MANPATH`: Unix-Like specified variable to set on Manual page's PATH like variable. This variable is not support for documentation/searching for Windows (Unless using in MinGW bash).


## Python
 - PSF: Python Software Foundation (PSF). The official Developer of Python Programing Laungage and CPython.
 - CPython: C language based Python Interpreter, developed and official released by PSF. Third-party repacked by Anaconda and conda-forge. PSF CPython license is under PSF License version 2.

   CPython is implemented with Python 2 and Python 3.

 - PyPy: Restricted Python(RPython) based Python Interpreter. PyPy license is multi-licensing with main MIT license.
 - Codon: LLVM based IR optimized Python Compiler. Developed by Exaloop, released with Apache 2.0 license.


## Microsoft
 - MSVC: Microsoft Visual C++. The compiler product is "Microsoft Optimized C/C++ compiler", with its basic compiler driver program `cl.exe`. 
 - NMAKE: MSVC toolchain packed Make utility from Microsoft.
 - MSBuild: A .NET based new type build program that generates Visual Studio solution. 

 - VS20XX -> Visual Studio 20XX.

    Visual Studio is a IDE includes toolset with Visual C++ (MSVC), .NET language(Visual Basic, C#, F#, Roslyn Compiler), .NET Frameworks(.NET Framework, Blazor etc.), Unity/Unreal Engine development. Visual Studio also provides a Clang and CMake+Ninja-build support. Current x64 releases is VS2015, VS2017, VS2019, VS2022 and VS2026.

 - VSCode: Visual Studio Code.
  
    VSCode is a light-weight code editor.

## CMake Build Systems
 - CMake is Cross-Platform Make, have independent Language to manage Project source code, generate and convert makefile rules to target project generators.
 - CMake also allows projects provide their redistributable cmake config files to other projects to resolve cmake dependicy.
 - CMake is developed by Kitware, open-sourced, under BSD-3 clause license, hosted on GitLab.

## AMD
 - AMD: Advanced Micro Devices Inc. (AMD).
 - ROCm: Radeon On Compute platform.
 - rocBLAS/hipBLAS/hipBLASLt
 - HIP SDK: C++ Heterogeneous-Compute Interface for Portability (HIP). AMD HIP SDK is part of AMD ROCm, a C++ Runtime API and Kernel Language that allows developers to create portable applications for AMD and NVIDIA GPUs from single source code. HIP compiler is AMD-LLVM based `hipcc.exe`.
 - TheRock: The HIP Environment and ROCm Kit. A under active development, early accessed, experimential super CMake project builds ROCm toolkit targeting on AMD64 and AMDGPU arch based Linux/Windows platforms. 

## NVIDIA
 - NVIDIA: NVIDIA Coporation.
 - NVIDIA CUDA: Compute Unified Device Architecture. CUDA compiler is `nvcc.exe`.
 - NVIDIA cuDNN: CUDA-X Libraries targing to Deep Neural Networks.
 - NVIDIA cuDSS: CUDA-X Libraries targing to Direct Sparse Solver.
 - NVIDIA cuTENSOR: CUDA-X Libraries targing to tensor linear algebra.
 - NVIDIA cuSPARSERLt: CUDA-X Libraries targing to general matrix-matrix operations.
 - NVIDIA cutlass: CUDA-X Libraries

## Intel 
 - Intel: Intel Coporation.
 - Intel oneAPI: A Standalone Installer with Intel toolsets can integrates to Visual Studio 20XX, Includes Intel High Performance Compilers/Libraries.
 - Intel C++: Intel oneAPI legacy "Intel C/C++ compiler classic" `icl.exe`. LLVM Based Intel C/C++ compiler is `icx.exe` and `icx-cl.exe`.
 - Intel Visual Fortran: Intel oneAPI legacy "Intel Visual Fortran compiler classic" `ifort.exe`. LLVM Based Intel Fortran compiler is `ifx.exe`.
 - Intel DPC++/C++: Intel Data Parallel C++ `dpcpp.exe`. Now `dpcpp` is deprecated with `icpx.exe` instead.
 - Intel LLVM: Start from oneAPI 2023 and 2025, Intel deprecated Intel Classic C++ `icl.exe` and Fortran Classic `ifort.exe` and moving its compiler backend to LLVM, with frontend moving to `icx.exe` and `ifx.exe`.

## GCC
 - GCC: GNU Compiler collection. A toolsets of various compiler infastructure like LLVM, includes GNU C/C++ compiler `gcc`/`g++`, GNU Fortran Compiler `gfortran`, GNU D compiler `gdc`, GNU Golang Compiler, GNU Ada compiler `gnat`, GNU COBOL compiler etc. GCC have various platform target types with targeting macOS x86/x64/ARM64, Linux x86/x64/ARM/ARM64/RISC-V, Windows x86/x64 (MinGW) etc.

 - On Windows platform, GCC compiler are built from Linux cross platform build, target it to redistributable MinGW-w64 GCC compilers. GCC also can be build by POSIX compatable environments like Cygwin/MSYS2 but needs to shipping with `cygwin-X.dll`/`msys2-X.dll`.

 Windows standalone GCC compilers can be found in Dev-C++, Code::Blocks, Strawberry Perl installation, or can be download via nixman

## LLVM
 - LLVM: LLVM compiler infastructure, with its name is an abbreviation from Low Level Virtual Machine, and a LLVM Dragon logo, founded by Apple Inc, develop and maintained by LLVM-project. LLVM is a project let programs can run codes by optimizing program's bitcode and compile to program.

 - LLVM licensing is under Apache 2.0 License with LLVM runtime exceptions. LLVM supports various operating systems like Windows, macOS, Linux, BSD, AIX, etc. Please be aware some LLVM sub-projects not support on specific platforms (like libunwind not support on Windows due to Microsoft SEH exception handeling instead). LLVM also is a fast-moving target, which each major release could have break changes.

 - LLVM supports modualized/customized Frontend(Language), Intermediate Representation(IR) optimizing and backend(target microcontroller architecture). Most customized language will use LLVM to develop its Frontend like C/C++, Fortran, Swift, Rust, Zig, Go, Cangjie, CUDA, HIP, DPC++ etc. Targeting backends depends on customized target(chips) like x86/x64, ARM/ARM64, PowerPC/PowerPC64, RISC-V, CUDA GPGPU,AMDGPU(GCN/RDNA-X/CDNA-X), IntelGPU (Arc GPU) etc.

 - LLVM's core function is its LLVM IR toolchain, combine its language frontend with self/other toolchains backend 
 like LLVM/Clang + MSVC/GCC linkers or LLVM linker LLD.

 - Clang: LLVM's official C/C++ language frontend. On Unix/Linux systems is `clang`/`clang++`,  On Windows is `clang-cl`.

 - LLD: LLVM's official Linker sub-project. A complete LLVM C/C++ compiler toolchain can be build by enabling LLVM sub-projects with clang and lld.

 - LLDB: LLVM Debugger.

 - Flang: LLVM based Fortran language compiler frontend.

 - MLIR: Multi Language Intermediate Representation. This is the requirement to build Flang and LLVM based customize language. Also Triton (OpenAI/triton) is based on MLIR.

 - LLVM Target: LLVM target is specifying the target chip what we want. 


