# yangre-gui

Yangre-gui is the idea of Benoit Claise and was built by Pieter Lewyllie for the [IETF 99 Hackathon](https://www.ietf.org/hackathon/99-hackathon.html)

It is a GUI on top of W3C-compliant regex validators like w3cgrep and yangre (one of the tools from  [libyang](https://github.com/CESNET/libyang)) so that one can be sure their regexs will work in YANG models.

For context, this was a major issue that Openconfig had. While there were a number of POSIX/Perl validators like regex101.com, there wasn't a W3C one.

## Getting Started

After cloning the project:

- compile and install the w3cgrep utility (it may be required to explicitly install and link with libxml2);
- configure `config.py` with the appropriate paths for the yangre and w3cgrep executables. I had some issues with yangre not finding the right library files, so I included an explicit path to the library. Feel free to remove or customize this as needed.

Best is to start it via the UWSGI.INI file

### Prerequisites

* Have w3cgrep and yangre installed on the local machine
* Python 3.5
* Flask


## Resources
* See [RFC 7950 section 9.4.5](https://tools.ietf.org/html/rfc7950#section-9.4.5) for details on the YANG regular expressions.
* See [RFC 7950 section 6.1.3](https://tools.ietf.org/html/rfc7950#section-6.1.3) for information on quoting

## Special notes on Yang Catalog edition

The scripts have been tuned to be integrated into https://yangcatalog.org and the docker directory has been removed.

## Acknowledgments

Thanks to Joe Clarke, Radek Krejci, all the testers from IETF and especially Benoit Claise for allowing me to participate! :)
