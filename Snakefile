##
## Specific for ALS850
##

# Condiguration

configfile: "config.yaml"


include: "core.smake"
include: "process.smake"
include: "germline.smake"

# Variables

FLUSH_DIR="/flush3/{USER}".format(**os.environ)

