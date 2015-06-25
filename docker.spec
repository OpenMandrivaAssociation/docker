%define _libexecdir /usr/libexec

# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_usrlibrpm}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global import_path github.com/docker/docker
%global gopath  %{_libdir}/golang
%define gosrc %{gopath}/src/%{import_path}

Name:           docker
Version:        1.6.2
Release:        1
Summary:        Automates deployment of containerized applications
License:        ASL 2.0
Group:		System/Kernel and hardware

URL:            http://www.docker.com
# only x86_64 for now: https://github.com/docker/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://%{import_path}/archive/v%{version}.tar.gz
#Source0:        https://%{import_path}/archive/%{commit}.tar.gz
Source100:	%{name}.rpmlintrc
BuildRequires:  gcc
BuildRequires:  glibc-static-devel

# ensure build uses golang 1.2-7 and above
# http://code.google.com/p/go/source/detail?r=a15f344a9efa35ef168c8feaa92a15a1cdc93db5
BuildRequires:  golang >= 1.3.3

BuildRequires:  sqlite3-devel

BuildRequires:  golang-net-devel
# Provided by this version of docker - doesn'- wompile without these versions
#BuildRequires:  golang(github.com/gorilla/mux)
#BuildRequires:  golang(github.com/gorilla/context)
#BuildRequires:  golang(github.com/kr/pty)
#BuildRequires:  golang(github.com/godbus/dbus)
#BuildRequires:  golang(github.com/coreos/go-systemd) >= 0-0.4
#BuildRequires:  golang(code.google.com/p/gosqlite/sqlite3)
#BuildRequires:  golang(github.com/syndtr/gocapability/capability)
#BuildRequires:  golang(github.com/docker/libcontainer)
#BuildRequires:  golang(github.com/tchap/go-patricia/patricia)
#BuildRequires:  golang(github.com/docker/libtrust)
#BuildRequires:  golang(github.com/docker/libtrust/trustgraph)

BuildRequires:  go-md2man
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-devel
BuildRequires:  pkgconfig(systemd)
Requires:       systemd-units

# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1035436
# this won't be needed for rhel7+
Requires:       bridge-utils
Requires:       lxc

# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup
Provides:       lxc-docker = %{version}

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
Requires:       docker-pkg-devel
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

%description devel
This is the source libraries for docker.

%package pkg-devel
BuildRequires:  golang >= 1.3.3
Requires:       golang >= 1.3.3
Summary:        A golang registry for global request variables (source libraries)
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

%description pkg-devel
These source librariees are provided by docker, but are independent of docker
specific logic. The import paths of %{import_path}/pkg/...

%prep
#%setup -q -n docker-%{commit}
%setup -q -n docker-%{version}
#rm -rf vendor/src/code.google.com vendor/src/github.com/{coreos,docker/libtrust,godbus,gorilla,kr,syndtr,tchap}
#for f in `find . -name '*.go'`; do
	#perl -pi -e 's|github.com/docker/docker/vendor/src/code.google.com/p/go/src/pkg/archive/tar|archive/tar|' $f
#done

%build
#mkdir -p _build

#pushd _build
  #mkdir -p src/github.com/docker
  #ln -s $(dirs +1 -l) src/github.com/docker/docker
#popd

export DOCKER_GITCOMMIT="%{shortcommit}"
#export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
#export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}

export CFLAGS="-I/usr/share/go/src/runtime"
AUTO_GOPATH=1 ./hack/make.sh dynbinary
#hack/make.sh dynbinary
docs/man/md2man-all.sh
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
install -p -m 644 docs/man/man1/docker*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 docs/man/man5/Dockerfile.5 %{buildroot}%{_mandir}/man5

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

for dir in api autogen builtins daemon engine graph \
           image links nat opts pkg registry runconfig utils
do
	cp -rpav $dir %{buildroot}/%{gosrc}
