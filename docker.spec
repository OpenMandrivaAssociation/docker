# modifying the dockerinit binary breaks the SHA1 sum check by docker

%global tini_version 0.19.0
%global buildx_version 0.25.0

%global project docker
%global repo %{project}
%global import_path github.com/%{project}/%{repo}

#debuginfo not supported with Go
%undefine _debugsource_packages
%global gopath  %{_libdir}/golang
%define gosrc %{gopath}/src/pkg/%{import_path}

%global optflags %{optflags} -Wno-error
%global build_ldflags %{build_ldflags} --rtlib=libgcc --unwindlib=libgcc

#define beta rc.3

Summary:	Automates deployment of containerized applications
Name:		docker
Version:	28.5.2
Release:	%{?beta:0.%{beta}.}1
License:	ASL 2.0
Group:		System/Configuration/Other
URL:		https://www.docker.com
%if 0%{?beta:1}
Source0:	https://github.com/moby/moby/archive/refs/tags/v%{version}%{?beta:-%{beta}}.tar.gz
%else
Source0:	https://github.com/moby/moby/archive/v%{version}/moby-%{version}.tar.gz
%endif
Source1:	%{repo}.service
Source2:	%{repo}.sysconfig
Source3:	%{repo}-storage.sysconfig
Source4:	docker.sysusers
Source6:	%{repo}-network.sysconfig
Source7:	%{repo}.socket
Source8:	%{repo}-network-cleanup.sh
Source9:	overlay.conf
# tini
Source11:	https://github.com/krallin/tini/archive/v%{tini_version}/tini-%{tini_version}.tar.gz
# cli
Source12:	https://github.com/docker/cli/archive/v%{version}%{?beta:-%{beta}}/cli-%{version}%{?beta?:-%{beta}}.tar.gz
# buildx
Source13:	https://github.com/docker/buildx/archive/v%{buildx_version}/buildx-%{buildx_version}.tar.gz
# (tpg) taken from https://gist.github.com/goll/bdd6b43c2023f82d15729e9b0067de60
# Not currently used, kept here for reference
Source14:	nftables-docker.nft
Patch0:		tini-clang15.patch
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	glibc-static-devel
BuildRequires:	libltdl-devel
BuildRequires:	golang >= 1.24.3
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	go-md2man
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	btrfs-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	cmake
Requires(pre):	systemd
%systemd_requires
# With docker >= 1.11 you now need containerd (and runC or crun as a dep)
Requires:	containerd >= 0.2.3
Requires:	crun
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:	xz
# Needed to share network with containers
Requires:	bridge-utils
Requires:	iptables
# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Provides:	lxc-docker = %{version}
Provides:	docker-swarm = %{version}-%{release}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package fish-completion
Summary:	fish completion files for Docker
Requires:	%{repo} = %{EVRD}
Provides:	%{repo}-io-fish-completion = %{EVRD}

%description fish-completion
This package installs %{summary}.

