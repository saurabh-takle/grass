include(GNUInstallDirs)

if(WITH_FHS)
  message("FHS file structure")
  set(GISBASE_DIR "${CMAKE_INSTALL_LIBEXECDIR}/${PROJECT_NAME_LOWER}")
  set(GRASS_INSTALL_BINDIR "${GISBASE_DIR}/bin")
  set(GRASS_INSTALL_LIBDIR "${CMAKE_INSTALL_LIBDIR}")
  set(GRASS_INSTALL_SCRIPTDIR "${GISBASE_DIR}/bin")
  set(GRASS_INSTALL_SHAREDIR
      "${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME_LOWER}")
  set(GRASS_INSTALL_ETCDIR "${GRASS_INSTALL_SHAREDIR}/etc")
  set(GRASS_INSTALL_ETCBINDIR "${GISBASE_DIR}/etc")
  set(GRASS_INSTALL_PYDIR "${PYTHON_SITEARCH}")
  set(GRASS_INSTALL_GUIDIR "${GRASS_INSTALL_PYDIR}/${PROJECT_NAME_LOWER}/gui")
  set(GRASS_INSTALL_GUISCRIPTDIR "${GRASS_INSTALL_SCRIPTDIR}")
  set(GRASS_INSTALL_DRIVERDIR "${GISBASE_DIR}/driver")
  set(GRASS_INSTALL_FONTSDIR "${GRASS_INSTALL_SHAREDIR}/fonts")
  set(GRASS_INSTALL_UTILSDIR "${GISBASE_DIR}/utils")
  set(GRASS_INSTALL_INCLUDEDIR "${CMAKE_INSTALL_INCLUDEDIR}")
  set(GRASS_INSTALL_DOCDIR
      "${CMAKE_INSTALL_DATAROOTDIR}/doc/${PROJECT_NAME_LOWER}-doc")
  set(GRASS_INSTALL_DEVDOCDIR
      "${CMAKE_INSTALL_DATAROOTDIR}/doc/${PROJECT_NAME_LOWER}-dev-doc")
  set(GRASS_INSTALL_MANDIR "${CMAKE_INSTALL_MANDIR}")
  set(GRASS_INSTALL_MKDOCSDIR
      "${CMAKE_INSTALL_DATAROOTDIR}/doc/${PROJECT_NAME_LOWER}-mkdocs")
  set(GRASS_INSTALL_DEMODIR "${GRASS_INSTALL_SHAREDIR}/demolocation")
  set(GRASS_INSTALL_MISCDIR "${GRASS_INSTALL_SHAREDIR}")
  set(GRASS_INSTALL_MAKEFILEDIR "${GISBASE_DIR}/Make")
  set(GRASS_INSTALL_LOCALEDIR "${CMAKE_INSTALL_LOCALEDIR}")
else()
  message("Legacy file structure")
  set(GISBASE_DIR "${CMAKE_INSTALL_LIBDIR}/grass${GRASS_VERSION_MAJOR}${GRASS_VERSION_MINOR}")
  set(GRASS_INSTALL_BINDIR "${GISBASE_DIR}/bin")
  set(GRASS_INSTALL_LIBDIR "${GISBASE_DIR}/lib")
  set(GRASS_INSTALL_SCRIPTDIR "${GISBASE_DIR}/scripts")
  set(GRASS_INSTALL_SHAREDIR "${GISBASE_DIR}/share")
  set(GRASS_INSTALL_ETCDIR "${GISBASE_DIR}/etc")
  set(GRASS_INSTALL_ETCBINDIR "${GISBASE_DIR}/etc")
  set(GRASS_INSTALL_PYDIR "${GISBASE_DIR}/etc/python")
  set(GRASS_INSTALL_GUIDIR "${GISBASE_DIR}/gui")
  set(GRASS_INSTALL_GUISCRIPTDIR "${GRASS_INSTALL_GUIDIR}/scripts")
  set(GRASS_INSTALL_DRIVERDIR "${GISBASE_DIR}/driver")
  set(GRASS_INSTALL_FONTSDIR "${GISBASE_DIR}/fonts")
  set(GRASS_INSTALL_UTILSDIR "${GISBASE_DIR}/utils")
  set(GRASS_INSTALL_INCLUDEDIR "${GISBASE_DIR}/include")
  set(GRASS_INSTALL_DOCDIR "${GISBASE_DIR}/docs/html")
  set(GRASS_INSTALL_DEVDOCDIR "${GISBASE_DIR}/html")
  set(GRASS_INSTALL_MANDIR "${GISBASE_DIR}/docs/man")
  set(GRASS_INSTALL_MKDOCSDIR "${GISBASE_DIR}/docs/mkdocs")
  set(GRASS_INSTALL_DEMODIR "${GISBASE_DIR}/demolocation")
  set(GRASS_INSTALL_MISCDIR "${GISBASE_DIR}")
  set(GRASS_INSTALL_MAKEFILEDIR "${GISBASE_DIR}/Make")
  set(GRASS_INSTALL_LOCALEDIR "${GISBASE_DIR}/locale")
endif()

