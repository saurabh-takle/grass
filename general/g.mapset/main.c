/****************************************************************
 *
 * MODULE:       g.mapset
 *
 * AUTHOR(S):    Radim Blazek
 *               Joel Pitt, joel.pitt@gmail.com
 *
 * PURPOSE:      Change current mapset, optionally adding it
 *               if the mapset does not exist.
 *
 * COPYRIGHT:    (C) 2004, 2010-2011 by the GRASS Development Team
 *
 *               This program is free software under the
 *               GNU General Public License (>=v2).
 *               Read the file COPYING that comes with GRASS
 *               for details.
 *
 **************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <grass/gis.h>
#include <grass/glocale.h>
#include <grass/parson.h>
#include <grass/spawn.h>

enum OutputFormat { PLAIN, JSON };

// Function to serialize and print JSON value
static void serialize_and_print_json_object(JSON_Value *root_value)
{
    char *serialized_string = json_serialize_to_string_pretty(root_value);
    if (!serialized_string) {
        json_value_free(root_value);
        G_fatal_error(_("Failed to serialize JSON to pretty format."));
    }

    puts(serialized_string);
    json_free_serialized_string(serialized_string);
    json_value_free(root_value);
}

int main(int argc, char *argv[])
{
    int ret;
    struct GModule *module;
    struct {
        struct Option *gisdbase, *location, *mapset, *format;
    } opt;
    struct {
        struct Flag *add, *list, *curr;
    } flag;
    const char *gisdbase_old, *location_old, *mapset_old;
    const char *gisdbase_new, *location_new, *mapset_new;
    const char *gis_lock;
    char *mapset_old_path, *mapset_new_path;
    char *lock_prog;
    const char *shell;
    char path[GPATH_MAX];
    enum OutputFormat format;
    JSON_Object *root_object = NULL;
    JSON_Value *root_value = NULL;

    G_gisinit(argv[0]);

    module = G_define_module();
    G_add_keyword(_("general"));
    G_add_keyword(_("settings"));
    G_add_keyword(_("project"));
    module->label = _("Changes or reports current mapset.");
    module->description = _("Optionally, creates new mapset or lists available "
                            "mapsets in given project (location).");

    opt.mapset = G_define_standard_option(G_OPT_M_MAPSET);
    opt.mapset->required = YES;
    opt.mapset->description = _("Name of mapset where to switch");
    opt.mapset->guisection = _("Mapset");
    opt.mapset->gisprompt = "new,mapset,mapset";

    opt.location = G_define_standard_option(G_OPT_M_LOCATION);
    opt.location->guisection = _("Mapset");

    opt.gisdbase = G_define_standard_option(G_OPT_M_DBASE);
    opt.gisdbase->guisection = _("Mapset");

    opt.format = G_define_standard_option(G_OPT_F_FORMAT);
    opt.format->guisection = _("Print");

    flag.add = G_define_flag();
    flag.add->key = 'c';
    flag.add->description = _("Create mapset if it doesn't exist");
    flag.add->answer = FALSE;
    flag.add->guisection = _("Create");

    flag.list = G_define_flag();
    flag.list->key = 'l';
    flag.list->suppress_required = YES;
    flag.list->description = _("List available mapsets and exit");
    flag.list->guisection = _("Print");

    flag.curr = G_define_flag();
    flag.curr->key = 'p';
    flag.curr->suppress_required = YES;
    flag.curr->description = _("Print current mapset and exit");
    flag.curr->guisection = _("Print");

    if (G_parser(argc, argv))
        exit(EXIT_FAILURE);

    if (strcmp(opt.format->answer, "json") == 0) {
        format = JSON;

        root_value = json_value_init_object();
        if (root_value == NULL) {
            G_fatal_error(
                _("Failed to initialize JSON object. Out of memory?"));
        }
        root_object = json_object(root_value);
    }
    else {
        format = PLAIN;
    }

    /* Store original values */
    gisdbase_old = G_getenv_nofatal("GISDBASE");
    location_old = G_getenv_nofatal("LOCATION_NAME");
    mapset_old = G_getenv_nofatal("MAPSET");

    if (flag.curr->answer) {
        switch (format) {
        case PLAIN:
            fprintf(stdout, "%s\n", mapset_old);
            break;

        case JSON:
            json_object_set_string(root_object, "project", location_old);
            json_object_set_string(root_object, "mapset", mapset_old);
            serialize_and_print_json_object(root_value);
            break;
        }
        exit(EXIT_SUCCESS);
    }

    G_asprintf(&mapset_old_path, "%s/%s/%s", gisdbase_old, location_old,
               mapset_old);

    /* New values */
    if (opt.gisdbase->answer)
        gisdbase_new = opt.gisdbase->answer;
    else
        gisdbase_new = gisdbase_old;

    if (opt.location->answer)
        location_new = opt.location->answer;
    else
        location_new = location_old;

    if (flag.list->answer) {
        char **ms;
        int nmapsets;
        JSON_Array *mapsets_array = NULL;
        JSON_Value *mapsets_value = NULL;

        G_setenv_nogisrc("LOCATION_NAME", location_new);
        G_setenv_nogisrc("GISDBASE", gisdbase_new);

        ms = G_get_available_mapsets();
        if (format == JSON) {
            mapsets_value = json_value_init_array();
            if (mapsets_value == NULL) {
                G_fatal_error(
                    _("Failed to initialize JSON array. Out of memory?"));
            }
            mapsets_array = json_array(mapsets_value);

            json_object_set_string(root_object, "project", location_new);
        }

        for (nmapsets = 0; ms[nmapsets]; nmapsets++) {
            if (G_mapset_permissions(ms[nmapsets]) > 0) {
                switch (format) {
                case PLAIN:
                    fprintf(stdout, "%s ", ms[nmapsets]);
                    break;

                case JSON:
                    json_array_append_string(mapsets_array, ms[nmapsets]);
                    break;
                }
            }
        }
        switch (format) {
        case PLAIN:
            fprintf(stdout, "\n");
            break;

        case JSON:
            json_object_set_value(root_object, "mapsets", mapsets_value);
            serialize_and_print_json_object(root_value);
            break;
        }

        exit(EXIT_SUCCESS);
    }

    mapset_new = opt.mapset->answer;
    G_asprintf(&mapset_new_path, "%s/%s/%s", gisdbase_new, location_new,
               mapset_new);

    /* TODO: this should be checked better (repeated '/' etc.) */
    if (strcmp(mapset_old_path, mapset_new_path) == 0) {
        G_warning(_("<%s> is already the current mapset"), mapset_new);
        exit(EXIT_SUCCESS);
    }
    /* Check if the mapset exists and user is owner */
    G_debug(2, "check : %s", mapset_new_path);

    ret = G_mapset_permissions2(gisdbase_new, location_new, mapset_new);
    switch (ret) {
    case 0:
        G_fatal_error(_("You don't have permission to use the mapset <%s>"),
                      mapset_new);
        break;
    case -1:
        if (flag.add->answer == TRUE) {
            G_debug(2, "Mapset <%s> doesn't exist, attempting to create it",
                    mapset_new);
            if (G_make_mapset(gisdbase_new, location_new, mapset_new) != 0)
                G_fatal_error(_("Unable to create new mapset <%s>"),
                              mapset_new);
        }
        else
            G_fatal_error(
                _("Mapset <%s> does not exist. Use -c flag to create it."),
                mapset_new);
        break;
    default:
        break;
    }

    /* Check if the mapset is in use */
    gis_lock = getenv("GIS_LOCK");
    if (!gis_lock)
        G_fatal_error(_("Unable to read GIS_LOCK environment variable"));

    G_asprintf(&lock_prog, "%s/etc/lock", G_gisbase());

    snprintf(path, sizeof(path), "%s/.gislock", mapset_new_path);
    G_debug(2, "%s", path);

    ret = G_spawn(lock_prog, lock_prog, path, gis_lock, NULL);
    G_debug(2, "lock result = %d", ret);
    G_free(lock_prog);

    /* Warning: the value returned by system() is not that returned by exit() in
     * executed program e.g. exit(1) -> 256 (multiplied by 256) */
    if (ret != 0) {
        /* .gislock does not exist */
        if (access(path, F_OK) != 0)
            G_fatal_error(_("Lock file of mapset <%s> cannot be checked"),
                          mapset_new);
        else
            G_fatal_error(_("There appears to be an active GRASS session in "
                            "selected mapset <%s>"),
                          mapset_new);
    }

    /* Clean temporary directory */
    snprintf(path, sizeof(path), "%s/etc/clean_temp", G_gisbase());
    G_verbose_message(_("Cleaning up temporary files..."));
    G_spawn(path, "clean_temp", NULL);

    /* Reset variables */
    G_setenv("GISDBASE", gisdbase_new);
    G_setenv("LOCATION_NAME", location_new);
    G_setenv("MAPSET", mapset_new);

    /* Remove old lock */
    snprintf(path, sizeof(path), "%s/.gislock", mapset_old_path);
    remove(path);

    G_free(mapset_old_path);

    shell = getenv("SHELL");
    /* For bash and zsh, we support switching of history, tcsh not (yet). */
    if (shell && (strstr(shell, "bash") || strstr(shell, "zsh"))) {
        G_important_message(_("Mapset switched."));
    }
    else {
        G_important_message(_("Mapset switched. Your shell continues "
                              "to use the history for the old mapset"));
    }
    if (shell && strstr(shell, "tcsh")) {
        G_important_message(_("You can switch the history by commands:\n"
                              "history -S; history -L %s/.history; setenv "
                              "histfile=%s/.history"),
                            mapset_new_path, mapset_new_path);
    }

    G_verbose_message(_("Your current mapset is <%s>"), mapset_new);

    G_free(mapset_new_path);

    return (EXIT_SUCCESS);
}
