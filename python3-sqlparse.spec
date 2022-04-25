#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Non-validating SQL parser
Summary(pl.UTF-8):	Parser SQL bez kontroli poprawności
Name:		python3-sqlparse
Version:	0.4.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sqlparse/
Source0:	https://files.pythonhosted.org/packages/source/s/sqlparse/sqlparse-%{version}.tar.gz
# Source0-md5:	66dce30d92823589f5e5e043f90b4f16
URL:		https://pypi.org/project/sqlparse/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sqlparse is a non-validating SQL parser for Python. It provides
support for parsing, splitting and formatting SQL statements.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{sqlformat,sqlformat-3}
ln -s sqlformat-3 $RPM_BUILD_ROOT%{_bindir}/sqlformat
install -Dp docs/sqlformat.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlformat-3.1
echo '.so sqlformat-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/sqlformat.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE README.rst TODO
%attr(755,root,root) %{_bindir}/sqlformat
%attr(755,root,root) %{_bindir}/sqlformat-3
%{py3_sitescriptdir}/sqlparse
%{py3_sitescriptdir}/sqlparse-%{version}-py*.egg-info
%{_mandir}/man1/sqlformat.1*
%{_mandir}/man1/sqlformat-3.1*

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
