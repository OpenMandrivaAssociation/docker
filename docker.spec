# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global dist_version 17.12.1
%global moby_version %{dist_version}-ce-rc1

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%global debug_package %{nil}
%global provider github
%global provider_tld com
%global project docker
%global repo %{project}
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}

#debuginfo not supported with Go
%global gopath  %{_libdir}/golang
%define gosrc %{gopath}/src/pkg/%{import_path}

%global commit      89658bed64c2a8fe05a978e5b87dbec409d57a0f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		docker
Version:	%{dist_version}
Release:	1
Summary:	Automates deployment of containerized applications
License:	ASL 2.0
Epoch:		1
Group:		System/Configuration/Other
URL:		http://www.docker.com
Source0:	https://%{import_path}/archive/v%{moby_version}.tar.gz
Source1:	%{repo}.service
Source2:	%{repo}.sysconfig
Source3:	%{repo}-storage.sysconfig
Source6:	%{repo}-network.sysconfig
Source7:	%{repo}.socket
Source8:	%{repo}-network-cleanup.sh
Source10:	https://%{provider}.%{provider_tld}/%{project}/libnetwork/archive/master.tar.gz
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	libltdl-devel
# ensure build uses golang 1.4 or above
BuildRequires:	golang >= 1.7
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	go-md2man
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	btrfs-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(libseccomp)
Requires(pre):	rpm-helper
Requires(post,preun,postun):	systemd
# With docker >= 1.11 you now need containerd (and runC as a dep)
Requires:	containerd >= 0.2.3
Requires:	runc
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:	xz
Requires:	bridge-utils
# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:	libcgroup
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
Requires:	%{repo} = %{version}-%{release}
Provides:	%{repo}-io-fish-completion = %{version}-%{release}

%description fish-completion
This package installs %{summary}.

%package unit-test
Summary:	%{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests.

%package vim
Summary:	vim syntax highlighting files for Docker
Requires:	%{repo} = %{version}-%{release}
Requires:	vim
Provides:	%{repo}-io-vim = %{version}-%{release}

%description vim
This package installs %{summary}.

%package zsh-completion
Summary:	zsh completion files for Docker
Requires:	%{repo} = %{version}-%{release}
Requires:	zsh
Provides:	%{repo}-io-zsh-completion = %{version}-%{release}

%description zsh-completion
This package installs %{summary}.

%prep
%setup -q -n %{name}-ce-%{moby_version}
%apply_patches

%build
export DOCKER_GITCOMMIT="%{shortcommit}"
mkdir -p src/github.com/docker
export GOPATH=%{gopath}:$(pwd)
# MAGIC HERE
ln -s ../../../components/cli src/github.com/docker
ln -s ../../../components/engine src/github.com/docker/docker
pushd components/cli
	DISABLE_WARN_OUTSIDE_CONTAINER=1 make VERSION=%{moby_version} dynbinary
popd
pushd components/engine
	DOCKER_BUILDTAGS='seccomp journald' VERSION=%{moby_version} hack/make.sh dynbinary
popd

%install
# install binaries
install -d %{buildroot}%{_bindir}
install -p -m 755 components/cli/build/docker-linux-amd64 %{buildroot}%{_bindir}/docker
install -d %{buildroot}%{_sbindir}
install -p -m 755 components/engine/bundles/dynbinary-daemon/dockerd-%{moby_version} %{buildroot}%{_sbindir}/dockerd

# Place to store images
install -d %{buildroot}%{_var}/lib/docker

# install bash completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 components/cli/contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 components/cli/contrib/completion/fish/%{repo}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 components/engine/contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 components/engine/contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 components/cli/contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 644 components/engine/contrib/udev/80-docker.rules %{buildroot}%{_udevrulesdir}
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

%check
# This is completely unstable so I desactivate it for now.
#[ ! -w /run/%{repo}.sock ] || {
    #mkdir test_dir
    #pushd test_dir
    #git clone https://github.com/lsm5/docker.git -b fedora-1.10
    #pushd %{repo}
    #make test
    #popd
    #popd
#}

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
exit 0

%post
%systemd_post docker

%preun
%systemd_preun docker

%postun
%systemd_postun_with_restart docker

%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-network
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-storage
%{_bindir}/docker
%{_sbindir}/docker-network-cleanup
%{_sbindir}/dockerd
%{_presetdir}/86-docker.preset
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%dir %{_var}/lib/docker
%dir %{_udevrulesdir}
%{_udevrulesdir}/80-docker.rules

%files fish-completion
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{repo}.fish

%files vim
%{_datadir}/vim/vimfiles/ftdetect/%{repo}file.vim
%{_datadir}/vim/vimfiles/syntax/%{repo}file.vim

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{repo}
