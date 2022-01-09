[01;34m.[00m
├── db_schema.drawio
├── db.sqlite
├── [01;34mduchamp_reader[00m
│   ├── app.py
│   ├── constantes.py
│   ├── __init__.py
│   ├── [01;34mmodeles[00m
│   │   ├── classes_generic.py
│   │   ├── classes_users.py
│   │   ├── __init__.py
│   │   └── new_artist_todelete.py
│   ├── [01;34m__pycache__[00m
│   ├── regex.py
│   ├── routes.py
│   ├── [01;34mstatic[00m
│   └── [01;34mtemplates[00m
│       ├── [01;34mpages[00m
│       │   ├── about.html
│       │   ├── accueil.html
│       │   └── artiste.html
│       └── [01;34mpartials[00m
├── [01;34menv_duchamp_reader[00m
│   ├── [01;34mbin[00m
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── [01;32measy_install[00m
│   │   ├── [01;32measy_install-3.8[00m
│   │   ├── [01;32mflask[00m
│   │   ├── [01;32mpip[00m
│   │   ├── [01;32mpip3[00m
│   │   ├── [01;32mpip3.8[00m
│   │   ├── [01;36mpython[00m -> [01;32mpython3[00m
│   │   └── [01;36mpython3[00m -> [01;32m/home/paulhector/.cours-python/bin/python3[00m
│   ├── [01;34minclude[00m
│   │   └── [01;34msite[00m
│   │       └── [01;34mpython3.8[00m
│   │           └── [01;34mgreenlet[00m
│   │               └── greenlet.h
│   ├── [01;34mlib[00m
│   │   └── [01;34mpython3.8[00m
│   │       └── [01;34msite-packages[00m
│   │           ├── [01;34mclick[00m
│   │           │   ├── _compat.py
│   │           │   ├── core.py
│   │           │   ├── decorators.py
│   │           │   ├── exceptions.py
│   │           │   ├── formatting.py
│   │           │   ├── globals.py
│   │           │   ├── __init__.py
│   │           │   ├── parser.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── _compat.cpython-38.pyc
│   │           │   │   ├── core.cpython-38.pyc
│   │           │   │   ├── decorators.cpython-38.pyc
│   │           │   │   ├── exceptions.cpython-38.pyc
│   │           │   │   ├── formatting.cpython-38.pyc
│   │           │   │   ├── globals.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── parser.cpython-38.pyc
│   │           │   │   ├── shell_completion.cpython-38.pyc
│   │           │   │   ├── termui.cpython-38.pyc
│   │           │   │   ├── _termui_impl.cpython-38.pyc
│   │           │   │   ├── testing.cpython-38.pyc
│   │           │   │   ├── _textwrap.cpython-38.pyc
│   │           │   │   ├── types.cpython-38.pyc
│   │           │   │   ├── _unicodefun.cpython-38.pyc
│   │           │   │   ├── utils.cpython-38.pyc
│   │           │   │   └── _winconsole.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── shell_completion.py
│   │           │   ├── _termui_impl.py
│   │           │   ├── termui.py
│   │           │   ├── testing.py
│   │           │   ├── _textwrap.py
│   │           │   ├── types.py
│   │           │   ├── _unicodefun.py
│   │           │   ├── utils.py
│   │           │   └── _winconsole.py
│   │           ├── [01;34mclick-8.0.3.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── easy_install.py
│   │           ├── [01;34mflask[00m
│   │           │   ├── app.py
│   │           │   ├── blueprints.py
│   │           │   ├── cli.py
│   │           │   ├── config.py
│   │           │   ├── ctx.py
│   │           │   ├── debughelpers.py
│   │           │   ├── globals.py
│   │           │   ├── helpers.py
│   │           │   ├── __init__.py
│   │           │   ├── [01;34mjson[00m
│   │           │   │   ├── __init__.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   └── tag.cpython-38.pyc
│   │           │   │   └── tag.py
│   │           │   ├── logging.py
│   │           │   ├── __main__.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── app.cpython-38.pyc
│   │           │   │   ├── blueprints.cpython-38.pyc
│   │           │   │   ├── cli.cpython-38.pyc
│   │           │   │   ├── config.cpython-38.pyc
│   │           │   │   ├── ctx.cpython-38.pyc
│   │           │   │   ├── debughelpers.cpython-38.pyc
│   │           │   │   ├── globals.cpython-38.pyc
│   │           │   │   ├── helpers.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── logging.cpython-38.pyc
│   │           │   │   ├── __main__.cpython-38.pyc
│   │           │   │   ├── scaffold.cpython-38.pyc
│   │           │   │   ├── sessions.cpython-38.pyc
│   │           │   │   ├── signals.cpython-38.pyc
│   │           │   │   ├── templating.cpython-38.pyc
│   │           │   │   ├── testing.cpython-38.pyc
│   │           │   │   ├── typing.cpython-38.pyc
│   │           │   │   ├── views.cpython-38.pyc
│   │           │   │   └── wrappers.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── scaffold.py
│   │           │   ├── sessions.py
│   │           │   ├── signals.py
│   │           │   ├── templating.py
│   │           │   ├── testing.py
│   │           │   ├── typing.py
│   │           │   ├── views.py
│   │           │   └── wrappers.py
│   │           ├── [01;34mFlask-2.0.2.dist-info[00m
│   │           │   ├── entry_points.txt
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mflask_login[00m
│   │           │   ├── __about__.py
│   │           │   ├── _compat.py
│   │           │   ├── config.py
│   │           │   ├── __init__.py
│   │           │   ├── login_manager.py
│   │           │   ├── mixins.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── __about__.cpython-38.pyc
│   │           │   │   ├── _compat.cpython-38.pyc
│   │           │   │   ├── config.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── login_manager.cpython-38.pyc
│   │           │   │   ├── mixins.cpython-38.pyc
│   │           │   │   ├── signals.cpython-38.pyc
│   │           │   │   ├── test_client.cpython-38.pyc
│   │           │   │   └── utils.cpython-38.pyc
│   │           │   ├── signals.py
│   │           │   ├── test_client.py
│   │           │   └── utils.py
│   │           ├── [01;34mFlask_Login-0.5.0.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mflask_sqlalchemy[00m
│   │           │   ├── _compat.py
│   │           │   ├── __init__.py
│   │           │   ├── model.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── _compat.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── model.cpython-38.pyc
│   │           │   │   └── utils.cpython-38.pyc
│   │           │   └── utils.py
│   │           ├── [01;34mFlask_SQLAlchemy-2.5.1.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mgreenlet[00m
│   │           │   ├── greenlet.c
│   │           │   ├── [01;32m_greenlet.cpython-38-x86_64-linux-gnu.so[00m
│   │           │   ├── greenlet.h
│   │           │   ├── __init__.py
│   │           │   ├── [01;34mplatform[00m
│   │           │   │   ├── setup_switch_x64_masm.cmd
│   │           │   │   ├── switch_aarch64_gcc.h
│   │           │   │   ├── switch_alpha_unix.h
│   │           │   │   ├── switch_amd64_unix.h
│   │           │   │   ├── switch_arm32_gcc.h
│   │           │   │   ├── switch_arm32_ios.h
│   │           │   │   ├── switch_csky_gcc.h
│   │           │   │   ├── switch_m68k_gcc.h
│   │           │   │   ├── switch_mips_unix.h
│   │           │   │   ├── switch_ppc64_aix.h
│   │           │   │   ├── switch_ppc64_linux.h
│   │           │   │   ├── switch_ppc_aix.h
│   │           │   │   ├── switch_ppc_linux.h
│   │           │   │   ├── switch_ppc_macosx.h
│   │           │   │   ├── switch_ppc_unix.h
│   │           │   │   ├── switch_riscv_unix.h
│   │           │   │   ├── switch_s390_unix.h
│   │           │   │   ├── switch_sparc_sun_gcc.h
│   │           │   │   ├── switch_x32_unix.h
│   │           │   │   ├── switch_x64_masm.asm
│   │           │   │   ├── switch_x64_masm.obj
│   │           │   │   ├── switch_x64_msvc.h
│   │           │   │   ├── switch_x86_msvc.h
│   │           │   │   └── switch_x86_unix.h
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   └── __init__.cpython-38.pyc
│   │           │   ├── slp_platformselect.h
│   │           │   └── [01;34mtests[00m
│   │           │       ├── __init__.py
│   │           │       ├── [01;34m__pycache__[00m
│   │           │       │   ├── __init__.cpython-38.pyc
│   │           │       │   ├── test_contextvars.cpython-38.pyc
│   │           │       │   ├── test_cpp.cpython-38.pyc
│   │           │       │   ├── test_extension_interface.cpython-38.pyc
│   │           │       │   ├── test_gc.cpython-38.pyc
│   │           │       │   ├── test_generator.cpython-38.pyc
│   │           │       │   ├── test_generator_nested.cpython-38.pyc
│   │           │       │   ├── test_greenlet.cpython-38.pyc
│   │           │       │   ├── test_leaks.cpython-38.pyc
│   │           │       │   ├── test_stack_saved.cpython-38.pyc
│   │           │       │   ├── test_throw.cpython-38.pyc
│   │           │       │   ├── test_tracing.cpython-38.pyc
│   │           │       │   ├── test_version.cpython-38.pyc
│   │           │       │   └── test_weakref.cpython-38.pyc
│   │           │       ├── test_contextvars.py
│   │           │       ├── test_cpp.py
│   │           │       ├── _test_extension.c
│   │           │       ├── _test_extension_cpp.cpp
│   │           │       ├── [01;32m_test_extension_cpp.cpython-38-x86_64-linux-gnu.so[00m
│   │           │       ├── [01;32m_test_extension.cpython-38-x86_64-linux-gnu.so[00m
│   │           │       ├── test_extension_interface.py
│   │           │       ├── test_gc.py
│   │           │       ├── test_generator_nested.py
│   │           │       ├── test_generator.py
│   │           │       ├── test_greenlet.py
│   │           │       ├── test_leaks.py
│   │           │       ├── test_stack_saved.py
│   │           │       ├── test_throw.py
│   │           │       ├── test_tracing.py
│   │           │       ├── test_version.py
│   │           │       └── test_weakref.py
│   │           ├── [01;34mgreenlet-1.1.2.dist-info[00m
│   │           │   ├── AUTHORS
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── LICENSE.PSF
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mitsdangerous[00m
│   │           │   ├── encoding.py
│   │           │   ├── exc.py
│   │           │   ├── __init__.py
│   │           │   ├── _json.py
│   │           │   ├── jws.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── encoding.cpython-38.pyc
│   │           │   │   ├── exc.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── _json.cpython-38.pyc
│   │           │   │   ├── jws.cpython-38.pyc
│   │           │   │   ├── serializer.cpython-38.pyc
│   │           │   │   ├── signer.cpython-38.pyc
│   │           │   │   ├── timed.cpython-38.pyc
│   │           │   │   └── url_safe.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── serializer.py
│   │           │   ├── signer.py
│   │           │   ├── timed.py
│   │           │   └── url_safe.py
│   │           ├── [01;34mitsdangerous-2.0.1.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mjinja2[00m
│   │           │   ├── async_utils.py
│   │           │   ├── bccache.py
│   │           │   ├── compiler.py
│   │           │   ├── constants.py
│   │           │   ├── debug.py
│   │           │   ├── defaults.py
│   │           │   ├── environment.py
│   │           │   ├── exceptions.py
│   │           │   ├── ext.py
│   │           │   ├── filters.py
│   │           │   ├── _identifier.py
│   │           │   ├── idtracking.py
│   │           │   ├── __init__.py
│   │           │   ├── lexer.py
│   │           │   ├── loaders.py
│   │           │   ├── meta.py
│   │           │   ├── nativetypes.py
│   │           │   ├── nodes.py
│   │           │   ├── optimizer.py
│   │           │   ├── parser.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── async_utils.cpython-38.pyc
│   │           │   │   ├── bccache.cpython-38.pyc
│   │           │   │   ├── compiler.cpython-38.pyc
│   │           │   │   ├── constants.cpython-38.pyc
│   │           │   │   ├── debug.cpython-38.pyc
│   │           │   │   ├── defaults.cpython-38.pyc
│   │           │   │   ├── environment.cpython-38.pyc
│   │           │   │   ├── exceptions.cpython-38.pyc
│   │           │   │   ├── ext.cpython-38.pyc
│   │           │   │   ├── filters.cpython-38.pyc
│   │           │   │   ├── _identifier.cpython-38.pyc
│   │           │   │   ├── idtracking.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── lexer.cpython-38.pyc
│   │           │   │   ├── loaders.cpython-38.pyc
│   │           │   │   ├── meta.cpython-38.pyc
│   │           │   │   ├── nativetypes.cpython-38.pyc
│   │           │   │   ├── nodes.cpython-38.pyc
│   │           │   │   ├── optimizer.cpython-38.pyc
│   │           │   │   ├── parser.cpython-38.pyc
│   │           │   │   ├── runtime.cpython-38.pyc
│   │           │   │   ├── sandbox.cpython-38.pyc
│   │           │   │   ├── tests.cpython-38.pyc
│   │           │   │   ├── utils.cpython-38.pyc
│   │           │   │   └── visitor.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── runtime.py
│   │           │   ├── sandbox.py
│   │           │   ├── tests.py
│   │           │   ├── utils.py
│   │           │   └── visitor.py
│   │           ├── [01;34mJinja2-3.0.3.dist-info[00m
│   │           │   ├── entry_points.txt
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mmarkupsafe[00m
│   │           │   ├── __init__.py
│   │           │   ├── _native.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   └── _native.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── _speedups.c
│   │           │   ├── [01;32m_speedups.cpython-38-x86_64-linux-gnu.so[00m
│   │           │   └── _speedups.pyi
│   │           ├── [01;34mMarkupSafe-2.0.1.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.rst
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mpip[00m
│   │           │   ├── __init__.py
│   │           │   ├── [01;34m_internal[00m
│   │           │   │   ├── build_env.py
│   │           │   │   ├── cache.py
│   │           │   │   ├── [01;34mcli[00m
│   │           │   │   │   ├── autocompletion.py
│   │           │   │   │   ├── base_command.py
│   │           │   │   │   ├── cmdoptions.py
│   │           │   │   │   ├── command_context.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── main_parser.py
│   │           │   │   │   ├── main.py
│   │           │   │   │   ├── parser.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── autocompletion.cpython-38.pyc
│   │           │   │   │   │   ├── base_command.cpython-38.pyc
│   │           │   │   │   │   ├── cmdoptions.cpython-38.pyc
│   │           │   │   │   │   ├── command_context.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── main.cpython-38.pyc
│   │           │   │   │   │   ├── main_parser.cpython-38.pyc
│   │           │   │   │   │   ├── parser.cpython-38.pyc
│   │           │   │   │   │   ├── req_command.cpython-38.pyc
│   │           │   │   │   │   └── status_codes.cpython-38.pyc
│   │           │   │   │   ├── req_command.py
│   │           │   │   │   └── status_codes.py
│   │           │   │   ├── [01;34mcommands[00m
│   │           │   │   │   ├── check.py
│   │           │   │   │   ├── completion.py
│   │           │   │   │   ├── configuration.py
│   │           │   │   │   ├── debug.py
│   │           │   │   │   ├── download.py
│   │           │   │   │   ├── freeze.py
│   │           │   │   │   ├── hash.py
│   │           │   │   │   ├── help.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── install.py
│   │           │   │   │   ├── list.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── check.cpython-38.pyc
│   │           │   │   │   │   ├── completion.cpython-38.pyc
│   │           │   │   │   │   ├── configuration.cpython-38.pyc
│   │           │   │   │   │   ├── debug.cpython-38.pyc
│   │           │   │   │   │   ├── download.cpython-38.pyc
│   │           │   │   │   │   ├── freeze.cpython-38.pyc
│   │           │   │   │   │   ├── hash.cpython-38.pyc
│   │           │   │   │   │   ├── help.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── install.cpython-38.pyc
│   │           │   │   │   │   ├── list.cpython-38.pyc
│   │           │   │   │   │   ├── search.cpython-38.pyc
│   │           │   │   │   │   ├── show.cpython-38.pyc
│   │           │   │   │   │   ├── uninstall.cpython-38.pyc
│   │           │   │   │   │   └── wheel.cpython-38.pyc
│   │           │   │   │   ├── search.py
│   │           │   │   │   ├── show.py
│   │           │   │   │   ├── uninstall.py
│   │           │   │   │   └── wheel.py
│   │           │   │   ├── configuration.py
│   │           │   │   ├── [01;34mdistributions[00m
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── installed.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── installed.cpython-38.pyc
│   │           │   │   │   │   ├── sdist.cpython-38.pyc
│   │           │   │   │   │   └── wheel.cpython-38.pyc
│   │           │   │   │   ├── sdist.py
│   │           │   │   │   └── wheel.py
│   │           │   │   ├── exceptions.py
│   │           │   │   ├── [01;34mindex[00m
│   │           │   │   │   ├── collector.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── package_finder.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       ├── collector.cpython-38.pyc
│   │           │   │   │       ├── __init__.cpython-38.pyc
│   │           │   │   │       └── package_finder.cpython-38.pyc
│   │           │   │   ├── __init__.py
│   │           │   │   ├── legacy_resolve.py
│   │           │   │   ├── locations.py
│   │           │   │   ├── main.py
│   │           │   │   ├── [01;34mmodels[00m
│   │           │   │   │   ├── candidate.py
│   │           │   │   │   ├── format_control.py
│   │           │   │   │   ├── index.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── link.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── candidate.cpython-38.pyc
│   │           │   │   │   │   ├── format_control.cpython-38.pyc
│   │           │   │   │   │   ├── index.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── link.cpython-38.pyc
│   │           │   │   │   │   ├── scheme.cpython-38.pyc
│   │           │   │   │   │   ├── search_scope.cpython-38.pyc
│   │           │   │   │   │   ├── selection_prefs.cpython-38.pyc
│   │           │   │   │   │   ├── target_python.cpython-38.pyc
│   │           │   │   │   │   └── wheel.cpython-38.pyc
│   │           │   │   │   ├── scheme.py
│   │           │   │   │   ├── search_scope.py
│   │           │   │   │   ├── selection_prefs.py
│   │           │   │   │   ├── target_python.py
│   │           │   │   │   └── wheel.py
│   │           │   │   ├── [01;34mnetwork[00m
│   │           │   │   │   ├── auth.py
│   │           │   │   │   ├── cache.py
│   │           │   │   │   ├── download.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── auth.cpython-38.pyc
│   │           │   │   │   │   ├── cache.cpython-38.pyc
│   │           │   │   │   │   ├── download.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── session.cpython-38.pyc
│   │           │   │   │   │   ├── utils.cpython-38.pyc
│   │           │   │   │   │   └── xmlrpc.cpython-38.pyc
│   │           │   │   │   ├── session.py
│   │           │   │   │   ├── utils.py
│   │           │   │   │   └── xmlrpc.py
│   │           │   │   ├── [01;34moperations[00m
│   │           │   │   │   ├── [01;34mbuild[00m
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── metadata_legacy.py
│   │           │   │   │   │   ├── metadata.py
│   │           │   │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   │   ├── metadata.cpython-38.pyc
│   │           │   │   │   │   │   ├── metadata_legacy.cpython-38.pyc
│   │           │   │   │   │   │   ├── wheel.cpython-38.pyc
│   │           │   │   │   │   │   └── wheel_legacy.cpython-38.pyc
│   │           │   │   │   │   ├── wheel_legacy.py
│   │           │   │   │   │   └── wheel.py
│   │           │   │   │   ├── check.py
│   │           │   │   │   ├── freeze.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── [01;34minstall[00m
│   │           │   │   │   │   ├── editable_legacy.py
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── legacy.py
│   │           │   │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   │   ├── editable_legacy.cpython-38.pyc
│   │           │   │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   │   ├── legacy.cpython-38.pyc
│   │           │   │   │   │   │   └── wheel.cpython-38.pyc
│   │           │   │   │   │   └── wheel.py
│   │           │   │   │   ├── prepare.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       ├── check.cpython-38.pyc
│   │           │   │   │       ├── freeze.cpython-38.pyc
│   │           │   │   │       ├── __init__.cpython-38.pyc
│   │           │   │   │       └── prepare.cpython-38.pyc
│   │           │   │   ├── pep425tags.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── build_env.cpython-38.pyc
│   │           │   │   │   ├── cache.cpython-38.pyc
│   │           │   │   │   ├── configuration.cpython-38.pyc
│   │           │   │   │   ├── exceptions.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── legacy_resolve.cpython-38.pyc
│   │           │   │   │   ├── locations.cpython-38.pyc
│   │           │   │   │   ├── main.cpython-38.pyc
│   │           │   │   │   ├── pep425tags.cpython-38.pyc
│   │           │   │   │   ├── pyproject.cpython-38.pyc
│   │           │   │   │   ├── self_outdated_check.cpython-38.pyc
│   │           │   │   │   └── wheel_builder.cpython-38.pyc
│   │           │   │   ├── pyproject.py
│   │           │   │   ├── [01;34mreq[00m
│   │           │   │   │   ├── constructors.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── constructors.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── req_file.cpython-38.pyc
│   │           │   │   │   │   ├── req_install.cpython-38.pyc
│   │           │   │   │   │   ├── req_set.cpython-38.pyc
│   │           │   │   │   │   ├── req_tracker.cpython-38.pyc
│   │           │   │   │   │   └── req_uninstall.cpython-38.pyc
│   │           │   │   │   ├── req_file.py
│   │           │   │   │   ├── req_install.py
│   │           │   │   │   ├── req_set.py
│   │           │   │   │   ├── req_tracker.py
│   │           │   │   │   └── req_uninstall.py
│   │           │   │   ├── self_outdated_check.py
│   │           │   │   ├── [01;34mutils[00m
│   │           │   │   │   ├── appdirs.py
│   │           │   │   │   ├── compat.py
│   │           │   │   │   ├── deprecation.py
│   │           │   │   │   ├── distutils_args.py
│   │           │   │   │   ├── encoding.py
│   │           │   │   │   ├── entrypoints.py
│   │           │   │   │   ├── filesystem.py
│   │           │   │   │   ├── filetypes.py
│   │           │   │   │   ├── glibc.py
│   │           │   │   │   ├── hashes.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── inject_securetransport.py
│   │           │   │   │   ├── logging.py
│   │           │   │   │   ├── marker_files.py
│   │           │   │   │   ├── misc.py
│   │           │   │   │   ├── models.py
│   │           │   │   │   ├── packaging.py
│   │           │   │   │   ├── pkg_resources.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── appdirs.cpython-38.pyc
│   │           │   │   │   │   ├── compat.cpython-38.pyc
│   │           │   │   │   │   ├── deprecation.cpython-38.pyc
│   │           │   │   │   │   ├── distutils_args.cpython-38.pyc
│   │           │   │   │   │   ├── encoding.cpython-38.pyc
│   │           │   │   │   │   ├── entrypoints.cpython-38.pyc
│   │           │   │   │   │   ├── filesystem.cpython-38.pyc
│   │           │   │   │   │   ├── filetypes.cpython-38.pyc
│   │           │   │   │   │   ├── glibc.cpython-38.pyc
│   │           │   │   │   │   ├── hashes.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── inject_securetransport.cpython-38.pyc
│   │           │   │   │   │   ├── logging.cpython-38.pyc
│   │           │   │   │   │   ├── marker_files.cpython-38.pyc
│   │           │   │   │   │   ├── misc.cpython-38.pyc
│   │           │   │   │   │   ├── models.cpython-38.pyc
│   │           │   │   │   │   ├── packaging.cpython-38.pyc
│   │           │   │   │   │   ├── pkg_resources.cpython-38.pyc
│   │           │   │   │   │   ├── setuptools_build.cpython-38.pyc
│   │           │   │   │   │   ├── subprocess.cpython-38.pyc
│   │           │   │   │   │   ├── temp_dir.cpython-38.pyc
│   │           │   │   │   │   ├── typing.cpython-38.pyc
│   │           │   │   │   │   ├── ui.cpython-38.pyc
│   │           │   │   │   │   ├── unpacking.cpython-38.pyc
│   │           │   │   │   │   ├── urls.cpython-38.pyc
│   │           │   │   │   │   ├── virtualenv.cpython-38.pyc
│   │           │   │   │   │   └── wheel.cpython-38.pyc
│   │           │   │   │   ├── setuptools_build.py
│   │           │   │   │   ├── subprocess.py
│   │           │   │   │   ├── temp_dir.py
│   │           │   │   │   ├── typing.py
│   │           │   │   │   ├── ui.py
│   │           │   │   │   ├── unpacking.py
│   │           │   │   │   ├── urls.py
│   │           │   │   │   ├── virtualenv.py
│   │           │   │   │   └── wheel.py
│   │           │   │   ├── [01;34mvcs[00m
│   │           │   │   │   ├── bazaar.py
│   │           │   │   │   ├── git.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── mercurial.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── bazaar.cpython-38.pyc
│   │           │   │   │   │   ├── git.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── mercurial.cpython-38.pyc
│   │           │   │   │   │   ├── subversion.cpython-38.pyc
│   │           │   │   │   │   └── versioncontrol.cpython-38.pyc
│   │           │   │   │   ├── subversion.py
│   │           │   │   │   └── versioncontrol.py
│   │           │   │   └── wheel_builder.py
│   │           │   ├── __main__.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   └── __main__.cpython-38.pyc
│   │           │   └── [01;34m_vendor[00m
│   │           │       ├── __init__.py
│   │           │       └── [01;34m__pycache__[00m
│   │           │           └── __init__.cpython-38.pyc
│   │           ├── [01;34mpip-20.0.2.dist-info[00m
│   │           │   ├── entry_points.txt
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mpkg_resources[00m
│   │           │   ├── [01;34mextern[00m
│   │           │   │   ├── __init__.py
│   │           │   │   └── [01;34m__pycache__[00m
│   │           │   │       └── __init__.cpython-38.pyc
│   │           │   ├── __init__.py
│   │           │   ├── py31compat.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   └── py31compat.cpython-38.pyc
│   │           │   └── [01;34m_vendor[00m
│   │           │       ├── appdirs.py
│   │           │       ├── __init__.py
│   │           │       ├── [01;34mpackaging[00m
│   │           │       │   ├── __about__.py
│   │           │       │   ├── _compat.py
│   │           │       │   ├── __init__.py
│   │           │       │   ├── markers.py
│   │           │       │   ├── [01;34m__pycache__[00m
│   │           │       │   │   ├── __about__.cpython-38.pyc
│   │           │       │   │   ├── _compat.cpython-38.pyc
│   │           │       │   │   ├── __init__.cpython-38.pyc
│   │           │       │   │   ├── markers.cpython-38.pyc
│   │           │       │   │   ├── requirements.cpython-38.pyc
│   │           │       │   │   ├── specifiers.cpython-38.pyc
│   │           │       │   │   ├── _structures.cpython-38.pyc
│   │           │       │   │   ├── utils.cpython-38.pyc
│   │           │       │   │   └── version.cpython-38.pyc
│   │           │       │   ├── requirements.py
│   │           │       │   ├── specifiers.py
│   │           │       │   ├── _structures.py
│   │           │       │   ├── utils.py
│   │           │       │   └── version.py
│   │           │       ├── [01;34m__pycache__[00m
│   │           │       │   ├── appdirs.cpython-38.pyc
│   │           │       │   ├── __init__.cpython-38.pyc
│   │           │       │   ├── pyparsing.cpython-38.pyc
│   │           │       │   └── six.cpython-38.pyc
│   │           │       ├── pyparsing.py
│   │           │       └── six.py
│   │           ├── [01;34mpkg_resources-0.0.0.dist-info[00m
│   │           │   ├── AUTHORS.txt
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   └── WHEEL
│   │           ├── [01;34m__pycache__[00m
│   │           │   └── easy_install.cpython-38.pyc
│   │           ├── [01;34msetuptools[00m
│   │           │   ├── archive_util.py
│   │           │   ├── build_meta.py
│   │           │   ├── cli-32.exe
│   │           │   ├── cli-64.exe
│   │           │   ├── cli.exe
│   │           │   ├── [01;34mcommand[00m
│   │           │   │   ├── alias.py
│   │           │   │   ├── bdist_egg.py
│   │           │   │   ├── bdist_rpm.py
│   │           │   │   ├── bdist_wininst.py
│   │           │   │   ├── build_clib.py
│   │           │   │   ├── build_ext.py
│   │           │   │   ├── build_py.py
│   │           │   │   ├── develop.py
│   │           │   │   ├── dist_info.py
│   │           │   │   ├── easy_install.py
│   │           │   │   ├── egg_info.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── install_egg_info.py
│   │           │   │   ├── install_lib.py
│   │           │   │   ├── install.py
│   │           │   │   ├── install_scripts.py
│   │           │   │   ├── launcher manifest.xml
│   │           │   │   ├── py36compat.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── alias.cpython-38.pyc
│   │           │   │   │   ├── bdist_egg.cpython-38.pyc
│   │           │   │   │   ├── bdist_rpm.cpython-38.pyc
│   │           │   │   │   ├── bdist_wininst.cpython-38.pyc
│   │           │   │   │   ├── build_clib.cpython-38.pyc
│   │           │   │   │   ├── build_ext.cpython-38.pyc
│   │           │   │   │   ├── build_py.cpython-38.pyc
│   │           │   │   │   ├── develop.cpython-38.pyc
│   │           │   │   │   ├── dist_info.cpython-38.pyc
│   │           │   │   │   ├── easy_install.cpython-38.pyc
│   │           │   │   │   ├── egg_info.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── install.cpython-38.pyc
│   │           │   │   │   ├── install_egg_info.cpython-38.pyc
│   │           │   │   │   ├── install_lib.cpython-38.pyc
│   │           │   │   │   ├── install_scripts.cpython-38.pyc
│   │           │   │   │   ├── py36compat.cpython-38.pyc
│   │           │   │   │   ├── register.cpython-38.pyc
│   │           │   │   │   ├── rotate.cpython-38.pyc
│   │           │   │   │   ├── saveopts.cpython-38.pyc
│   │           │   │   │   ├── sdist.cpython-38.pyc
│   │           │   │   │   ├── setopt.cpython-38.pyc
│   │           │   │   │   ├── test.cpython-38.pyc
│   │           │   │   │   ├── upload.cpython-38.pyc
│   │           │   │   │   └── upload_docs.cpython-38.pyc
│   │           │   │   ├── register.py
│   │           │   │   ├── rotate.py
│   │           │   │   ├── saveopts.py
│   │           │   │   ├── sdist.py
│   │           │   │   ├── setopt.py
│   │           │   │   ├── test.py
│   │           │   │   ├── upload_docs.py
│   │           │   │   └── upload.py
│   │           │   ├── config.py
│   │           │   ├── depends.py
│   │           │   ├── _deprecation_warning.py
│   │           │   ├── dep_util.py
│   │           │   ├── dist.py
│   │           │   ├── errors.py
│   │           │   ├── extension.py
│   │           │   ├── [01;34mextern[00m
│   │           │   │   ├── __init__.py
│   │           │   │   └── [01;34m__pycache__[00m
│   │           │   │       └── __init__.cpython-38.pyc
│   │           │   ├── glob.py
│   │           │   ├── gui-32.exe
│   │           │   ├── gui-64.exe
│   │           │   ├── gui.exe
│   │           │   ├── _imp.py
│   │           │   ├── __init__.py
│   │           │   ├── installer.py
│   │           │   ├── launch.py
│   │           │   ├── lib2to3_ex.py
│   │           │   ├── monkey.py
│   │           │   ├── msvc.py
│   │           │   ├── namespaces.py
│   │           │   ├── package_index.py
│   │           │   ├── py27compat.py
│   │           │   ├── py31compat.py
│   │           │   ├── py33compat.py
│   │           │   ├── py34compat.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── archive_util.cpython-38.pyc
│   │           │   │   ├── build_meta.cpython-38.pyc
│   │           │   │   ├── config.cpython-38.pyc
│   │           │   │   ├── depends.cpython-38.pyc
│   │           │   │   ├── _deprecation_warning.cpython-38.pyc
│   │           │   │   ├── dep_util.cpython-38.pyc
│   │           │   │   ├── dist.cpython-38.pyc
│   │           │   │   ├── errors.cpython-38.pyc
│   │           │   │   ├── extension.cpython-38.pyc
│   │           │   │   ├── glob.cpython-38.pyc
│   │           │   │   ├── _imp.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── installer.cpython-38.pyc
│   │           │   │   ├── launch.cpython-38.pyc
│   │           │   │   ├── lib2to3_ex.cpython-38.pyc
│   │           │   │   ├── monkey.cpython-38.pyc
│   │           │   │   ├── msvc.cpython-38.pyc
│   │           │   │   ├── namespaces.cpython-38.pyc
│   │           │   │   ├── package_index.cpython-38.pyc
│   │           │   │   ├── py27compat.cpython-38.pyc
│   │           │   │   ├── py31compat.cpython-38.pyc
│   │           │   │   ├── py33compat.cpython-38.pyc
│   │           │   │   ├── py34compat.cpython-38.pyc
│   │           │   │   ├── sandbox.cpython-38.pyc
│   │           │   │   ├── site-patch.cpython-38.pyc
│   │           │   │   ├── ssl_support.cpython-38.pyc
│   │           │   │   ├── unicode_utils.cpython-38.pyc
│   │           │   │   ├── version.cpython-38.pyc
│   │           │   │   ├── wheel.cpython-38.pyc
│   │           │   │   └── windows_support.cpython-38.pyc
│   │           │   ├── sandbox.py
│   │           │   ├── script (dev).tmpl
│   │           │   ├── script.tmpl
│   │           │   ├── site-patch.py
│   │           │   ├── ssl_support.py
│   │           │   ├── unicode_utils.py
│   │           │   ├── [01;34m_vendor[00m
│   │           │   │   ├── __init__.py
│   │           │   │   ├── ordered_set.py
│   │           │   │   ├── [01;34mpackaging[00m
│   │           │   │   │   ├── __about__.py
│   │           │   │   │   ├── _compat.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── markers.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── __about__.cpython-38.pyc
│   │           │   │   │   │   ├── _compat.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── markers.cpython-38.pyc
│   │           │   │   │   │   ├── requirements.cpython-38.pyc
│   │           │   │   │   │   ├── specifiers.cpython-38.pyc
│   │           │   │   │   │   ├── _structures.cpython-38.pyc
│   │           │   │   │   │   ├── tags.cpython-38.pyc
│   │           │   │   │   │   ├── utils.cpython-38.pyc
│   │           │   │   │   │   └── version.cpython-38.pyc
│   │           │   │   │   ├── requirements.py
│   │           │   │   │   ├── specifiers.py
│   │           │   │   │   ├── _structures.py
│   │           │   │   │   ├── tags.py
│   │           │   │   │   ├── utils.py
│   │           │   │   │   └── version.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── ordered_set.cpython-38.pyc
│   │           │   │   │   ├── pyparsing.cpython-38.pyc
│   │           │   │   │   └── six.cpython-38.pyc
│   │           │   │   ├── pyparsing.py
│   │           │   │   └── six.py
│   │           │   ├── version.py
│   │           │   ├── wheel.py
│   │           │   └── windows_support.py
│   │           ├── [01;34msetuptools-44.0.0.dist-info[00m
│   │           │   ├── AUTHORS.txt
│   │           │   ├── dependency_links.txt
│   │           │   ├── entry_points.txt
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   ├── WHEEL
│   │           │   └── zip-safe
│   │           ├── [01;34msqlalchemy[00m
│   │           │   ├── [01;32mcimmutabledict.cpython-38-x86_64-linux-gnu.so[00m
│   │           │   ├── [01;34mconnectors[00m
│   │           │   │   ├── __init__.py
│   │           │   │   ├── mxodbc.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── mxodbc.cpython-38.pyc
│   │           │   │   │   └── pyodbc.cpython-38.pyc
│   │           │   │   └── pyodbc.py
│   │           │   ├── [01;32mcprocessors.cpython-38-x86_64-linux-gnu.so[00m
│   │           │   ├── [01;32mcresultproxy.cpython-38-x86_64-linux-gnu.so[00m
│   │           │   ├── [01;34mdatabases[00m
│   │           │   │   ├── __init__.py
│   │           │   │   └── [01;34m__pycache__[00m
│   │           │   │       └── __init__.cpython-38.pyc
│   │           │   ├── [01;34mdialects[00m
│   │           │   │   ├── [01;34mfirebird[00m
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── fdb.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── kinterbasdb.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       ├── base.cpython-38.pyc
│   │           │   │   │       ├── fdb.cpython-38.pyc
│   │           │   │   │       ├── __init__.cpython-38.pyc
│   │           │   │   │       └── kinterbasdb.cpython-38.pyc
│   │           │   │   ├── __init__.py
│   │           │   │   ├── [01;34mmssql[00m
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── information_schema.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── json.py
│   │           │   │   │   ├── mxodbc.py
│   │           │   │   │   ├── provision.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── information_schema.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── json.cpython-38.pyc
│   │           │   │   │   │   ├── mxodbc.cpython-38.pyc
│   │           │   │   │   │   ├── provision.cpython-38.pyc
│   │           │   │   │   │   ├── pymssql.cpython-38.pyc
│   │           │   │   │   │   └── pyodbc.cpython-38.pyc
│   │           │   │   │   ├── pymssql.py
│   │           │   │   │   └── pyodbc.py
│   │           │   │   ├── [01;34mmysql[00m
│   │           │   │   │   ├── aiomysql.py
│   │           │   │   │   ├── asyncmy.py
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── cymysql.py
│   │           │   │   │   ├── dml.py
│   │           │   │   │   ├── enumerated.py
│   │           │   │   │   ├── expression.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── json.py
│   │           │   │   │   ├── mariadbconnector.py
│   │           │   │   │   ├── mariadb.py
│   │           │   │   │   ├── mysqlconnector.py
│   │           │   │   │   ├── mysqldb.py
│   │           │   │   │   ├── oursql.py
│   │           │   │   │   ├── provision.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── aiomysql.cpython-38.pyc
│   │           │   │   │   │   ├── asyncmy.cpython-38.pyc
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── cymysql.cpython-38.pyc
│   │           │   │   │   │   ├── dml.cpython-38.pyc
│   │           │   │   │   │   ├── enumerated.cpython-38.pyc
│   │           │   │   │   │   ├── expression.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── json.cpython-38.pyc
│   │           │   │   │   │   ├── mariadbconnector.cpython-38.pyc
│   │           │   │   │   │   ├── mariadb.cpython-38.pyc
│   │           │   │   │   │   ├── mysqlconnector.cpython-38.pyc
│   │           │   │   │   │   ├── mysqldb.cpython-38.pyc
│   │           │   │   │   │   ├── oursql.cpython-38.pyc
│   │           │   │   │   │   ├── provision.cpython-38.pyc
│   │           │   │   │   │   ├── pymysql.cpython-38.pyc
│   │           │   │   │   │   ├── pyodbc.cpython-38.pyc
│   │           │   │   │   │   ├── reflection.cpython-38.pyc
│   │           │   │   │   │   ├── reserved_words.cpython-38.pyc
│   │           │   │   │   │   └── types.cpython-38.pyc
│   │           │   │   │   ├── pymysql.py
│   │           │   │   │   ├── pyodbc.py
│   │           │   │   │   ├── reflection.py
│   │           │   │   │   ├── reserved_words.py
│   │           │   │   │   └── types.py
│   │           │   │   ├── [01;34moracle[00m
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── cx_oracle.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── provision.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       ├── base.cpython-38.pyc
│   │           │   │   │       ├── cx_oracle.cpython-38.pyc
│   │           │   │   │       ├── __init__.cpython-38.pyc
│   │           │   │   │       └── provision.cpython-38.pyc
│   │           │   │   ├── [01;34mpostgresql[00m
│   │           │   │   │   ├── array.py
│   │           │   │   │   ├── asyncpg.py
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── dml.py
│   │           │   │   │   ├── ext.py
│   │           │   │   │   ├── hstore.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── json.py
│   │           │   │   │   ├── pg8000.py
│   │           │   │   │   ├── provision.py
│   │           │   │   │   ├── psycopg2cffi.py
│   │           │   │   │   ├── psycopg2.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── array.cpython-38.pyc
│   │           │   │   │   │   ├── asyncpg.cpython-38.pyc
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── dml.cpython-38.pyc
│   │           │   │   │   │   ├── ext.cpython-38.pyc
│   │           │   │   │   │   ├── hstore.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── json.cpython-38.pyc
│   │           │   │   │   │   ├── pg8000.cpython-38.pyc
│   │           │   │   │   │   ├── provision.cpython-38.pyc
│   │           │   │   │   │   ├── psycopg2cffi.cpython-38.pyc
│   │           │   │   │   │   ├── psycopg2.cpython-38.pyc
│   │           │   │   │   │   ├── pygresql.cpython-38.pyc
│   │           │   │   │   │   ├── pypostgresql.cpython-38.pyc
│   │           │   │   │   │   └── ranges.cpython-38.pyc
│   │           │   │   │   ├── pygresql.py
│   │           │   │   │   ├── pypostgresql.py
│   │           │   │   │   └── ranges.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   └── __init__.cpython-38.pyc
│   │           │   │   ├── [01;34msqlite[00m
│   │           │   │   │   ├── aiosqlite.py
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── dml.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── json.py
│   │           │   │   │   ├── provision.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── aiosqlite.cpython-38.pyc
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── dml.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── json.cpython-38.pyc
│   │           │   │   │   │   ├── provision.cpython-38.pyc
│   │           │   │   │   │   ├── pysqlcipher.cpython-38.pyc
│   │           │   │   │   │   └── pysqlite.cpython-38.pyc
│   │           │   │   │   ├── pysqlcipher.py
│   │           │   │   │   └── pysqlite.py
│   │           │   │   └── [01;34msybase[00m
│   │           │   │       ├── base.py
│   │           │   │       ├── __init__.py
│   │           │   │       ├── mxodbc.py
│   │           │   │       ├── [01;34m__pycache__[00m
│   │           │   │       │   ├── base.cpython-38.pyc
│   │           │   │       │   ├── __init__.cpython-38.pyc
│   │           │   │       │   ├── mxodbc.cpython-38.pyc
│   │           │   │       │   ├── pyodbc.cpython-38.pyc
│   │           │   │       │   └── pysybase.cpython-38.pyc
│   │           │   │       ├── pyodbc.py
│   │           │   │       └── pysybase.py
│   │           │   ├── [01;34mengine[00m
│   │           │   │   ├── base.py
│   │           │   │   ├── characteristics.py
│   │           │   │   ├── create.py
│   │           │   │   ├── cursor.py
│   │           │   │   ├── default.py
│   │           │   │   ├── events.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── interfaces.py
│   │           │   │   ├── mock.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   ├── characteristics.cpython-38.pyc
│   │           │   │   │   ├── create.cpython-38.pyc
│   │           │   │   │   ├── cursor.cpython-38.pyc
│   │           │   │   │   ├── default.cpython-38.pyc
│   │           │   │   │   ├── events.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── interfaces.cpython-38.pyc
│   │           │   │   │   ├── mock.cpython-38.pyc
│   │           │   │   │   ├── reflection.cpython-38.pyc
│   │           │   │   │   ├── result.cpython-38.pyc
│   │           │   │   │   ├── row.cpython-38.pyc
│   │           │   │   │   ├── strategies.cpython-38.pyc
│   │           │   │   │   ├── url.cpython-38.pyc
│   │           │   │   │   └── util.cpython-38.pyc
│   │           │   │   ├── reflection.py
│   │           │   │   ├── result.py
│   │           │   │   ├── row.py
│   │           │   │   ├── strategies.py
│   │           │   │   ├── url.py
│   │           │   │   └── util.py
│   │           │   ├── [01;34mevent[00m
│   │           │   │   ├── api.py
│   │           │   │   ├── attr.py
│   │           │   │   ├── base.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── legacy.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── api.cpython-38.pyc
│   │           │   │   │   ├── attr.cpython-38.pyc
│   │           │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── legacy.cpython-38.pyc
│   │           │   │   │   └── registry.cpython-38.pyc
│   │           │   │   └── registry.py
│   │           │   ├── events.py
│   │           │   ├── exc.py
│   │           │   ├── [01;34mext[00m
│   │           │   │   ├── associationproxy.py
│   │           │   │   ├── [01;34masyncio[00m
│   │           │   │   │   ├── base.py
│   │           │   │   │   ├── engine.py
│   │           │   │   │   ├── events.py
│   │           │   │   │   ├── exc.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   │   ├── engine.cpython-38.pyc
│   │           │   │   │   │   ├── events.cpython-38.pyc
│   │           │   │   │   │   ├── exc.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── result.cpython-38.pyc
│   │           │   │   │   │   ├── scoping.cpython-38.pyc
│   │           │   │   │   │   └── session.cpython-38.pyc
│   │           │   │   │   ├── result.py
│   │           │   │   │   ├── scoping.py
│   │           │   │   │   └── session.py
│   │           │   │   ├── automap.py
│   │           │   │   ├── baked.py
│   │           │   │   ├── compiler.py
│   │           │   │   ├── [01;34mdeclarative[00m
│   │           │   │   │   ├── extensions.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       ├── extensions.cpython-38.pyc
│   │           │   │   │       └── __init__.cpython-38.pyc
│   │           │   │   ├── horizontal_shard.py
│   │           │   │   ├── hybrid.py
│   │           │   │   ├── indexable.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── instrumentation.py
│   │           │   │   ├── mutable.py
│   │           │   │   ├── [01;34mmypy[00m
│   │           │   │   │   ├── apply.py
│   │           │   │   │   ├── decl_class.py
│   │           │   │   │   ├── infer.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── names.py
│   │           │   │   │   ├── plugin.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── apply.cpython-38.pyc
│   │           │   │   │   │   ├── decl_class.cpython-38.pyc
│   │           │   │   │   │   ├── infer.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── names.cpython-38.pyc
│   │           │   │   │   │   ├── plugin.cpython-38.pyc
│   │           │   │   │   │   └── util.cpython-38.pyc
│   │           │   │   │   └── util.py
│   │           │   │   ├── orderinglist.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── associationproxy.cpython-38.pyc
│   │           │   │   │   ├── automap.cpython-38.pyc
│   │           │   │   │   ├── baked.cpython-38.pyc
│   │           │   │   │   ├── compiler.cpython-38.pyc
│   │           │   │   │   ├── horizontal_shard.cpython-38.pyc
│   │           │   │   │   ├── hybrid.cpython-38.pyc
│   │           │   │   │   ├── indexable.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── instrumentation.cpython-38.pyc
│   │           │   │   │   ├── mutable.cpython-38.pyc
│   │           │   │   │   ├── orderinglist.cpython-38.pyc
│   │           │   │   │   └── serializer.cpython-38.pyc
│   │           │   │   └── serializer.py
│   │           │   ├── [01;34mfuture[00m
│   │           │   │   ├── engine.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── [01;34morm[00m
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── [01;34m__pycache__[00m
│   │           │   │   │       └── __init__.cpython-38.pyc
│   │           │   │   └── [01;34m__pycache__[00m
│   │           │   │       ├── engine.cpython-38.pyc
│   │           │   │       └── __init__.cpython-38.pyc
│   │           │   ├── __init__.py
│   │           │   ├── inspection.py
│   │           │   ├── log.py
│   │           │   ├── [01;34morm[00m
│   │           │   │   ├── attributes.py
│   │           │   │   ├── base.py
│   │           │   │   ├── clsregistry.py
│   │           │   │   ├── collections.py
│   │           │   │   ├── context.py
│   │           │   │   ├── decl_api.py
│   │           │   │   ├── decl_base.py
│   │           │   │   ├── dependency.py
│   │           │   │   ├── descriptor_props.py
│   │           │   │   ├── dynamic.py
│   │           │   │   ├── evaluator.py
│   │           │   │   ├── events.py
│   │           │   │   ├── exc.py
│   │           │   │   ├── identity.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── instrumentation.py
│   │           │   │   ├── interfaces.py
│   │           │   │   ├── loading.py
│   │           │   │   ├── mapper.py
│   │           │   │   ├── path_registry.py
│   │           │   │   ├── persistence.py
│   │           │   │   ├── properties.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── attributes.cpython-38.pyc
│   │           │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   ├── clsregistry.cpython-38.pyc
│   │           │   │   │   ├── collections.cpython-38.pyc
│   │           │   │   │   ├── context.cpython-38.pyc
│   │           │   │   │   ├── decl_api.cpython-38.pyc
│   │           │   │   │   ├── decl_base.cpython-38.pyc
│   │           │   │   │   ├── dependency.cpython-38.pyc
│   │           │   │   │   ├── descriptor_props.cpython-38.pyc
│   │           │   │   │   ├── dynamic.cpython-38.pyc
│   │           │   │   │   ├── evaluator.cpython-38.pyc
│   │           │   │   │   ├── events.cpython-38.pyc
│   │           │   │   │   ├── exc.cpython-38.pyc
│   │           │   │   │   ├── identity.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── instrumentation.cpython-38.pyc
│   │           │   │   │   ├── interfaces.cpython-38.pyc
│   │           │   │   │   ├── loading.cpython-38.pyc
│   │           │   │   │   ├── mapper.cpython-38.pyc
│   │           │   │   │   ├── path_registry.cpython-38.pyc
│   │           │   │   │   ├── persistence.cpython-38.pyc
│   │           │   │   │   ├── properties.cpython-38.pyc
│   │           │   │   │   ├── query.cpython-38.pyc
│   │           │   │   │   ├── relationships.cpython-38.pyc
│   │           │   │   │   ├── scoping.cpython-38.pyc
│   │           │   │   │   ├── session.cpython-38.pyc
│   │           │   │   │   ├── state.cpython-38.pyc
│   │           │   │   │   ├── strategies.cpython-38.pyc
│   │           │   │   │   ├── strategy_options.cpython-38.pyc
│   │           │   │   │   ├── sync.cpython-38.pyc
│   │           │   │   │   ├── unitofwork.cpython-38.pyc
│   │           │   │   │   └── util.cpython-38.pyc
│   │           │   │   ├── query.py
│   │           │   │   ├── relationships.py
│   │           │   │   ├── scoping.py
│   │           │   │   ├── session.py
│   │           │   │   ├── state.py
│   │           │   │   ├── strategies.py
│   │           │   │   ├── strategy_options.py
│   │           │   │   ├── sync.py
│   │           │   │   ├── unitofwork.py
│   │           │   │   └── util.py
│   │           │   ├── [01;34mpool[00m
│   │           │   │   ├── base.py
│   │           │   │   ├── dbapi_proxy.py
│   │           │   │   ├── events.py
│   │           │   │   ├── impl.py
│   │           │   │   ├── __init__.py
│   │           │   │   └── [01;34m__pycache__[00m
│   │           │   │       ├── base.cpython-38.pyc
│   │           │   │       ├── dbapi_proxy.cpython-38.pyc
│   │           │   │       ├── events.cpython-38.pyc
│   │           │   │       ├── impl.cpython-38.pyc
│   │           │   │       └── __init__.cpython-38.pyc
│   │           │   ├── processors.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── events.cpython-38.pyc
│   │           │   │   ├── exc.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── inspection.cpython-38.pyc
│   │           │   │   ├── log.cpython-38.pyc
│   │           │   │   ├── processors.cpython-38.pyc
│   │           │   │   ├── schema.cpython-38.pyc
│   │           │   │   └── types.cpython-38.pyc
│   │           │   ├── schema.py
│   │           │   ├── [01;34msql[00m
│   │           │   │   ├── annotation.py
│   │           │   │   ├── base.py
│   │           │   │   ├── coercions.py
│   │           │   │   ├── compiler.py
│   │           │   │   ├── crud.py
│   │           │   │   ├── ddl.py
│   │           │   │   ├── default_comparator.py
│   │           │   │   ├── dml.py
│   │           │   │   ├── elements.py
│   │           │   │   ├── events.py
│   │           │   │   ├── expression.py
│   │           │   │   ├── functions.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── lambdas.py
│   │           │   │   ├── naming.py
│   │           │   │   ├── operators.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── annotation.cpython-38.pyc
│   │           │   │   │   ├── base.cpython-38.pyc
│   │           │   │   │   ├── coercions.cpython-38.pyc
│   │           │   │   │   ├── compiler.cpython-38.pyc
│   │           │   │   │   ├── crud.cpython-38.pyc
│   │           │   │   │   ├── ddl.cpython-38.pyc
│   │           │   │   │   ├── default_comparator.cpython-38.pyc
│   │           │   │   │   ├── dml.cpython-38.pyc
│   │           │   │   │   ├── elements.cpython-38.pyc
│   │           │   │   │   ├── events.cpython-38.pyc
│   │           │   │   │   ├── expression.cpython-38.pyc
│   │           │   │   │   ├── functions.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── lambdas.cpython-38.pyc
│   │           │   │   │   ├── naming.cpython-38.pyc
│   │           │   │   │   ├── operators.cpython-38.pyc
│   │           │   │   │   ├── roles.cpython-38.pyc
│   │           │   │   │   ├── schema.cpython-38.pyc
│   │           │   │   │   ├── selectable.cpython-38.pyc
│   │           │   │   │   ├── sqltypes.cpython-38.pyc
│   │           │   │   │   ├── traversals.cpython-38.pyc
│   │           │   │   │   ├── type_api.cpython-38.pyc
│   │           │   │   │   ├── util.cpython-38.pyc
│   │           │   │   │   └── visitors.cpython-38.pyc
│   │           │   │   ├── roles.py
│   │           │   │   ├── schema.py
│   │           │   │   ├── selectable.py
│   │           │   │   ├── sqltypes.py
│   │           │   │   ├── traversals.py
│   │           │   │   ├── type_api.py
│   │           │   │   ├── util.py
│   │           │   │   └── visitors.py
│   │           │   ├── [01;34mtesting[00m
│   │           │   │   ├── assertions.py
│   │           │   │   ├── assertsql.py
│   │           │   │   ├── asyncio.py
│   │           │   │   ├── config.py
│   │           │   │   ├── engines.py
│   │           │   │   ├── entities.py
│   │           │   │   ├── exclusions.py
│   │           │   │   ├── fixtures.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── mock.py
│   │           │   │   ├── pickleable.py
│   │           │   │   ├── [01;34mplugin[00m
│   │           │   │   │   ├── bootstrap.py
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── plugin_base.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── bootstrap.cpython-38.pyc
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── plugin_base.cpython-38.pyc
│   │           │   │   │   │   ├── pytestplugin.cpython-38.pyc
│   │           │   │   │   │   └── reinvent_fixtures_py2k.cpython-38.pyc
│   │           │   │   │   ├── pytestplugin.py
│   │           │   │   │   └── reinvent_fixtures_py2k.py
│   │           │   │   ├── profiling.py
│   │           │   │   ├── provision.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── assertions.cpython-38.pyc
│   │           │   │   │   ├── assertsql.cpython-38.pyc
│   │           │   │   │   ├── asyncio.cpython-38.pyc
│   │           │   │   │   ├── config.cpython-38.pyc
│   │           │   │   │   ├── engines.cpython-38.pyc
│   │           │   │   │   ├── entities.cpython-38.pyc
│   │           │   │   │   ├── exclusions.cpython-38.pyc
│   │           │   │   │   ├── fixtures.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── mock.cpython-38.pyc
│   │           │   │   │   ├── pickleable.cpython-38.pyc
│   │           │   │   │   ├── profiling.cpython-38.pyc
│   │           │   │   │   ├── provision.cpython-38.pyc
│   │           │   │   │   ├── requirements.cpython-38.pyc
│   │           │   │   │   ├── schema.cpython-38.pyc
│   │           │   │   │   ├── util.cpython-38.pyc
│   │           │   │   │   └── warnings.cpython-38.pyc
│   │           │   │   ├── requirements.py
│   │           │   │   ├── schema.py
│   │           │   │   ├── [01;34msuite[00m
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   │   ├── test_cte.cpython-38.pyc
│   │           │   │   │   │   ├── test_ddl.cpython-38.pyc
│   │           │   │   │   │   ├── test_deprecations.cpython-38.pyc
│   │           │   │   │   │   ├── test_dialect.cpython-38.pyc
│   │           │   │   │   │   ├── test_insert.cpython-38.pyc
│   │           │   │   │   │   ├── test_reflection.cpython-38.pyc
│   │           │   │   │   │   ├── test_results.cpython-38.pyc
│   │           │   │   │   │   ├── test_rowcount.cpython-38.pyc
│   │           │   │   │   │   ├── test_select.cpython-38.pyc
│   │           │   │   │   │   ├── test_sequence.cpython-38.pyc
│   │           │   │   │   │   ├── test_types.cpython-38.pyc
│   │           │   │   │   │   ├── test_unicode_ddl.cpython-38.pyc
│   │           │   │   │   │   └── test_update_delete.cpython-38.pyc
│   │           │   │   │   ├── test_cte.py
│   │           │   │   │   ├── test_ddl.py
│   │           │   │   │   ├── test_deprecations.py
│   │           │   │   │   ├── test_dialect.py
│   │           │   │   │   ├── test_insert.py
│   │           │   │   │   ├── test_reflection.py
│   │           │   │   │   ├── test_results.py
│   │           │   │   │   ├── test_rowcount.py
│   │           │   │   │   ├── test_select.py
│   │           │   │   │   ├── test_sequence.py
│   │           │   │   │   ├── test_types.py
│   │           │   │   │   ├── test_unicode_ddl.py
│   │           │   │   │   └── test_update_delete.py
│   │           │   │   ├── util.py
│   │           │   │   └── warnings.py
│   │           │   ├── types.py
│   │           │   └── [01;34mutil[00m
│   │           │       ├── _collections.py
│   │           │       ├── compat.py
│   │           │       ├── _compat_py3k.py
│   │           │       ├── concurrency.py
│   │           │       ├── _concurrency_py3k.py
│   │           │       ├── deprecations.py
│   │           │       ├── __init__.py
│   │           │       ├── langhelpers.py
│   │           │       ├── _preloaded.py
│   │           │       ├── [01;34m__pycache__[00m
│   │           │       │   ├── _collections.cpython-38.pyc
│   │           │       │   ├── compat.cpython-38.pyc
│   │           │       │   ├── _compat_py3k.cpython-38.pyc
│   │           │       │   ├── concurrency.cpython-38.pyc
│   │           │       │   ├── _concurrency_py3k.cpython-38.pyc
│   │           │       │   ├── deprecations.cpython-38.pyc
│   │           │       │   ├── __init__.cpython-38.pyc
│   │           │       │   ├── langhelpers.cpython-38.pyc
│   │           │       │   ├── _preloaded.cpython-38.pyc
│   │           │       │   ├── queue.cpython-38.pyc
│   │           │       │   └── topological.cpython-38.pyc
│   │           │       ├── queue.py
│   │           │       └── topological.py
│   │           ├── [01;34mSQLAlchemy-1.4.29.dist-info[00m
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── top_level.txt
│   │           │   └── WHEEL
│   │           ├── [01;34mwerkzeug[00m
│   │           │   ├── datastructures.py
│   │           │   ├── datastructures.pyi
│   │           │   ├── [01;34mdebug[00m
│   │           │   │   ├── console.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── console.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── repr.cpython-38.pyc
│   │           │   │   │   └── tbtools.cpython-38.pyc
│   │           │   │   ├── repr.py
│   │           │   │   ├── [01;34mshared[00m
│   │           │   │   │   ├── [01;35mconsole.png[00m
│   │           │   │   │   ├── debugger.js
│   │           │   │   │   ├── FONT_LICENSE
│   │           │   │   │   ├── ICON_LICENSE.md
│   │           │   │   │   ├── [01;35mless.png[00m
│   │           │   │   │   ├── [01;35mmore.png[00m
│   │           │   │   │   ├── [01;35msource.png[00m
│   │           │   │   │   ├── style.css
│   │           │   │   │   └── ubuntu.ttf
│   │           │   │   └── tbtools.py
│   │           │   ├── exceptions.py
│   │           │   ├── filesystem.py
│   │           │   ├── formparser.py
│   │           │   ├── http.py
│   │           │   ├── __init__.py
│   │           │   ├── _internal.py
│   │           │   ├── local.py
│   │           │   ├── [01;34mmiddleware[00m
│   │           │   │   ├── dispatcher.py
│   │           │   │   ├── http_proxy.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── lint.py
│   │           │   │   ├── profiler.py
│   │           │   │   ├── proxy_fix.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── dispatcher.cpython-38.pyc
│   │           │   │   │   ├── http_proxy.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── lint.cpython-38.pyc
│   │           │   │   │   ├── profiler.cpython-38.pyc
│   │           │   │   │   ├── proxy_fix.cpython-38.pyc
│   │           │   │   │   └── shared_data.cpython-38.pyc
│   │           │   │   └── shared_data.py
│   │           │   ├── [01;34m__pycache__[00m
│   │           │   │   ├── datastructures.cpython-38.pyc
│   │           │   │   ├── exceptions.cpython-38.pyc
│   │           │   │   ├── filesystem.cpython-38.pyc
│   │           │   │   ├── formparser.cpython-38.pyc
│   │           │   │   ├── http.cpython-38.pyc
│   │           │   │   ├── __init__.cpython-38.pyc
│   │           │   │   ├── _internal.cpython-38.pyc
│   │           │   │   ├── local.cpython-38.pyc
│   │           │   │   ├── _reloader.cpython-38.pyc
│   │           │   │   ├── routing.cpython-38.pyc
│   │           │   │   ├── security.cpython-38.pyc
│   │           │   │   ├── serving.cpython-38.pyc
│   │           │   │   ├── testapp.cpython-38.pyc
│   │           │   │   ├── test.cpython-38.pyc
│   │           │   │   ├── urls.cpython-38.pyc
│   │           │   │   ├── user_agent.cpython-38.pyc
│   │           │   │   ├── useragents.cpython-38.pyc
│   │           │   │   ├── utils.cpython-38.pyc
│   │           │   │   └── wsgi.cpython-38.pyc
│   │           │   ├── py.typed
│   │           │   ├── _reloader.py
│   │           │   ├── routing.py
│   │           │   ├── [01;34msansio[00m
│   │           │   │   ├── __init__.py
│   │           │   │   ├── multipart.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── multipart.cpython-38.pyc
│   │           │   │   │   ├── request.cpython-38.pyc
│   │           │   │   │   ├── response.cpython-38.pyc
│   │           │   │   │   └── utils.cpython-38.pyc
│   │           │   │   ├── request.py
│   │           │   │   ├── response.py
│   │           │   │   └── utils.py
│   │           │   ├── security.py
│   │           │   ├── serving.py
│   │           │   ├── testapp.py
│   │           │   ├── test.py
│   │           │   ├── urls.py
│   │           │   ├── user_agent.py
│   │           │   ├── useragents.py
│   │           │   ├── utils.py
│   │           │   ├── [01;34mwrappers[00m
│   │           │   │   ├── accept.py
│   │           │   │   ├── auth.py
│   │           │   │   ├── base_request.py
│   │           │   │   ├── base_response.py
│   │           │   │   ├── common_descriptors.py
│   │           │   │   ├── cors.py
│   │           │   │   ├── etag.py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── json.py
│   │           │   │   ├── [01;34m__pycache__[00m
│   │           │   │   │   ├── accept.cpython-38.pyc
│   │           │   │   │   ├── auth.cpython-38.pyc
│   │           │   │   │   ├── base_request.cpython-38.pyc
│   │           │   │   │   ├── base_response.cpython-38.pyc
│   │           │   │   │   ├── common_descriptors.cpython-38.pyc
│   │           │   │   │   ├── cors.cpython-38.pyc
│   │           │   │   │   ├── etag.cpython-38.pyc
│   │           │   │   │   ├── __init__.cpython-38.pyc
│   │           │   │   │   ├── json.cpython-38.pyc
│   │           │   │   │   ├── request.cpython-38.pyc
│   │           │   │   │   ├── response.cpython-38.pyc
│   │           │   │   │   └── user_agent.cpython-38.pyc
│   │           │   │   ├── request.py
│   │           │   │   ├── response.py
│   │           │   │   └── user_agent.py
│   │           │   └── wsgi.py
│   │           └── [01;34mWerkzeug-2.0.2.dist-info[00m
│   │               ├── INSTALLER
│   │               ├── LICENSE.rst
│   │               ├── METADATA
│   │               ├── RECORD
│   │               ├── top_level.txt
│   │               └── WHEEL
│   ├── [01;36mlib64[00m -> [01;34mlib[00m
│   ├── pyvenv.cfg
│   └── [01;34mshare[00m
│       └── [01;34mpython-wheels[00m
│           ├── appdirs-1.4.3-py2.py3-none-any.whl
│           ├── CacheControl-0.12.6-py2.py3-none-any.whl
│           ├── certifi-2019.11.28-py2.py3-none-any.whl
│           ├── chardet-3.0.4-py2.py3-none-any.whl
│           ├── colorama-0.4.3-py2.py3-none-any.whl
│           ├── contextlib2-0.6.0-py2.py3-none-any.whl
│           ├── distlib-0.3.0-py2.py3-none-any.whl
│           ├── distro-1.4.0-py2.py3-none-any.whl
│           ├── html5lib-1.0.1-py2.py3-none-any.whl
│           ├── idna-2.8-py2.py3-none-any.whl
│           ├── ipaddr-2.2.0-py2.py3-none-any.whl
│           ├── lockfile-0.12.2-py2.py3-none-any.whl
│           ├── msgpack-0.6.2-py2.py3-none-any.whl
│           ├── packaging-20.3-py2.py3-none-any.whl
│           ├── pep517-0.8.2-py2.py3-none-any.whl
│           ├── pip-20.0.2-py2.py3-none-any.whl
│           ├── pkg_resources-0.0.0-py2.py3-none-any.whl
│           ├── progress-1.5-py2.py3-none-any.whl
│           ├── pyparsing-2.4.6-py2.py3-none-any.whl
│           ├── requests-2.22.0-py2.py3-none-any.whl
│           ├── retrying-1.3.3-py2.py3-none-any.whl
│           ├── setuptools-44.0.0-py2.py3-none-any.whl
│           ├── six-1.14.0-py2.py3-none-any.whl
│           ├── toml-0.10.0-py2.py3-none-any.whl
│           ├── urllib3-1.25.8-py2.py3-none-any.whl
│           ├── webencodings-0.5.1-py2.py3-none-any.whl
│           └── wheel-0.34.2-py2.py3-none-any.whl
├── [01;34messaiperso[00m
│   ├── essaiperso.py
│   └── [01;34mtemplates[00m
│       └── essaiperso.html
├── path.py
├── README.md
└── run.py

167 directories, 1394 files