message(STATUS "GISBASE_DIR ${GISBASE_DIR}")
message(STATUS "GRASS_INSTALL_BINDIR ${GRASS_INSTALL_BINDIR}")
message(STATUS "GRASS_INSTALL_LIBDIR ${GRASS_INSTALL_LIBDIR}")
message(STATUS "GRASS_INSTALL_SCRIPTDIR ${GRASS_INSTALL_SCRIPTDIR}")
message(STATUS "GRASS_INSTALL_SHAREDIR ${GRASS_INSTALL_SHAREDIR}")
message(STATUS "GRASS_INSTALL_ETCDIR ${GRASS_INSTALL_ETCDIR}")
message(STATUS "GRASS_INSTALL_ETCBINDIR ${GRASS_INSTALL_ETCBINDIR}")
message(STATUS "GRASS_INSTALL_PYDIR ${GRASS_INSTALL_PYDIR}")
message(STATUS "GRASS_INSTALL_GUIDIR ${GRASS_INSTALL_GUIDIR}")
message(STATUS "GRASS_INSTALL_GUISCRIPTDIR ${GRASS_INSTALL_GUISCRIPTDIR}")
message(STATUS "GRASS_INSTALL_DRIVERDIR ${GRASS_INSTALL_DRIVERDIR}")
message(STATUS "GRASS_INSTALL_FONTSDIR ${GRASS_INSTALL_FONTSDIR}")
message(STATUS "GRASS_INSTALL_UTILSDIR ${GRASS_INSTALL_UTILSDIR}")
message(STATUS "GRASS_INSTALL_INCLUDEDIR ${GRASS_INSTALL_INCLUDEDIR}")
message(STATUS "GRASS_INSTALL_DOCDIR ${GRASS_INSTALL_DOCDIR}")
message(STATUS "GRASS_INSTALL_DEVDOCDIR ${GRASS_INSTALL_DEVDOCDIR}")
message(STATUS "GRASS_INSTALL_MANDIR ${GRASS_INSTALL_MANDIR}")
message(STATUS "GRASS_INSTALL_MKDOCSDIR ${GRASS_INSTALL_MKDOCSDIR}")
message(STATUS "GRASS_INSTALL_DEMODIR ${GRASS_INSTALL_DEMODIR}")
message(STATUS "GRASS_INSTALL_MISCDIR ${GRASS_INSTALL_MISCDIR}")
message(STATUS "GRASS_INSTALL_MAKEFILEDIR ${GRASS_INSTALL_MAKEFILEDIR}")
message(STATUS "GRASS_INSTALL_LOCALEDIR ${GRASS_INSTALL_LOCALEDIR}")

set(OUTDIR "${CMAKE_BINARY_DIR}/output")
set(GISBASE ${CMAKE_INSTALL_PREFIX}/${GISBASE_DIR})
set(RUNTIME_GISBASE "${OUTDIR}/${GISBASE_DIR}")
set(GISRC_NAME ".grassrc${GRASS_VERSION_MAJOR}${GRASS_VERSION_MINOR}")

if(WITH_FHS)
  file(TO_NATIVE_PATH "${GRASS_INSTALL_PYDIR}" GRASS_INSTALL_PYDIR_PATH)
  file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_PYDIR}" GRASS_INSTALL_PYDIR_RUNTIME_PATH)
else()
  file(TO_NATIVE_PATH "${CMAKE_INSTALL_PREFIX}/${GRASS_INSTALL_PYDIR}" GRASS_INSTALL_PYDIR_PATH)
  file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_PYDIR}" GRASS_INSTALL_PYDIR_RUNTIME_PATH)
endif()
message(STATUS "GRASS_INSTALL_PYDIR_PATH ${GRASS_INSTALL_PYDIR_PATH}")
message(STATUS "GRASS_INSTALL_PYDIR_RUNTIME_PATH ${GRASS_INSTALL_PYDIR_RUNTIME_PATH}")

file(TO_NATIVE_PATH "${CMAKE_SOURCE_DIR}" MODULE_TOPDIR)
file(TO_NATIVE_PATH "${RUNTIME_GISBASE}" RUN_GISBASE_NATIVE)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_BINDIR}" BIN_DIR)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_LIBDIR}" LIB_DIR)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_SCRIPTDIR}" SCRIPTS_DIR)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_DOCDIR}" DOC_DIR)

file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_DEMODIR}/${GISRC_NAME}" GISRC)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_PYDIR}" ETC_PYTHON_DIR)
file(TO_NATIVE_PATH "${OUTDIR}/${GRASS_INSTALL_GUIDIR}/wxpython"
     GUI_WXPYTHON_DIR)
message(STATUS "GISBASE ${GISBASE}")
message(STATUS "GISBASE_NATIVE ${RUN_GISBASE_NATIVE}")

message("Creating directories in ${GISBASE}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_BINDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_SCRIPTDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_SHAREDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_DEMODIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_DRIVERDIR}/db")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_UTILSDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_LIBDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_PYDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_ETCBINDIR}/lister")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_PYDIR}/grass/lib")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_GUIDIR}/wxpython/xml")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_GUIDIR}/icons")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_GUIDIR}/images")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_DOCDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_MANDIR}")
file(MAKE_DIRECTORY "${OUTDIR}/${GRASS_INSTALL_MKDOCSDIR}/source")
