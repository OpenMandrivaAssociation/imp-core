%define section         free
%define gcj_support     1
%bcond_without          bootstrap

Name:           imp-core
Version:        0.7.8
Release:        %mkrel 0.0.5
Epoch:          0
Summary:        org.freecompany.imp.core
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
Source0:        http://repository.freecompany.org/org/freecompany/imp/zips/imp-core-src-0.7.8.zip
Source1:        imp-core-0.7.8-build.xml
Requires:       brimstone-cache
Requires:       brimstone-core
Requires:       brimstone-main
Requires:       brimstone-module
Requires:       infoset
Requires:       util-multicaster
Requires:       xmlwriter
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  ant-nodeps
BuildRequires:  brimstone-cache
BuildRequires:  brimstone-core
BuildRequires:  brimstone-main
BuildRequires:  brimstone-module
%if %without bootstrap
BuildRequires:  imp-core
%endif
BuildRequires:  infoset
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
BuildRequires:  util-multicaster
BuildRequires:  xmlwriter
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.imp.core

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%if %with bootstrap
%{__cp} -a %{SOURCE1} build.xml
%endif
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit brimstone-cache brimstone-core brimstone-main brimstone-module infoset util-multicaster xmlwriter)
%if %without bootstrap
export CLASSPATH=${CLASSPATH}:$(build-classpath imp-core)
%endif
export OPT_JAR_LIST="ant/ant-junit ant/ant-nodeps"
%{ant} jar javadoc test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