done

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
%{_libexecdir}/docker/dockerinit
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker
%dir %{_udevrulesdir}
%{_udevrulesdir}/80-docker.rules
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%files devel
%dir %{gosrc}
%dir %{gosrc}/api
%{gosrc}/api/README.md
%{gosrc}/api/*.go
%dir %{gosrc}/api/client
%{gosrc}/api/client/*.go
%dir %{gosrc}/api/server
%{gosrc}/api/server/*.go
%dir %{gosrc}/api/types
%{gosrc}/api/types/*.go
%dir %{gosrc}/autogen/dockerversion
%{gosrc}/autogen/dockerversion/*.go
%dir %{gosrc}/builtins
%{gosrc}/builtins/*.go
%dir %{gosrc}/daemon
%{gosrc}/daemon/*.go
%{gosrc}/daemon/README.md
%dir %{gosrc}/daemon/execdriver
%{gosrc}/daemon/execdriver/*.go
%dir %{gosrc}/daemon/execdriver/execdrivers
%{gosrc}/daemon/execdriver/execdrivers/*.go
%dir %{gosrc}/daemon/execdriver/lxc
%{gosrc}/daemon/execdriver/lxc/*.go
%dir %{gosrc}/daemon/execdriver/native
%{gosrc}/daemon/execdriver/native/*.go
%dir %{gosrc}/daemon/execdriver/native/template
%{gosrc}/daemon/execdriver/native/template/*.go
%dir %{gosrc}/daemon/graphdriver
%{gosrc}/daemon/graphdriver/*.go
%dir %{gosrc}/daemon/graphdriver/aufs
%{gosrc}/daemon/graphdriver/aufs/*.go
%dir %{gosrc}/daemon/graphdriver/btrfs
%{gosrc}/daemon/graphdriver/btrfs/*.go
%dir %{gosrc}/daemon/graphdriver/devmapper
%{gosrc}/daemon/graphdriver/devmapper/*.go
%{gosrc}/daemon/graphdriver/devmapper/README.md
%dir %{gosrc}/daemon/graphdriver/graphtest
%{gosrc}/daemon/graphdriver/graphtest/*.go
%dir %{gosrc}/daemon/graphdriver/overlay
%{gosrc}/daemon/graphdriver/overlay/*.go
%dir %{gosrc}/daemon/graphdriver/vfs
%{gosrc}/daemon/graphdriver/vfs/*.go
%dir %{gosrc}/daemon/logger
%{gosrc}/daemon/logger/*.go
%dir %{gosrc}/daemon/logger/jsonfilelog
%{gosrc}/daemon/logger/jsonfilelog/*.go
%dir %{gosrc}/daemon/logger/syslog
%{gosrc}/daemon/logger/syslog/*.go
%dir %{gosrc}/daemon/networkdriver
%dir %{gosrc}/daemon/networkdriver/bridge
%{gosrc}/daemon/networkdriver/bridge/*.go
%dir %{gosrc}/daemon/networkdriver/ipallocator
%{gosrc}/daemon/networkdriver/ipallocator/*.go
%{gosrc}/daemon/networkdriver/*.go
%dir %{gosrc}/daemon/networkdriver/portallocator
%{gosrc}/daemon/networkdriver/portallocator/*.go
%dir %{gosrc}/daemon/networkdriver/portmapper
%{gosrc}/daemon/networkdriver/portmapper/*.go
%dir %{gosrc}/engine
%{gosrc}/engine/*.go
%dir %{gosrc}/graph
%{gosrc}/graph/*.go
%dir %{gosrc}/image
%{gosrc}/image/*.go
%dir %{gosrc}/image/spec
%{gosrc}/image/spec/*.md
%dir %{gosrc}/links
%{gosrc}/links/*.go
%dir %{gosrc}/nat
%{gosrc}/nat/*.go
%dir %{gosrc}/opts
%{gosrc}/opts/*.go
%dir %{gosrc}/pkg
%dir %{gosrc}/pkg/term
%dir %{gosrc}/pkg/term/winconsole
%{gosrc}/pkg/term/winconsole/*.go
%dir %{gosrc}/registry
%dir %{gosrc}/registry/v2
%{gosrc}/registry/*.go
%{gosrc}/registry/v2/*.go
%dir %{gosrc}/runconfig
%{gosrc}/runconfig/*.go
%dir %{gosrc}/utils
%{gosrc}/utils/*.go

%files pkg-devel
%dir %{gosrc}
%dir %{gosrc}/pkg
%{gosrc}/pkg/README.md
%dir %{gosrc}/pkg/archive
%{gosrc}/pkg/*/README.md
%{gosrc}/pkg/*/LICENSE*
%{gosrc}/pkg/*/*.go
%dir %{gosrc}/pkg/archive/testdata
%{gosrc}/pkg/archive/testdata/broken.tar
%dir %{gosrc}/pkg/mflag/example
%{gosrc}/pkg/mflag/example/example.go
%dir %{gosrc}/pkg/networkfs/etchosts
%dir %{gosrc}/pkg/networkfs/resolvconf
%{gosrc}/pkg/networkfs/*/*.go
%dir %{gosrc}/pkg/parsers/filters
%dir %{gosrc}/pkg/parsers/kernel
%{gosrc}/pkg/parsers/*/*.go
%{gosrc}/pkg/tarsum/tarsum_spec.md
%dir %{gosrc}/pkg/tarsum/testdata
%dir %{gosrc}/pkg/tarsum/testdata/collision
%dir %{gosrc}/pkg/tarsum/testdata/xattr
%dir %{gosrc}/pkg/tarsum/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457
%dir %{gosrc}/pkg/tarsum/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158
%{gosrc}/pkg/tarsum/testdata/*/*
