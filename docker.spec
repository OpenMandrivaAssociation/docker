%global project docker
%global repo %{project}
%global import_path github.com/%{project}/%{repo}

#debuginfo not fully supported with Go
%undefine _debugsource_packages

%global optflags %{optflags} -Wno-error
%global build_ldflags %{build_ldflags} --rtlib=libgcc --unwindlib=libgcc

#define beta rc.3

Summary:	Automates deployment of containerized applications
Name:		docker
Version:	29.1.5
Release:	%{?beta:0.%{beta}.}1
License:	ASL 2.0
Group:		System/Configuration/Other
URL:		https://www.docker.com
%if 0%{?beta:1}
Source0:	https://github.com/moby/moby/archive/refs/tags/v%{version}%{?beta:-%{beta}}.tar.gz
%else
Source0:	https://github.com/moby/moby/archive/refs/tags/docker-v%{version}.tar.gz
%endif
Source1:	%{repo}.service
Source2:	%{repo}.sysconfig
Source3:	%{repo}-storage.sysconfig
Source4:	docker.sysusers
Source5:	daemon.json
Source6:	%{repo}-network.sysconfig
Source7:	%{repo}.socket
Source8:	%{repo}-network-cleanup.sh
Source9:	overlay.conf
# (tpg) taken from https://gist.github.com/goll/bdd6b43c2023f82d15729e9b0067de60
# Not currently used, kept here for reference
Source14:	nftables-docker.nft
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
BuildRequires:	pkgconfig(libnftables)
BuildRequires:	cmake
Requires(pre):	systemd
%systemd_requires
# For Docker remapping (subuid and subgid)
Requires:   setup >= 2.9.5
# For "docker run --init"
Requires:	tini-static
# With docker >= 1.11 you now need containerd (and runC or crun as a dep)
Requires:	containerd >= 0.2.3
Requires:	crun
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:	xz
# Needed to share network with containers
Requires:	bridge-utils
Requires:	iptables
# It may make sense to make this a Recommends: in the future
# For now, let's keep it a hard requirement because it used to
# be directly in this package
Requires:	docker-cli
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

%prep
%autosetup -p1 -n moby-docker-v%{version}%{?beta:-%{beta}}
find . -name "*~" |xargs rm || :

%build
export DOCKER_GITCOMMIT="OpenMandriva-%{version}-%{release}"
export DOCKER_CLI_EXPERIMENTAL=enabled

# dockerd
DOCKER_BUILDTAGS='seccomp journald' VERSION=%{version} hack/make.sh dynbinary

%install
# install binaries
install -d %{buildroot}%{_sbindir}
install -p -m 755 bundles/dynbinary-daemon/dockerd %{buildroot}%{_sbindir}/dockerd
install -p -m 755 bundles/dynbinary-daemon/docker-proxy %{buildroot}%{_bindir}/docker-proxy
ln -s tini-static %{buildroot}%{_bindir}/docker-init

# Place to store images
install -d %{buildroot}%{_var}/lib/docker

install -d %{buildroot}%{_sysconfdir}/docker
# (tpg) we are using nftables
# (bero) but the approach of this ruleset breaks adding interfaces/ports
# dynamically, so for now we're letting docker use iptables-legacy
#install -D -p -m 755 %{SOURCE14} %{buildroot}%{_sysconfdir}/nftables/%{name}.nft

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
cat >%{buildroot}%{_udevrulesdir}/80-docker.rules <<'EOF'
# hide docker's loopback devices from udisks, and thus from user desktops
SUBSYSTEM=="block", ENV{DM_NAME}=="docker-*", ENV{UDISKS_PRESENTATION_HIDE}="1", ENV{UDISKS_IGNORE}="1"
SUBSYSTEM=="block", DEVPATH=="/devices/virtual/block/loop*", ATTR{loop/backing_file}=="/var/lib/docker/*", ENV{UDISKS_PRESENTATION_HIDE}="1", ENV{UDISKS_IGNORE}="1"
EOF
# install storage dir
install -d -m 700 %{buildroot}%{_var}/lib/docker
# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{SOURCE7} %{buildroot}%{_unitdir}

# for additional args
install -d %{buildroot}%{_sysconfdir}/docker/
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/docker/daemon.json

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
%config(noreplace) %{_sysconfdir}/docker/daemon.json
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-network
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-storage
%{_sysusersdir}/%{name}.conf
%dir %{_sysconfdir}/docker
%{_bindir}/docker-proxy
%{_bindir}/docker-init
%{_sbindir}/docker-network-cleanup
%{_sbindir}/dockerd
%{_presetdir}/86-docker.preset
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%dir %{_var}/lib/docker
%dir %{_udevrulesdir}
%{_udevrulesdir}/80-docker.rules
%{_sysconfdir}/modules-load.d/overlay.conf