%package unit-test
Summary:	%{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests.

%package vim
Summary:	vim syntax highlighting files for Docker
Requires:	%{repo} = %{EVRD}
Requires:	vim
Provides:	%{repo}-io-vim = %{EVRD}

%description vim
This package installs %{summary}.

%package zsh-completion
Summary:	zsh completion files for Docker
Requires:	%{repo} = %{EVRD}
Requires:	zsh
Provides:	%{repo}-io-zsh-completion = %{EVRD}

%description zsh-completion
This package installs %{summary}.

%prep
%setup -q -n moby-%{version}%{?beta:-%{beta}}
tar xf %{SOURCE11}
mv tini-%{tini_version} tini
tar xf %{SOURCE12}
tar xf %{SOURCE13}
mv buildx-%{buildx_version} buildx
find . -name "*~" |xargs rm || :
# Needs to be done after unpacking extra bits, given we may want
# to patch tini -- so no %%autosetup
%autopatch -p1

%build
mkdir -p GO/src/github.com/{docker,krallin}
ln -s $(pwd)/cli-%{version}%{?beta:-%{beta}} GO/src/github.com/docker/cli
ln -s $(pwd)/libnetwork-master GO/src/github.com/docker/libnetwork
ln -s $(pwd)/tini GO/src/github.com/krallin/tini
ln -s $(pwd) GO/src/github.com/docker/docker
export DOCKER_GITCOMMIT="OpenMandriva-%{version}-%{release}"
export DOCKER_CLI_EXPERIMENTAL=enabled
export TMP_GOPATH="$(pwd)/GO"
export GOPATH=%{gopath}:"$(pwd)/GO"
export GO111MODULE=off

# docker-init
cd tini
    %cmake
    %make_build tini-static
cd ../..

# dockerd
DOCKER_BUILDTAGS='seccomp journald' VERSION=%{version} hack/make.sh dynbinary

# cli
cd cli-%{version}%{?beta:-%{beta}}
    DISABLE_WARN_OUTSIDE_CONTAINER=1 make VERSION=%{version} LDFLAGS="-linkmode=external" dynbinary
cd ..

# buildx
cd buildx
   VERSION=%{buildx_version} REVISION=%{release} GO111MODULE=on hack/build
cd ..

%install
# install binaries
install -d %{buildroot}%{_bindir}
install -p -m 755 cli-%{version}%{?beta:-%{beta}}/build/docker-linux-* %{buildroot}%{_bindir}/docker
install -d %{buildroot}%{_sbindir}
install -p -m 755 bundles/dynbinary-daemon/dockerd %{buildroot}%{_sbindir}/dockerd
install -p -m 755 bundles/dynbinary-daemon/docker-proxy %{buildroot}%{_bindir}/docker-proxy
install -p -m 755 tini/build/tini-static %{buildroot}%{_bindir}/docker-init

install -d -m 0755 %{buildroot}/%{_libexecdir}/docker/cli-plugins
install -p -m 0755 buildx/bin/build/docker-buildx %{buildroot}/%{_libexecdir}/docker/cli-plugins/

# Place to store images
install -d %{buildroot}%{_var}/lib/docker

install -d %{buildroot}%{_sysconfdir}/docker
# (tpg) we are using nftables
# (bero) but the approach of this ruleset breaks adding interfaces/ports
# dynamically, so for now we're letting docker use iptables-legacy
#install -D -p -m 755 %{SOURCE14} %{buildroot}%{_sysconfdir}/nftables/%{name}.nft

# install bash completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 cli-%{version}%{?beta:-%{beta}}/contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 cli-%{version}%{?beta:-%{beta}}/contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 cli-%{version}%{?beta:-%{beta}}/contrib/completion/fish/%{repo}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 644 contrib/udev/80-docker.rules %{buildroot}%{_udevrulesdir}
# install storage dir
install -d -m 700 %{buildroot}%{_var}/lib/docker
# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{SOURCE7} %{buildroot}%{_unitdir}

# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}-network
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}-storage

#network cleanup
install -d %{buildroot}%{_sbindir}
install -p -m 755 %{SOURCE8} %{buildroot}%{_sbindir}/docker-network-cleanup

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-docker.preset << EOF
enable docker.socket
EOF

install -d %{buildroot}%{_sysconfdir}/modules-load.d/
install -p -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/modules-load.d/overlay.conf

install -Dpm 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf

#%%check
# This is completely unstable so I deactivate it for now.
#[ ! -w /run/%{repo}.sock ] || {
    #mkdir test_dir
    #pushd test_dir
    #git clone https://github.com/lsm5/docker.git -b fedora-1.10
    #pushd %{repo}
    #make test
    #popd
    #popd
#}

%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-network
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-storage
%{_sysusersdir}/%{name}.conf
%dir %{_sysconfdir}/docker
%config(noreplace) %ghost %{_sysconfdir}/docker/daemon.json
%{_bindir}/docker
%{_bindir}/docker-proxy
%{_bindir}/docker-init
%{_sbindir}/docker-network-cleanup
%{_sbindir}/dockerd
%{_libexecdir}/docker/cli-plugins/docker-buildx
%{_presetdir}/86-docker.preset
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%dir %{_var}/lib/docker
%dir %{_udevrulesdir}
%{_udevrulesdir}/80-docker.rules
%{_sysconfdir}/modules-load.d/overlay.conf

%files fish-completion
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{repo}.fish

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{repo}
