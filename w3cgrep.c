/*
 * w3cgrep.c --
 *
 * A poor man's grep which uses XSD regular expressions instead of any
 * of the other regular expressions.
 *
 * Use this tool to check yang patterns. Requires libxml2.
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#if !defined(WIN32)
/* Should be possible to support this
   for win32 too, but it's not needed */
#include <libxml/xmlregexp.h>
#endif

static const char *progname = "w3cgrep";

static int invert_flag = 0;
static int count_flag = 0;
static int mult_flag = 0;

static void
grep_file(FILE *in, xmlRegexpPtr regex, const char *fname)
{
    char line[1024];
    int len;
    unsigned count = 0;

    while (! feof(in)) {
        if (! fgets(line, sizeof(line), in)) {
            break;
        }
        len = strlen(line);
        if (len) line[len-1] = 0;
        if (xmlRegexpExec(regex, BAD_CAST(line)) == ! invert_flag) {
            count++;
            if (! count_flag) {
                if (mult_flag) {
                    fprintf(stdout, "%s:", fname);
                }
                fprintf(stdout, "%s\n", line);
            }
        }
    }
    if (count_flag) {
        if (mult_flag) {
            fprintf(stdout, "%s:", fname);
        }
        fprintf(stdout, "%u\n", count);
    }
}

static int
grep(const char *filename, xmlRegexpPtr regex)
{
    FILE *in;
    const char *fname = filename;

    if (! filename || strcmp(filename, "-") == 0) {
        clearerr(stdin);
        in = stdin;
        fname = NULL;
    } else {
        in = fopen(filename, "r");
        if (! in) {
            perror(progname);
            return -1;
        }
    }

    grep_file(in, regex, fname);

    if (fflush(stdout) || ferror(stdout) || ferror(in)) {
        perror(progname);
        exit(1);
    }

    if (in != stdin) {
        fclose(in);
    }

    return 0;
}

int
main(int argc, char **argv)
{
    const char *usage = "Usage: %s [-c] [-h] [-v] [V] pattern files ... \n";
    xmlRegexpPtr regex;
    int c, status = EXIT_SUCCESS;

    while ((c = getopt(argc, argv, "chivV")) >= 0) {
        switch (c) {
        case 'c':
            count_flag = 1;
            break;
        case 'h':
            printf(usage, progname);
            exit(EXIT_SUCCESS);
        case 'v':
            invert_flag = 1;
            break;
        case 'V':
            printf("%s version 0.2.0\n", progname);
            exit(EXIT_SUCCESS);
        default:
            exit(EXIT_FAILURE);
        }
    }

    if (optind == argc) {
        fprintf(stderr, usage, progname);
        exit(EXIT_FAILURE);
    }

    regex = xmlRegexpCompile(BAD_CAST(argv[optind]));
    if (! regex) {
        fprintf(stderr, "%s: regex pattern compilation failed\n", progname);
        return EXIT_FAILURE;
    }
    optind++;

    if (optind == argc) {
        if (grep(NULL, regex) < 0) {
            status = EXIT_FAILURE;
        }
    } else {
        mult_flag = (argc - optind) > 1;
        for (; optind < argc; optind++) {
            if (grep(argv[optind], regex) < 0) {
                status = EXIT_FAILURE;
            }
        }
    }

    xmlRegFreeRegexp(regex);

    return status;
}

