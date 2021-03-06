%define __prefix /opt
%define __spec_install_post /usr/lib/rpm/brp-compress || :

Name: %{name}
Summary: %{summary}
Version: %{version}
Release: %{release}%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Requires: %{requires}
BuildRequires: %{buildrequires}
License: proprietary
Group: Apps/sys
Autoreq: 0


%description
%{name} built with generic node project spec

%prep
if [ -d %{name} ]; then
    echo "Cleaning out stale build directory" 1>&2
    rm -rf %{name}
fi

%pre
/usr/bin/getent group %{name} || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} || /usr/sbin/useradd -r -d /opt/%{name}/ -s /bin/false %{name} -g %{name}


%build

mkdir -p %{name}
cp -r '%{source}' %{name}/src
rm -rf %{name}/src/.git*
rm -rf %{name}/src/rpmtools/.git*
rm -rf %{name}/src/.idea*


pushd %{name}/src
    if [ -e "package.json" ]
    then
        HASH=$(cat package.json | grep -v 'version' | md5sum | awk '{ print $1 }')
        CACHED_NODE_MODULES="/tmp/node_modules_${HASH}.tar"
        if [ -e "${CACHED_NODE_MODULES}" ]
        then
          echo "Found cached node_modules: ${CACHED_NODE_MODULES}, use it"
          tar xf ${CACHED_NODE_MODULES} ./
        else
          echo "No found cached node_modules, download..."
          npm install || exit 1
          echo "Save node_modules into cache: ${CACHED_NODE_MODULES}"
          tar cf ${CACHED_NODE_MODULES} ./node_modules || true
        fi
    fi

    for i in $(%{meta} excludeFiles); do
        echo "Remove files: ${i}"
        rm -rf ${i}
    done
popd

%install
mkdir -p %{buildroot}%{__prefix}/%{name}
mv %{name} %{buildroot}%{__prefix}/

%{__install} -p -D -m 0755 %{buildroot}%{__prefix}/%{name}/src/rpmtools/node/init.d/main.init.sh %{buildroot}%{_initrddir}/%{name}


mkdir -p %{buildroot}%{_sysconfdir}/%{name}
touch %{buildroot}%{_sysconfdir}/%{name}/production.json

# configs
rm -rf %{buildroot}%{__prefix}/%{name}/src/rpmtools
mkdir -p %{buildroot}/var/run/%{name}

%post
if [ $1 -gt 1 ]; then
    echo "Upgrade"
else
    echo "Install"
    /sbin/chkconfig --list %{name} > /dev/null 2>&1 || /sbin/chkconfig --add %{name}
    /sbin/chkconfig %{name} on

    mkdir -p /var/log/%{name}
    chown -R %{name}:%{name} /var/log/%{name}
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_initrddir}/%{name}
%{__prefix}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/production.json
%defattr(-,%{name},%{name})
/var/run/%{name}/