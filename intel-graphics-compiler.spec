
%define llvm_version 7.0.1
%define opencl_clang_version 8.0.1

Summary:	The Intel Graphics Compiler for OpenCL
Name:		intel-graphics-compiler
Version:	1.0.8
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/intel/intel-graphics-compiler/archive/igc-%{version}/igc-%{version}.tar.gz
# Source0-md5:	9999fd7b6947b2ed0a11f7b07b1e7acc
Patch0:		pkgconfig.patch
URL:		https://github.com/intel/intel-graphics-compiler/
BuildRequires:	llvm-devel >= %{llvm_version}
BuildRequires:	opencl-clang-devel >= %{opencl_clang_version}
BuildRequires:	cmake >= 3.2.0
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Intel Graphics Compiler for OpenCL is an LLVM based compiler for OpenCL
targeting Intel Gen graphics hardware architecture.

%package libs
Summary:	The Intel Graphics Compiler for OpenCL libraries
Group:		Libraries

%description libs
The Intel Graphics Compiler for OpenCL libraries.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -qn %{name}-igc-%{version}

%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DCCLANG_FROM_SYSTEM=ON \
	../
%{__make}

cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/GenX_IR
%attr(755,root,root) %{_bindir}/iga64

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libiga64.so.1.*.*
%ghost %attr(755,root,root) %{_libdir}/libiga64.so.1
%attr(755,root,root) %{_libdir}/libigc.so.1.*.*
%ghost %attr(755,root,root) %{_libdir}/libigc.so.1
%attr(755,root,root) %{_libdir}/libigdfcl.so.1.*.*
%ghost %attr(755,root,root) %{_libdir}/libigdfcl.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/igc
%attr(755,root,root) %{_libdir}/libiga64.so
%attr(755,root,root) %{_libdir}/libigc.so
%attr(755,root,root) %{_libdir}/libigdfcl.so
%{_pkgconfigdir}/igc-opencl.pc