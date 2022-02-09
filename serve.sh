LLsub -i --resv-ports 1
PORTAL_FWNAME="$(id -un | tr '[A-Z]' '[a-z]')-stream"
PORTAL_FWFILE="/home/gridsan/portal-url-fw/${PORTAL_FWNAME}"
echo $PORTAL_FWFILE
echo "Portal URL is: https://${PORTAL_FWNAME}.fn.txe1-portal.mit.edu/"
echo "http://$(hostname -s):${SLURM_STEP_RESV_PORTS}/" >> $PORTAL_FWFILE

chmod u+x ${PORTAL_FWFILE}

streamlit run main.py --server.port ${SLURM_STEP_RESV_PORT}

