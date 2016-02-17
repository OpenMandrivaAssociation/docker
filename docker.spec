%define _libexecdir /usr/libexec
%define debugcflags %nil

# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_usrlibrpm}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global import_path github.com/docker/docker
%global go_dir  %{_libdir}/go
%define gosrc %{go_dir}/src/%{import_path}
%define provider github
%define provider_tld com
%define project %{name}
%define	shortcommit 9e83765

Name:           docker
Version:        1.10.1
Release:        2
Summary:        Automates deployment of containerized applications
License:        ASL 2.0
Group:		System/Base
URL:            http://www.docker.com
Source0:        https://%{import_path}/archive/v%{version}.tar.gz
Source1:	docker.rpmlintrc
Source2:	docker.conf
Patch0:		docker-1.9.1-dockeropts-service.patch
BuildRequires:  glibc-static-devel

BuildRequires:  golang
BuildRequires:  pkgconfig(sqlite3)

BuildRequires:  go-md2man
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-devel
BuildRequires:  pkgconfig(systemd)
Requires:       systemd-units

# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup
Requires:	e2fsprogs
Requires:	iptables

Obsoletes: docker-io < 1.2.0-8
Provides: docker-io = %{version}-%{release}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package devel
BuildRequires:  golang >= 1.3.3
Requires:       golang >= 1.3.3
Summary:        A golang registry for global request variables (source libraries)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/api) = %{version}-%{release}
Provides:       golang(%{import_path}/api/client) = %{version}-%{release}
Provides:       golang(%{import_path}/api/server) = %{version}-%{release}
Provides:       golang(%{import_path}/api/types) = %{version}-%{release}
Provides:       golang(%{import_path}/archive) = %{version}-%{release}
Provides:       golang(%{import_path}/builtins) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/overlay) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger/jsonfilelog) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/logger/syslog) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/dockerversion) = %{version}-%{release}
Provides:       golang(%{import_path}/engine) = %{version}-%{release}
Provides:       golang(%{import_path}/graph) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/integration) = %{version}-%{release}
Provides:       golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides:       golang(%{import_path}/links) = %{version}-%{release}
Provides:       golang(%{import_path}/nat) = %{version}-%{release}
Provides:       golang(%{import_path}/opts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term/winconsole) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/registry/v2) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/user) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/version) = %{version}-%{release}

%description devel
This is the source libraries for docker.

%package	vim
Summary:	vim syntax highlighting files for Docker
Requires:	%{name} = %{EVRD}
Requires:	vim

%description vim
This package installs %{summary}.

%prep
#%setup -q -n docker-%{commit}
%setup -q -n docker-%{version}
%apply_patches
#rm -rf vendor/src/code.google.com vendor/src/github.com/{coreos,docker/libtrust,godbus,gorilla,kr,syndtr,tchap}
#for f in `find . -name '*.go'`; do
	#perl -pi -e 's|github.com/docker/docker/vendor/src/code.google.com/p/go/src/pkg/archive/tar|archive/tar|' $f
#done

%build
export CC=gcc
export CXX=g++
sed -i 's!external!internal!g' hack/make.sh
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
export DOCKER_GITCOMMIT="%{shortcommit}"
export CGO_CFLAGS="-I%{_includedir}"
export CGO_LDFLAGS="-L%{_libdir}"
export AUTO_GOPATH=1

DEBUG=1 ./hack/make.sh dynbinary
./man/md2man-all.sh
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bundles/%{version}/dynbinary/docker-%{version} %{buildroot}%{_bindir}/docker

# install dockerinit
install -d %{buildroot}%{_libexecdir}/docker
install -p -m 755 bundles/%{version}/dynbinary/dockerinit-%{version} %{buildroot}%{_libexecdir}/docker/dockerinit

# Place to store images
install -d %{buildroot}%{_libexecdir}/cache/docker

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/man1/docker*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man/man5/Dockerfile.5 %{buildroot}%{_mandir}/man5

# sysconfig
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/docker
# install bash completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash
# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions
# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax
# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 755 contrib/udev/80-docker.rules %{buildroot}%{_udevrulesdir}
# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker
# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 contrib/init/systemd/docker.service %{buildroot}%{_unitdir}
install -p -m 644 contrib/init/systemd/docker.socket %{buildroot}%{_unitdir}

# It's convenient to have docker listening on a tcp port so add it
# the fd: param doesn't seem to work as well as the unix one
# Also use rather /var/cache to store images
perl -pi -e 's|-H fd://|-H unix://var/run/docker.sock -H tcp://127.0.0.1:2375 -g /var/cache/docker|'  %{buildroot}%{_unitdir}/docker.service
# Fix rights on docker socket so it can start - systemd should do it, but it's systemd you know !
perl -pi -e "s|^SocketUser|#Doesn't seem to work\nSocketUser|m" %{buildroot}%{_unitdir}/docker.socket
perl -pi -e "s|^SocketGroup=docker|SocketGroup=docker\n# So do it another way\nExecStartPost=/bin/chgrp docker /var/run/docker.sock|m"  %{buildroot}%{_unitdir}/docker.socket

# sources
install -d -p %{buildroot}/%{gosrc}

for dir in api autogen daemon \
           image opts pkg registry runconfig utils
do
	cp -rpav $dir %{buildroot}/%{gosrc}
done

find %{buildroot} -name "*~" -exec rm -rf {} \;
find %{buildroot}%{go_dir}/src/github.com/ -type d -exec chmod 0755 {} \;

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
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%doc LICENSE-vim-syntax README-vim-syntax.md
%{_mandir}/man1/docker*.1.gz
%{_mandir}/man5/Dockerfile.5.gz
%{_bindir}/docker
%dir %{_libexecdir}/docker
%dir %{_libexecdir}/cache/docker
%config(noreplace) %{_sysconfdir}/sysconfig/docker
%{_libexecdir}/docker/dockerinit
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker
%dir %{_udevrulesdir}
%{_udevrulesdir}/80-docker.rules

%files vim
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%files devel
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md
%dir %{go_dir}/src/%{provider}.%{provider_tld}/%{project}
%{go_dir}/src/%{import_path}
