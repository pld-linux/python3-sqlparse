#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Non-validating SQL parser
Summary(pl.UTF-8):	Parser SQL bez kontroli poprawności
Name:		python-sqlparse
# keep 0.3.x here for python2 support
Version:	0.3.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sqlparse/
Source0:	https://files.pythonhosted.org/packages/source/s/sqlparse/sqlparse-%{version}.tar.gz
# Source0-md5:	423047887a3590b04dd18f8caf843a2f
URL:		https://pypi.org/project/sqlparse/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sqlparse is a non-validating SQL parser for Python. It provides
support for parsing, splitting and formatting SQL statements.

%description -l pl.UTF-8
sqlparse to parser SQL dla Pythona nie sprawdzający poprawnosci.
Obsługuje analizę, podział i formatowanie zapytań SQL.

%package -n python3-sqlparse
Summary:	Non-validating SQL parser
Summary(pl.UTF-8):	Parser SQL bez kontroli poprawności
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-sqlparse
sqlparse is a non-validating SQL parser for Python. It provides
support for parsing, splitting and formatting SQL statements.

%description -n python3-sqlparse -l pl.UTF-8
sqlparse to parser SQL dla Pythona nie sprawdzający poprawnosci.
Obsługuje analizę, podział i formatowanie zapytań SQL.

%package apidocs
Summary:	API documentation for Python sqlparse module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sqlparse
Group:		Documentation

%description apidocs
API documentation for Python sqlparse module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sqlparse.

%prep
%setup -q -n sqlparse-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{sqlformat,sqlformat-2}
install -Dp docs/sqlformat.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlformat-2.1
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{sqlformat,sqlformat-3}
ln -s sqlformat-3 $RPM_BUILD_ROOT%{_bindir}/sqlformat
install -Dp docs/sqlformat.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlformat-3.1
echo '.so sqlformat-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/sqlformat.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE README.rst TODO
%attr(755,root,root) %{_bindir}/sqlformat-2
%{py_sitescriptdir}/sqlparse
%{py_sitescriptdir}/sqlparse-%{version}-py*.egg-info
%{_mandir}/man1/sqlformat-2.1*
%endif

%if %{with python3}
%files -n python3-sqlparse
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE README.rst TODO
%attr(755,root,root) %{_bindir}/sqlformat
%attr(755,root,root) %{_bindir}/sqlformat-3
%{py3_sitescriptdir}/sqlparse
%{py3_sitescriptdir}/sqlparse-%{version}-py*.egg-info
%{_mandir}/man1/sqlformat.1*
%{_mandir}/man1/sqlformat-3.1*
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
